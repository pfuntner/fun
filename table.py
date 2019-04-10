#! /usr/bin/env python

import re
import logging
import argparse

class Table(list):
  regexp = re.compile(r'\{:[<>]')

  class Row(object):
    def __init__(self, *args):
      self.cols = args

  def __init__(self, *headings, **vargs):
    global log

    keys = set(vargs.keys()) - set(['centered'])
    assert not keys, 'Invalid keywords: {keys}'.format(keys=', '.join(keys))

    if 'log' not in globals():
      log = logging.getLogger()

    super(Table, self).__init__()
    self.headings = [self.Row(*headings)] if headings else None

    self.centered = vargs.get('centered', False)

  def append(self, *cols):
    super(Table, self).append(self.Row(*(str(col) for col in cols)))
    log.debug('There are now {rows} rows'.format(rows=len(self)))

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
    return self.format((self.headings if self.headings else []) + self)

  def format(self, rows):
    # figure width and `numeracy` of columns
    widths = []
    isNumerics = []
    for (row_num, row) in enumerate(rows):
      for (col_num, col) in enumerate(row.cols):
        if ((not self.headings) or (row_num > 0)) and (len(self) > 0):
          try:
            num = float(col)
            isNumeric = True
          except:
            isNumeric = False
        else:
          """
          if we're processing the heading row, we'll pretend the column is numeric since it shouldn't decide contribute
          to the decision of whether to left or right-justify the column
          """
          isNumeric = True

        if col_num >= len(widths):
          widths.append(len(col))
          isNumerics.append(isNumeric)
        else:
          widths[col_num] = max(widths[col_num], len(col))
          isNumerics[col_num] = isNumerics[col_num] and isNumeric

    log.debug('widths: {widths}, isNumerics: {isNumerics}'.format(**locals()))

    ret = []
    format_string = ' '.join(['{{:{direction}{width}}}'.format(
      direction='>' if isNumerics[col_num] else '<',
      width=widths[col_num],
    ) for col_num in range(len(widths))])

    for (row_num, row) in enumerate(rows):
      log.debug('Rendering row {row_num}: {row.cols}'.format(**locals()))
      cols = row.cols + tuple([''] * (len(widths) - len(row.cols)))
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
