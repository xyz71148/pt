import os
import logging
from optparse import OptionParser
from pt.libs.utils import set_logging
from pt.cmd_options import CmdOptions

current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))


def main():
    parser = OptionParser()
    parser.add_option("-l", "--logging", default="info", dest="logging", help="logging level: debug|info")
    (options, args) = parser.parse_args()
    CmdOptions.set_options(options)
    if options.logging == "debug":
        set_logging(logging.DEBUG)
    else:
        set_logging(logging.INFO)

    logging.debug(options)
    logging.debug(current_dir)


if __name__ == '__main__':
    main()
