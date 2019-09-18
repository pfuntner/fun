#! /usr/bin/env python2

import sys
import argparse

def see(expr):
  value = eval(expr)
  print '{expr}: {value!r}'.format(**locals())

see('sys.argv')
sys.argv = ['./pgm', '-vl', 'foo']
see('sys.argv')
parser = argparse.ArgumentParser(description='Kidnapping command line arguments')
parser.add_argument('-v', dest='verbose', action='store_true', help='Option -v')
parser.add_argument('-l', dest='long', action='store_true', help='Option -l')
parser.add_argument('args', metavar='arg', nargs='+', help='One or more arguments')
args = parser.parse_args()
see('args')
