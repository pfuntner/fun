#! /usr/bin/env python

import logging
import argparse

import subprocess

class Table(list):
  class Row(object):
    def __init__(self, *args):
      self.cols = args

  def __init__(self, *headings):
    global log

    if 'log' not in globals():
      log = logging.getLogger()
      
    super(Table, self).__init__()
    self.headings = [self.Row(*headings)] if headings else None

  def append(self, *cols):
    super(Table, self).append(self.Row(*cols))
    log.debug('There are now {rows} rows'.format(rows=len(self)))

  @staticmethod
  def sorter(col):
    return lambda row: row.cols[col]

  def sort(self, col):
    log.debug('Sorting with {rows} rows'.format(rows=len(self)))
    super(Table, self).sort(key=self.sorter(col))

  def __str__(self):
    log.debug('Rendering string with {rows} rows'.format(rows=len(self)))
    p = subprocess.Popen('column -t --separator |'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for row in (self.headings if self.headings else []) + self:
      p.stdin.write('|'.join(row.cols) + '\n')
    p.stdin.close()
    ret = p.stdout.read().strip('\n')
    p.wait()
    return ret

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Driver for Table class')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  parser.add_argument('-l', '--logging', dest='logging', action='store_false', help='Disable logging', default=True)
  args = parser.parse_args()
  
  if args.logging:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
    log = logging.getLogger()
    log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  table = Table()
  table.append('a', 'b', 'c')
  table.append('This', 'is', 'a test')
  print str(table)
