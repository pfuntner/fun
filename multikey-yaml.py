#! /usr/bin/env python2

import yaml
import json

txt = """snmp:
  nms-server:
    0.0.0.0:
      community: public
    0.0.0.0:
      user:
        name: test
        auth-protocol: md0
        auth-key: admin0
        priv-protocol: cbc-des
        priv-key: admin0
  agent:
    community: public"""

data = yaml.load(txt)
print json.dumps(data, indent=2, sort_keys=True)
