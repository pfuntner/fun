#! /usr/bin/env python2

import sys
import subprocess

p = subprocess.Popen(sys.argv[1:])
print 'PID {pid}'.format(pid=p.pid)
