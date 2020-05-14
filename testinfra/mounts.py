import re

"""
$ pytest -s mounts.py --hosts=target
"""

def test_mounts(host):
  try:
    print("factor()['partitions']: {}".format(host.facter()['partitions']))
    return
  except Exception as e:
    print('Caught during `host.facter()`: {!r}'.format(str(e)))

  try:
    mount_items = host.mount_point.get_mountpoints()
    for mount_item in mount_items:
      print('mount_item: {} at {}'.format(mount_item.device, mount_item.path))

    dev_mount_items = [item.device for item in mount_items if re.match(r'/dev/(sd|vd|xvd).*', item.device)] or [item.device for item in mount_items if item.device == '/dev/root']
    print("get_mountpoints(): {}".format(list(set(dev_mount_items))))
    return
  except Exception as e:
    print('Caught during `host.facter()`: {!r}'.format(str(e)))
