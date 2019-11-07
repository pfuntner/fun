"""
$ pytest -s foo.py

  ==================================================================== test session starts ====================================================================
  platform cygwin -- Python 2.7.16, pytest-4.6.5, py-1.8.0, pluggy-0.12.0
  rootdir: /home/jpfuntne/repos/fun/testinfra
  plugins: testinfra-3.1.0
  collected 1 item
  
  foo.py hostname: CommandResult(command='hostname', exit_status=0, stdout='JPFUNTNE-GCEYJ\n', stderr=None)
  .
  
  ================================================================= 1 passed in 0.21 seconds ==================================================================
$ ansiblehost runon
{'ansible_ssh_private_key_file': 'c:/sto/pfuntner-runon.pem', 'ansible_host': '64.102.179.79', 'ansible_user': 'centos'}
$ pytest -s foo.py --hosts=centos@64.102.179.79 --ssh-identity-file=c:/sto/pfuntner-runon.pem

"""

def test_foo(host):
  print 'hostname: {}'.format(host.run('hostname'))
