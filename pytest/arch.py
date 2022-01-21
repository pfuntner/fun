def test_arch(host):
  # print(f'{host.run("hostname").stdout.strip()}: host.system_info.arch: {host.system_info.arch}')
  print(f'{host.backend.get_hostname()}: host.system_info.arch: {host.system_info.arch}')
