#!/usr/bin/env python
# coding:utf-8
import sys
import os
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,format='%(asctime)s : %(message)s')

def os_system(cmd,info = 1):
    msg = "> exec: {}".format(cmd)
    if info == 1:
        logging.info(msg)
    error = os.system(cmd)
    if error > 0:
        logging.info("run result: {}".format(error))
        sys.exit(1)

def main():
    logging.info("init app...")

try:
    main()
except Exception as e:
    print("=====error====")
    print(e)
    sys.exit(1)
