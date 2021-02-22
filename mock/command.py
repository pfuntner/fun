import subprocess

def exec():
  p = subprocess.Popen(['true'])
  rc = p.wait()
  return rc
