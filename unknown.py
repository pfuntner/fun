#! /usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
(known, unknown) = parser.parse_known_args()

print(f'{known=}')
print(f'{unknown=}')

# print 'dir: {}'.format(dir(known))

# args = parser.parse_args()
# 
# logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
# log = logging.getLogger()
# log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
