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


class Gcp():
    gae_project_id = None
    base_username = None
    base_password = None
    instance_name = None
    server_type = None
    init_scripts = None
    instance_ports_config = None
    port_password = None
    base_url = None
    http_server_port = None
    http_server_check_port = None
    host_ip = None

    def __init__(self):
        self.gae_project_id = os.getenv("GAE_PROJECT_ID")
        self.base_username = os.getenv("BASE_USERNAME")
        self.base_password = os.getenv("BASE_PASSWORD")
        self.instance_name = os.getenv("INSTANCE_NAME")
        self.base_url = os.getenv("BASE_URL", None)
        logging.debug(vars(self))
        if self.base_url is None:
            self.base_url = "https://{}.appspot.com".format(self.gae_project_id)

        self.url_boot = "{}/api/compute/instance/boot/{}".format(self.base_url, self.instance_name)
        self.host_ip = utils.get_host_ip()


    def get_instance_info(self):
        logging.debug("get_instance_info: %s", self.url_boot)
        try:
            res = requests.get(self.url_boot, auth=(self.base_username, self.base_password))
            logging.debug(res.text)
            res_json = res.json()
            self.server_type = res_json['body']['server_type']
            self.init_scripts = res_json['body']['init_scripts']
            self.instance_ports_config = res_json['body']['config']
            self.port_password = res_json['body']['config']['port_password']
            return res_json['body']
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = "file: {},error: {},trace: {}".format(__file__, e,
                                                             repr(traceback.format_tb(exc_traceback)))
            self.report_error(msg)

    @classmethod
    def report_error(self, error):
        logging.error(error)

    def shell_run(self, cmd):
        env = dict(os.environ, ip=self.host_ip, base_api=self.base_url, basic_user_name=self.base_username,
                   basic_password=self.base_password, instance_name=self.instance_name)
        logging.info("run: %s", cmd)
        result = utils.shell_exec_result(cmd, **env)
        logging.info(result)
        return result

    def run_shadowsocks_docker(self):
        ports = " ".join(["-p {port}:{port}".format(port=port) for port in self.port_password.keys()])

        self.shell_run(
            "sudo docker rm -f shadowsocks  && sudo docker run -d --name shadowsocks -e SERVER_START=1 "
            "-v /tmp/shadowsocks:/etc/supervisor/conf_d -e "
            "BOOTS=shadowsocks " + ports + " --cap-add=NET_ADMIN sanfun/public:shadowsocks-v1")

    def run_proxy_go(self):
        if os.path.exists("/bin/proxy_go") is False:
            self.shell_run("curl https://"+self.gae_project_id+".appspot.com/static/proxy_go -o /bin/proxy_go && "
                           "sudo chmod +x /bin/proxy_go")
        self.shell_run(
            "nohup proxy_go {http_server_check_port} {http_server_port} https://{gae_project_id}.appspot.com  >> "
            "/tmp/proxy.log &".format(
                gae_project_id=self.gae_project_id,
                http_server_check_port=self.http_server_check_port,
                http_server_port=self.http_server_port
            ))

    def upload_instance_status(self):
        self.shell_run(
            "curl -u {base_username}:{base_password} -X PUT -F ip={host_ip} -F init=1 {report_url}".format(
                base_username=self.base_username,
                base_password=self.base_password,
                host_ip=self.host_ip,
                report_url=self.url_report,
            ))

    def init_instance(self):
        self.get_instance_info()
        self.url_report = "{}/api/compute/instance/{}/{}".format(self.base_url, self.server_type, self.instance_name)
        self.path_shadowsocks_supervisor_config = "/tmp/shadowsocks/shadowsocks_supervisor_config.conf"
        self.path_shadowsocks_server_json = "/tmp/shadowsocks/shadowsocks_server_json.conf"

        self.http_server_port = "0.0.0.0:80"
        self.http_server_check_port = "0.0.0.0:8001"

        logging.debug("init gcp: %s", vars(self))

        init_scripts = self.init_scripts
        if len(init_scripts) > 0:
            self.shell_run(init_scripts)
        if self.server_type == "shadowsocks":
            self.shell_run("mkdir -p /tmp/shadowsocks")
            utils.file_write(self.path_shadowsocks_server_json, json.dumps(self.instance_ports_config))
            utils.file_write(self.path_shadowsocks_supervisor_config, shadowsocks_supervisor_config)
            self.run_shadowsocks_docker()
        self.upload_instance_status()

    def check(self):
        logging.info("checking instance")
        instance_info = self.get_instance_info()
        cmd = instance_info['cmd']
        if len(cmd) > 0:
            output = self.shell_run(cmd)
            r = requests.put("{}/api/compute/instance/cmd/result/{}".format(self.base_url, self.instance_name),
                             dict(cmd_result=output), auth=(self.base_username, self.base_password))
            logging.info(r.text)

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
                self.check()
                time.sleep(1)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                msg = "fline: {},error: {},trace: {}".format(__file__, e,
                                                                 repr(traceback.format_tb(exc_traceback)))
                self.report_error(msg)
                time.sleep(10)


def main():
    g = Gcp()
    g.run()


if __name__ == '__main__':
    utils.set_logging(logging.DEBUG)
    main()
