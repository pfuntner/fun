#! /usr/bin/env python

import server

def fun():
  return 'This is server.fun(): foo={foo!r}, bar={bar}'.format(foo=foo if hasattr(server, 'foo') else False, bar=bar if hasattr(server, 'bar') else False)

assert __name__ != '__main__', 'server.py should not be called directly'
