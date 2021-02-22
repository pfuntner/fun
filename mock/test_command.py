import unittest
import command

class mocked_subprocess(object):
  def __init__(self, *args):
    pass

  def wait(self):
    return 42

@unittest.mock.patch('command.subprocess')
def test_command(mock_command_subprocess):
  mock_command_subprocess.Popen = mocked_subprocess
  result = command.exec()
  print(f'result = {result}')
  assert result == 42
