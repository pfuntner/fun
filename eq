#! /usr/bin/env python2

class Obj(object):
  def __init__(self, x):
    self.x = x

  def __str__(self):
    return str(self.x)

  def __eq__(self, other):
    ret = self.x == other.x
    print '__eq__({self!s}, {other!s}) -> {ret}'.format(**locals())
    return ret

o1 = Obj(1)
o2 = Obj(2)
o3 = Obj(1)

print o1 == o2
print o1 == o3
