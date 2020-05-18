import os
import requests
import time
import traceback
import sys
import logging
import pt.libs.utils as utils
import simplejson as json

shadowsocks_supervisor_config = """[program:shadowsocks]
command=/bin/bash -c "/usr/local/bin/ssserver -vv -c /etc/supervisor/conf_d/config.json"
directory=/root/
autostart=true
autorestart=true
priority=10
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
stderr_logfile=/dev/fd/2
stderr_logfile_maxbytes=0"""

ovpn_initpki = """#exp_internal 1 # Uncomment for debug
set timeout -1
spawn sudo docker run -it --volumes-from {ovpn_data} kylemanna/openvpn ovpn_initpki
#expect -exact "Confirm removal:"
#send -- "yes{sep}"
expect -exact "Enter New CA Key Passphrase:"
send -- "{pwd}{sep}"
expect -exact "Re-Enter New CA Key Passphrase:"
send -- "{pwd}{sep}"
expect -exact "Common Name (eg: your user, host, or server name) \[Easy-RSA CA\]:"
send -- "{host_ip}{sep}"
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key:"
send -- "{pwd}{sep}"
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key:"
send -- "{pwd}{sep}"
expect eof"""

build_client_full = """spawn sudo docker run -it --volumes-from {ovpn_data} kylemanna/openvpn easyrsa build-client-full {host_name} nopass
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key"
send -- "{pwd}{sep}"
expect eof"""


def os_system(cmd, info=1):
    cmd = cmd.strip('"').strip(",")
    msg = "> exec: {}".format(cmd)
    if info == 1:
        print(msg)
    error = os.system(cmd)
    if error > 0:
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
    http_server_check_port = None
    host_ip = None

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

        self.url_boot = "{}/api/compute/instance/boot/{}".format(self.base_url, self.instance_name)
        self.host_ip = utils.get_host_ip()
        self.host_name = self.host_ip.replace(".", "_")
        self.ovpn_file = "/opt/openvpn/{}.ovpn".format(self.host_name)
        self.ovpn_data = "ovpn-data"

    def get_instance_info(self):
        logging.debug("get_instance_info: %s", self.url_boot)
        try:
            res = requests.get(self.url_boot, auth=(self.base_username, self.base_password))
            logging.debug(res.text)
            res_json = res.json()
            self.instance = res_json['body']
            self.server_type = res_json['body']['server_type']
            self.init_scripts = res_json['body']['init_scripts']
            self.instance_ports_config = res_json['body']['config']
            self.port_password = res_json['body']['config']['port_password']
            return res_json['body']
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = "{},{},{}".format(exc_type, exc_value, traceback.format_tb(exc_traceback))
            self.report_error(e, msg)

    @classmethod
    def report_error(self, e, error):
        logging.error(error)
        try:
            requests.put("{}//api/utils/email".format(self.base_url),
                     dict(email=self.instance['email'], title=e, content=error),
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

    def run_proxy_go(self):
        if os.path.exists("/bin/proxy_go") is False:
            self.shell_run("curl https://" + self.gae_project_id + ".appspot.com/static/proxy_go -o /bin/proxy_go && "
                                                                   "sudo chmod +x /bin/proxy_go")
        self.shell_run("pkill proxy_go")
        cmd = "nohup proxy_go {http_server_check_port} {http_server_port} https://{gae_project_id}.appspot.com  >> /tmp/proxy.log &".format(
            gae_project_id=self.gae_project_id,
            http_server_check_port=self.http_server_check_port,
            http_server_port=self.http_server_port
        )
        os_system(cmd, info=1)
        self.shell_run("pgrep proxy_go")

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

    def init_instance(self):
        self.get_instance_info()
        self.url_report = "{}/api/compute/instance/{}/{}".format(self.base_url, self.server_type, self.instance_name)
        self.path_shadowsocks_supervisor_config = "/tmp/shadowsocks/shadowsocks.conf"
        self.path_shadowsocks_server_json = "/tmp/shadowsocks/config.json"

        self.http_server_port = "0.0.0.0:80"
        self.http_server_check_port = "0.0.0.0:8001"

        logging.debug("init gcp: %s", vars(self))

        self.run_proxy_go()

        init_scripts = self.init_scripts
        if len(init_scripts) > 0:
            self.shell_run(init_scripts)

        if self.server_type == "shadowsocks":
            self.shell_run("mkdir -p /tmp/shadowsocks")
            utils.file_write(self.path_shadowsocks_server_json, json.dumps(self.instance_ports_config))
            utils.file_write(self.path_shadowsocks_supervisor_config, shadowsocks_supervisor_config)
            self.run_shadowsocks_docker()

        if self.server_type == "openvpn":
            self.init_openvpn()

        # self.shell_run("sudo docker ps")
        # self.shell_run("netstat -tnlp")
        self.upload_instance_status()

    def init_openvpn(self):
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

    def check(self):
        instance_info = self.get_instance_info()
        cmd = instance_info['cmd']
        if len(cmd) > 0:
            output = self.shell_run(cmd)
            r = requests.put("{}/api/compute/instance/cmd/result/{}".format(self.base_url, self.instance_name),
                             dict(cmd_result=output), auth=(self.base_username, self.base_password))
            logging.info(r.text)

        if self.server_type == "shadowsocks":
            instance_ports_config = utils.file_read(self.path_shadowsocks_server_json)
            if json.dumps(self.instance_ports_config) != instance_ports_config:
                utils.file_write(self.path_shadowsocks_server_json, json.dumps(self.instance_ports_config))
                self.run_shadowsocks_docker()
                self.upload_instance_status()

    def run(self):
        init = False
        while True:
            try:
                if init is False:
                    init = True
                    self.init_instance()
                if int(time.time()) % 3600 == 0:
                    logging.info("checking instance")
                self.check()
                time.sleep(1)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                msg = "{},{},{}".format(exc_type,exc_value,traceback.format_tb(exc_traceback))
                self.report_error(e, msg)
                time.sleep(10)


def main(query):
    g = Gcp(query)
    g.run()


def init_machine_template():
    utils.shell_exec_result("sudo rm -rf /opt/openvpn /tmp/*.py /tmp/*.log /tmp/*.sh /tmp/shadowsocks")
    utils.shell_exec_result("sudo docker rm -f $(sudo docker ps -aq)")


if __name__ == '__main__':
    utils.set_logging(logging.DEBUG)
    main(os.getenv("query"))
