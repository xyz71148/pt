import os
import logging
from optparse import OptionParser
from pt.libs.utils import set_logging
from pt.cmd_options import CmdOptions
from pt.apps.gcp import gcp
import pt.apps.server.ubuntu as server_ubuntu


current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))


def main():
    parser = OptionParser()
    parser.add_option("-l", "--logging", default="info", dest="logging", help="logging level: debug|info")
    parser.add_option("-m", "--module", default="", dest="module", help="""
        server.ubuntu.init_docker
        server.ubuntu.add_docker_group | gcp
    """)
    (options, args) = parser.parse_args()
    CmdOptions.set_options(options)
    if options.logging == "debug":
        set_logging(logging.DEBUG)
    else:
        set_logging(logging.INFO)

    logging.debug(options)
    logging.debug(current_dir)
    if options.module == "gcp":
        gcp.main()

    if options.module == "server.ubuntu.init_docker":
        server_ubuntu.init_docker()

    if options.module == "server.ubuntu.add_docker_group":
        server_ubuntu.add_docker_group()


if __name__ == '__main__':
    main()
