#! /usr/bin/env python

"""
   I've always been a fan of using the getopt module but am sometimes encouraged by folks to use argparse.  It does seem to have
   some advantages but it's always been a little cryptic to me too.  So I came up with a sample for some common options/arguments
   I often what to deal with and put in my own tools.  It's still a little unnatural to me but it works.
   
   With regard to mutually exclusive options, argparse gives you a way to do it but it does not allow the options to appear on the
   same command line - an error is thrown when this happens.  When I implement mutually exclusive options with getopt, I typically
   only accept the last option and behave as though the other options were not specified at all.  I would kind of prefer that behavior
   but this isn't a bad compromise.
"""

import sys
import argparse

def see(expr):
  value = eval(expr)
  sys.stderr.write('{expr}: {value!r}\n'.format(**locals()))

parser = argparse.ArgumentParser(description='A sample use of ArgumentParser')
parser.add_argument('-v', '--verbose', dest='verbose', action='count',  help='Toggle verbose debugging')
parser.add_argument('--cfg', dest='cfg', help='Specify configuration filename', required=True)

group = parser.add_mutually_exclusive_group()
group.add_argument('--opt1', dest='opt1', action='store_true',  help='Option 1')
group.add_argument('--opt2', dest='opt2', action='store_true',  help='Option 2')

parser.add_argument('pattern', help='Regular expression pattern')
parser.add_argument('files', metavar='file', nargs='*', help='Files to process')

args = parser.parse_args()

# args.verbose is None if not specified - to test toggling, try `(args.verbose or 0) % 2`
see('args.verbose')

see('args.cfg')
see('args.pattern')
see('args.files')

see('args.opt1')
see('args.opt2')

parser.print_help(sys.stderr) # could be used when validating options/arguments

print 'Done'
