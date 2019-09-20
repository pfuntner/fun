#! /usr/bin/env python2

import math
import random
import string

def random_string():
  ret = ''
  while len(ret) < random.randint(0,40):
    ret += random.choice(string.printable)
  return ret

def show(val):
  hashcode = hash(val)
  # print hashcode
  exp = int(math.log(math.fabs(hashcode), 2))
  bits = int(exp)
  if bits != exp:
    bits += 1
  print '{hashcode:32} {bits:6} {val!r}'.format(**locals())

for iteration in range(100):
  show(random_string())
  show(random.randint(-2**31, 2**31-1))
