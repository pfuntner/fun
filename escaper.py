#! /usr/bin/env python3

import re

def escaper(s):
  pos = 0
  while pos < len(s):
    if s[pos+1:pos+3] == '\\n' and s[pos:pos+3] != '\\\\n':
      s = s[:pos+1] + '\n' + s[pos+3:]
    pos += 1
  return s

def doit(s):
  print('{s1!r}\t{s2!r}'.format(s1=s, s2=escaper(s)))

doit('abc\nxyz')
doit('abc\\nxyz')
doit('abc\\\\nxyz')
