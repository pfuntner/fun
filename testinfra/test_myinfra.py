"""
https://pytest.org/en/latest/
https://testinfra.readthedocs.io/en/latest/

Example:

  $ pytest test_myinfra.py | fitwidth
  ============================= test session starts ==============================
  platform linux2 -- Python 2.7.5, pytest-4.6.5, py-1.8.0, pluggy-0.12.0
  rootdir: /home/centos/repos/fun/testinfra
  plugins: testinfra-3.1.0
  collected 3 items
  
  test_myinfra.py .FF                                                      [100%]
  
  =================================== FAILURES ===================================
  ________________________ test_nginx_is_installed[local] ________________________
  
  host = <testinfra.host.Host object at 0x7ff03c4b8990>
  
      def test_nginx_is_installed(host):
          print 'type(host): {}'.format(type(host))
          print 'hostname: {}'.format(host.run('hostname'))
          hosts = host.file('/etc/ansible/hosts')
          print '/dev/null: {}'.format(hosts)
          print '/dev/null owner: {}'.format(hosts.user)
          print '/dev/null uid: {}'.format(hosts.uid)
          print '/dev/null content: {!r}'.format(hosts.content)
          nginx = host.package("nginx")
  >       assert nginx.is_installed
  E       assert False
  E        +  where False = <package nginx>.is_installed
  
  test_myinfra.py:26: AssertionError
  ----------------------------- Captured stdout call -----------------------------
  type(host): <class 'testinfra.host.Host'>
  hostname: CommandResult(command='hostname', exit_status=0, stdout='pfuntner1.cisco.com\n', stderr=None)
  /dev/null: <file /etc/ansible/hosts>
  /dev/null owner: root
  /dev/null uid: 0
  /dev/null content: "# This is the default ansible 'hosts' file.\n#\n# It sho ... r=ec2-user ansible_ssh_private_key_file=/home/centos/sto/pfuntner-aws.pem\n"
  ____________________ test_nginx_running_and_enabled[local] _____________________
  
  host = <testinfra.host.Host object at 0x7ff03c4b8990>
  
      def test_nginx_running_and_enabled(host):
          nginx = host.service("nginx")
  >       assert nginx.is_running
  E       assert False
  E        +  where False = <service nginx>.is_running
  
  test_myinfra.py:32: AssertionError
  ====================== 2 failed, 1 passed in 0.14 seconds ======================
  $

  
"""

def mountpoint_dev(host, path):
  return host.mount_point(path).device if host.mount_point(path).exists else None

def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644


def test_nginx_is_installed(host):
    print 'type(host): {}'.format(type(host))
    print 'hostname: {}'.format(host.run('hostname'))
    info = host.system_info
    for attr in dir(info):
      if '_' not in attr:
        print 'info.{attr}: {value}'.format(attr=attr, value=getattr(info, attr))

    hosts = host.file('/etc/ansible/hosts')
    print '/dev/null: {}'.format(hosts)
    print '/dev/null owner: {}'.format(hosts.user)
    print '/dev/null uid: {}'.format(hosts.uid)
    print '/dev/null content: {!r}'.format(hosts.content)

    print 'mount_point("/"): {!r}'.format(mountpoint_dev(host, "/"))
    print 'mount_point("/etc"): {!r}'.format(mountpoint_dev(host, "/etc"))

    nginx = host.package("nginx")
    assert nginx.is_installed
    assert nginx.version.startswith("1.2")


def test_nginx_running_and_enabled(host):
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled
