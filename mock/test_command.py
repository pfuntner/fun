import unittest
import command

class mocked_Popen(object):
  def __init__(self, *args):
    pass

  def wait(self):
    return 42

def mocked_getpid():
  return -42

@unittest.mock.patch('command.os')
@unittest.mock.patch('command.subprocess')
def test_command(mock_command_subprocess, mock_command_os):
  mock_command_subprocess.Popen = mocked_Popen
  mock_command_os.getpid = mocked_getpid

  result = command.exec()
  print(f'result = {result}')
  assert result == 42
