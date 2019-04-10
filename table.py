#! /usr/bin/env python

import re
import logging
import argparse

class Table(list):
  regexp = re.compile(r'\{:[<>]')

  class Row(object):
    def __init__(self, *args):
      self.cols = tuple(map(str, args))

  def __init__(self, *headings, **vargs):
    global log

    if 'log' not in globals():
      log = logging.getLogger()

    keys = set(vargs.keys()) - set(['centered'])
    assert not keys, 'Invalid keywords: {keys}'.format(keys=', '.join(keys))

    super(Table, self).__init__()
    self.headings = self.Row(*headings) if headings else None

    self.centered = vargs.get('centered', False)

    self.widths = [len(col) for col in self.headings.cols] if self.headings else []

    # We'll assume that a column is numeric until we find an exception.
    self.isNumerics = [True] * len(self.widths) if self.headings else []

  @classmethod
  def isNumeric(cls, value):
    try:
      num = float(value)
      return True
    except:
      return False
    
  def append(self, *cols):
    super(Table, self).append(self.Row(*cols))
    log.debug('There are now {rows} rows'.format(rows=len(self)))
   
    # maintain the maximum widths of columns and remember if a column is completely numeric or not
    for (col_num, col) in enumerate(self[-1].cols):
      if col_num >= len(self.widths):
        self.widths.append(len(col))
        self.isNumerics.append(self.isNumeric(col))
      else:
        self.widths[col_num] = max(self.widths[col_num], len(col))
        self.isNumerics[col_num] = self.isNumerics[col_num] and self.isNumeric(col)

  @staticmethod
  def sorter(col):
    """
    Returns a method to be used by sort methods to extract the a comparison key.  
    I thought this could be used in general if the caller wanted to sort a table 
    on the fly (`sorted(Table)`) which does not affect the source table but I
    don't think that's the case.  You can certainly call `sorted(Table)` but
    it returns a list which is not as useful as having a Table.
    """
    return lambda row: row.cols[col]

  def sort(self, col):
    log.debug('Sorting with {rows} rows'.format(rows=len(self)))
    super(Table, self).sort(key=self.sorter(col))

  def __str__(self):
    log.debug('Rendering string with {rows} rows'.format(rows=len(self)))
    return self.format(([self.headings] if self.headings else []) + self)

  def format(self, rows):
    log.debug('widths: {self.widths}, isNumerics: {self.isNumerics}'.format(**locals()))

    ret = []
    format_string = ' '.join(['{{:{direction}{width}}}'.format(
      direction='>' if self.isNumerics[col_num] else '<',
      width=self.widths[col_num],
    ) for col_num in range(len(self.widths))])

    for (row_num, row) in enumerate(rows):
      log.debug('Rendering row {row_num}: {row.cols}'.format(**locals()))
      cols = row.cols + tuple([''] * (len(self.widths) - len(row.cols)))
      ret.append((self.regexp.sub('{:^' if self.centered else '{:<', format_string) if self.headings and row_num == 0 else format_string).format(*cols))

    return '\n'.join(ret)

if __name__ == '__main__':
  import math

  parser = argparse.ArgumentParser(description='Driver for Table class')
  parser.add_argument('-H', '--headings', dest='headings', action='store_true', help='Use headings')
  parser.add_argument('-c', '--centered', dest='centered', action='store_true', help='Center headings')
  parser.add_argument('-l', '--logging', dest='logging', action='store_false', help='Disable logging', default=True)
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  args = parser.parse_args()

  if args.logging:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
    log = logging.getLogger()
    log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  if args.headings:
    table = Table('one', 'two', 'three', 'four', centered=args.centered)
  else:
    table = Table()
  table.append('a', 'b', 'c', '+1')
  table.append('This', 'is', 'a test', '1.2')
  table.append('1', '2', '3', 4)
  table.append('', '', '', 1e50)
  table.append('easy', 'as', 'pi', math.pi)
  table.append('single column')
  print str(table)

  empty = Table()
  print str(empty)
