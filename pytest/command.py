import pytest

@pytest.fixture(scope='session', autouse=True)
def fixer():
  print('Welcome to fixer!')
  print('Goodbye from fixer!')
  yield
  print('Back inside fixer!')

def test_command(host):
  print('hostname: ' + str(host.run('hostname')))
