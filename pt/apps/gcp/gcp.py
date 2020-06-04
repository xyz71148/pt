import os
import requests
import time
import traceback
import sys
import logging
import _thread
import pt.libs.utils as utils
import simplejson as json
from pt.apps.gcp.config_files import shadowsocks_supervisor_config,ovpn_initpki,build_client_full


def os_system(cmd, info=1,e=True):
    cmd = cmd.strip('"').strip(",")
    msg = "> exec: {}".format(cmd)
    if info == 1:
        print(msg)
    error = os.system(cmd)
    if error > 0 and  e:
        raise Exception("run result: {}".format(error))


class Gcp():
    gae_project_id = None
    base_username = None
    base_password = None
    instance_name = None
    server_type = None
    init_scripts = None
    instance_ports_config = None
    instance = None
    port_password = None
    base_url = None
    http_server_port = None
    host_ip = None
    email = None
    t_num = 0
    worker_config = None

    def __init__(self, query):
        logging.debug(query)
        query = query.split("|")
        self.instance_name = query[0]
        self.gae_project_id = query[1]
        self.base_username = query[2]
        self.base_password = query[3]
        self.base_url = os.getenv("BASE_URL", None)
        logging.debug(vars(self))
        if self.base_url is None:
            self.base_url = "https://{}.appspot.com".format(self.gae_project_id)

        self.host_ip = utils.get_host_ip()
        self.url_boot = "{}/api/compute/instance/boot/{}/{}".format(self.base_url, self.instance_name, self.host_ip)

        self.host_name = self.host_ip.replace(".", "_")
        self.ovpn_file = "/opt/openvpn/{}.ovpn".format(self.host_name)
        self.ovpn_data = "ovpn-data"

    def get_instance_info(self):
        logging.info("get_instance_info: %s", self.url_boot)
        res = requests.get(self.url_boot, auth=(self.base_username, self.base_password))
        logging.debug(res.text)
        if res.status_code != 200:
            raise Exception("get_instance_info system error")
        res_json = res.json()
        if res_json['code'] != 200:
            raise Exception("get_instance_info error: " + json.dumps(res_json))
        self.instance = res_json['body']
        if self.email is None:
            self.email = res_json['body']['email']
            logging.info("email: %s", self.email)
        self.worker_config = self.instance['worker_config']
        self.proxy_server_port = self.instance['proxy_server_port']
        self.proxy_server_image = self.instance['proxy_server_image']

        self.server_type = res_json['body']['server_type']
        self.init_scripts = res_json['body']['init_scripts']
        self.instance_ports_config = res_json['body']['config']
        self.port_password = res_json['body']['config']['port_password']
        return res_json['body']

    @classmethod
    def report_error(self, e, error):
        logging.error(error)
        if self.email is None:
            return
        try:
            requests.put("{}//api/utils/email".format(self.base_url),
                     dict(email=self.email, title=e, content=error),
                     auth=(self.base_username, self.base_password))
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = "{},{},{}".format(exc_type, exc_value, traceback.format_tb(exc_traceback))
            logging.error(msg)

    def shell_run(self, cmd, raise_error=False):
        env = dict(os.environ, host_ip=self.host_ip, base_url=self.base_url, base_username=self.base_username,
                   base_password=self.base_password, instance_name=self.instance_name)
        logging.info("run: %s", cmd)
        try:
            result = utils.shell_exec_result(cmd, **env)
            logging.info(result)
            return result
        except Exception as e:
            logging.error(e)
            if raise_error:
                raise e

    def run_shadowsocks_docker(self):
        ports = " ".join(["-p {port}:{port}".format(port=port) for port in self.port_password.keys()])
        self.shell_run("sudo docker rm -f shadowsocks")
        self.shell_run("sudo docker run -d --name shadowsocks -e SERVER_START=1 "
                       "-v /tmp/shadowsocks:/etc/supervisor/conf_d -e "
                       "BOOTS=shadowsocks " + ports + " --cap-add=NET_ADMIN sanfun/public:shadowsocks-v1",
                       raise_error=True)
        self.upload_instance_status()

    def run_proxy_go(self):
        proxy = "https://{}.appspot.com".format(self.gae_project_id)
        self.shell_run("sudo docker rm -f proxy")
        self.shell_run("sudo docker run -d --name proxy "
                       "-e PORT={port} "
                       "-e IP=0.0.0.0 "
                       "-e PROXY={proxy} "
                       "-p {port}:{port} "
                       "{image}".format(image=self.proxy_server_image, port=self.proxy_server_port, proxy=proxy),
                       raise_error=True)

    def upload_instance_status(self):
        file_upload = ""
        if self.server_type == "openvpn":
            file_upload = "-F files=@{}".format(self.ovpn_file)

        self.shell_run(
            "curl -u {base_username}:{base_password} -X PUT -F ip={host_ip} {file_upload} {report_url}".format(
                base_username=self.base_username,
                base_password=self.base_password,
                host_ip=self.host_ip,
                report_url=self.url_report,
                file_upload=file_upload
            ))

    def start_new_thread(self,func):
        _thread.start_new_thread(func, ())

    def run_init_scripts(self):
        init_scripts = self.init_scripts
        if len(init_scripts) > 0:
            self.shell_run(init_scripts)

    def run_workers(self):
        self.shell_run("mkdir -p /opt/worker")
        utils.file_write(self.path_workers_json, json.dumps(self.worker_config))
        utils.file_write(self.path_worker_setting_json, json.dumps(self.worker_config['setting']))
        utils.file_write(self.path_worker_account_json, json.dumps(self.worker_config['gcp_account']))

        docker_image = self.worker_config['docker_image']
        worker_port = self.worker_config['worker_port']
        executor = "{}__{}".format(self.instance_name, worker_port)

        os_system("sudo docker rm -f {}".format(self.instance_name), e=False)
        if worker_port is None or len(worker_port) == 0:
            return

        temp = "sudo docker run --cap-add=NET_ADMIN --name {name} -d -p {port}:{port} " \
               "-e GOOGLE_APPLICATION_CREDENTIALS=/opt/worker/account.json " \
               "-e EXECUTOR={executor} -e APP=check,shel_check_build,shel_check_deploy,app_prod " \
               "-e FLASK_ENV=prod -e PYTHONPATH=/data/home " \
               "-v /opt/worker:/opt/worker -e IP={host_ip} -e PORT={port} " \
               "{docker_image}"

        os_system(
            temp.format(
                docker_image=docker_image,
                host_ip=self.host_ip,
                port=worker_port,
                executor=executor,
                name=self.instance_name
            ),e=False)

    def run_shadowsocks(self):
        self.shell_run("mkdir -p /tmp/shadowsocks")
        utils.file_write(self.path_shadowsocks_server_json, json.dumps(self.instance_ports_config))
        utils.file_write(self.path_shadowsocks_supervisor_config, shadowsocks_supervisor_config)
        self.run_shadowsocks_docker()

    def run_openvpn(self):
        if os.path.exists(self.ovpn_file):
            return
        self.shell_run("sudo mkdir -p /opt/openvpn")
        self.shell_run("sudo docker rm -f {}".format(self.ovpn_data))
        self.shell_run("sudo docker run --name {ovpn_data} -v /etc/openvpn busybox".format(ovpn_data=self.ovpn_data))

        port = list(self.port_password.keys())[0]
        pwd = self.port_password[port]

        self.shell_run(
            "sudo docker run --volumes-from {ovpn_data} kylemanna/openvpn ovpn_genconfig -u udp://{host_ip}:{port}".format(
                ovpn_data=self.ovpn_data,
                host_ip=self.host_ip,
                port=port,
            ))

        ovpn_initpki_str = ovpn_initpki.format(sep=r"\r", ovpn_data=self.ovpn_data, pwd=pwd, host_ip=self.host_ip)
        utils.file_write("/opt/openvpn/ovpn_initpki.txt", ovpn_initpki_str)

        os_system("expect -f /opt/openvpn/ovpn_initpki.txt", info=1)

        build_client_full_str = build_client_full.format(sep=r"\r", ovpn_data=self.ovpn_data, pwd=pwd,
                                                         host_name=self.host_name)
        utils.file_write("/opt/openvpn/build_client_full.txt", build_client_full_str)
        os_system("expect -f /opt/openvpn/build_client_full.txt", info=1)
        self.shell_run(
            "sudo docker run --volumes-from {ovpn_data}  kylemanna/openvpn ovpn_getclient {host_name} > {ovpn_file}".format(
                ovpn_data=self.ovpn_data,
                host_name=self.host_name,
                ovpn_file=self.ovpn_file
            ), raise_error=True)

        self.shell_run("sudo docker rm -f openvpn")
        self.shell_run(
            "sudo docker run --name openvpn --volumes-from {ovpn_data} -d -p {port}:{port}/udp --cap-add=NET_ADMIN kylemanna/openvpn".format(
                ovpn_data=self.ovpn_data,
                host_name=self.host_name,
                port=port
            ), raise_error=True)
        self.upload_instance_status()

    def init_instance(self):
        self.get_instance_info()
        self.url_report = "{}/api/compute/instance/{}/{}".format(self.base_url, self.server_type, self.instance_name)
        self.path_shadowsocks_supervisor_config = "/tmp/shadowsocks/shadowsocks.conf"
        self.path_shadowsocks_server_json = "/tmp/shadowsocks/config.json"
        self.path_workers_json = "/tmp/workers.json"
        self.path_worker_setting_json = "/opt/worker/setting.json"
        self.path_worker_account_json = "/opt/worker/account.json"

        logging.debug("init gcp: %s", vars(self))
        self.start_new_thread(self.run_proxy_go)
        self.start_new_thread(self.run_init_scripts)
        self.start_new_thread(self.run_workers)

        if self.server_type == "shadowsocks":
            self.start_new_thread(self.run_shadowsocks)

        if self.server_type == "openvpn":
            self.start_new_thread(self.run_openvpn)

    def run_cmd(self):
        cmd = self.get_instance_info()['cmd']
        output = self.shell_run(cmd)
        r = requests.put("{}/api/compute/instance/cmd/result/{}".format(self.base_url, self.instance_name),
                         dict(cmd_result=output), auth=(self.base_username, self.base_password))
        logging.info("cmd report result: %s", r.text)

    def check(self):
        instance_info = self.get_instance_info()
        cmd = instance_info['cmd']
        if len(cmd) > 0:
            self.start_new_thread(self.run_cmd)

        if self.server_type == "shadowsocks":
            instance_ports_config = utils.file_read(self.path_shadowsocks_server_json)
            if json.dumps(self.instance_ports_config) != instance_ports_config:
                utils.file_write(self.path_shadowsocks_server_json, json.dumps(self.instance_ports_config))
                self.start_new_thread(self.run_shadowsocks_docker)
        if os.path.exists(self.path_workers_json):
            workers_json = utils.file_read(self.path_workers_json)
            if workers_json != json.dumps(self.worker_config):
                self.start_new_thread(self.run_workers)

    def run(self):
        init = False
        while True:
            try:
                if init is False:
                    self.init_instance()
                    time.sleep(5)
                    init = True
                if int(time.time()) % 3600 == 0:
                    logging.info("checking instance")
                self.check()
                time.sleep(3)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                msg = "{},{},{}".format(exc_type,exc_value,traceback.format_tb(exc_traceback))
                self.report_error(e, msg)
                time.sleep(20)


