#! /usr/bin/env python2

import logging
import argparse

import common


parser = argparse.ArgumentParser(description='import_test')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

obj = common.Obj()
log.info('obj.value: {obj.value}'.format(**locals()))
