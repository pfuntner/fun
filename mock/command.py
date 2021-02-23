import os
import subprocess

def exec():
  print(os.getpid())
  p = subprocess.Popen(['true'])
  rc = p.wait()
  return rc