def main(query):
    g = Gcp(query)
    g.run()


def init_machine_template():
    if not os.path.exists("/swapfile"):
        os.system("sudo dd if=/dev/zero of=/swapfile bs=1M count=1024")
        os.system("sudo mkswap -f /swapfile")
        os.system("sudo mkswap -f /swapfile && sudo chmod 0600 /swapfile && sudo swapon /swapfile && free -m")
        os.system("sudo chmod 777 /etc/fstab && sudo echo '/swapfile none swap sw 0 0' >> /etc/fstab && sudo chmod 644 /etc/fstab")
        os.system("sudo chmod 777 /etc/sysctl.conf && sudo echo 'vm.swappiness=10' >> /etc/sysctl.conf && sudo echo 'vm.vfs_cache_pressure=50' >> /etc/sysctl.conf && sudo chmod 644 /etc/sysctl.conf")
    os.system("sudo cat /etc/fstab")
    os.system("sudo cat /etc/sysctl.conf | grep vm.")
    os.system("sudo rm -rf /opt/openvpn /opt/worker /tmp/*.py /tmp/*.log /tmp/*.json /tmp/*.sh /tmp/shadowsocks")
    os.system("sudo docker rm -f $(sudo docker ps -aq)")
    os.system("sudo pip3 install setuptools==40.3.0")

if __name__ == '__main__':
    utils.set_logging(logging.DEBUG)
    main(os.getenv("query"))
