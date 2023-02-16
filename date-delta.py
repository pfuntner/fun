#! /usr/bin/env python3

import re
import sys
import signal
import logging
import argparse
import datetime

from dateutil.relativedelta import relativedelta

DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

parser = argparse.ArgumentParser(description='Perform `date math` with dateutil.relativedelta')
parser.add_argument('terms', metavar='term', nargs='+', help='One or more delta terms.  Eg: months=6')
parser.add_argument('-f', '--format', default=DEFAULT_DATE_FORMAT, help=f'Date format to use.  Default: (DEFAULT_DATE_FORMAT!r)')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger(sys.argv[0])
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

regexp = re.compile(r'^([^=]+)=(.+)$')
terms = dict()
for term in args.terms:
  try:
    match = regexp.search(term)
    if match is None:
      raise Exception(f'No match with {regexp.pattern!r} pattern')
    terms[match.group(1)] = int(match.group(2))
  except Exception as e:
    parser.error(f'Could not parse {term!r}: {e!s}')

print((datetime.datetime.now() - relativedelta(**terms)).strftime(args.format))
