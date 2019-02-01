#! /usr/bin/env python

import server

def see(name):
  print '{name}: {value!r}'.format(value=eval(name), **locals())

server.foo = 'bar'

see('server.fun()')
see('server.foo')
