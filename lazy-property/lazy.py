#! /usr/bin/env python3

import sys
import signal
import logging
import argparse

"""
  https://stevenloria.com/lazy-properties/
  We import this in our other *_info class to lazyload attributes
"""
def lazy_property(fn):
    '''Decorator that makes a property lazy-evaluated.
    '''
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property

class Foo(object):
  @lazy_property
  def bar(self):
    ret = 'foobar'
    log.info(f'Foo.bar() returning {ret!r}')
    return ret

class Meta(object):
  def __init__(self):
    self.foo = Foo()

def explore(o):
  ret = {}
  if o is not None:
    for elem in dir(o):
      if not elem.startswith('__'):
        ret[elem] = repr(getattr(o, elem))
    if hasattr(o, 'foo'):
      if o.foo is not None:
        for elem in dir(o.foo):
          if not elem.startswith('__'):
            ret[f'foo.{elem}'] = repr(getattr(o.foo, elem))
  return ret

parser = argparse.ArgumentParser(description=sys.argv[0])
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.INFO - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

log.info(f'Welcome to {sys.argv[0]}')
obj = Meta()
log.info(f'object is instantiated')
log.info(explore(obj))
log.info(f'obj.bar = {obj.foo.bar!r}')
log.info(explore(obj))
log.info(f'obj.bar = {obj.foo.bar!r}')
log.info(explore(obj))

obj.foo = None
log.info(explore(obj))
log.info(f'obj.bar = {obj.foo.bar!r}')

log.info(f'Goodbye from {sys.argv[0]}')
