import os
import logging
from optparse import OptionParser
from pt.libs.utils import set_logging,set_logging_file
from pt.cmd_options import CmdOptions
from pt.apps.gcp import gcp
import pt.apps.server.ubuntu as server_ubuntu
from pt import __version__
import pprint

current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))


def main():
    parser = OptionParser()
    parser.add_option("-l", "--level", default="info", dest="level", help="logging level: debug|info")
    parser.add_option("-q", "--query", default="", dest="query", help="query")
    parser.add_option("-f", "--log_file", default="", dest="log_file", help="log_file")
    parser.add_option("-m", "--module", default="", dest="module", help="""
        server.ubuntu.init_docker
        server.ubuntu.add_docker_group | gcp
    """)
    (options, args) = parser.parse_args()
    CmdOptions.set_options(options)

    if options.level == "debug":
        set_logging(logging.DEBUG)
    else:
        set_logging(logging.INFO)
    if len(options.log_file) > 0:
        set_logging_file(options.level,options.log_file)

    logging.info(options)
    logging.info(__version__)
    logging.info(current_dir)

    if options.module == "help":
        pprint.pprint([
            "update",
            "gcp",
            "gcp.init_machine_template",
            "server.ubuntu.init_docker",
            "server.ubuntu.add_docker_group"
        ])

    if options.module == "gcp":
        gcp.main(options.query)
    if options.module == "update":
        os.system("sudo pip3 install git+https://github.com/xyz71148/pt")
        os.system("pt")
    if options.module == "gcp.init_machine_template":
        gcp.init_machine_template()
    if options.module == "server.ubuntu.init_docker":
        server_ubuntu.init_docker()
    if options.module == "server.ubuntu.add_docker_group":
        server_ubuntu.add_docker_group()


if __name__ == '__main__':
    main()
