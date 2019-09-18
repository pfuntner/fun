#! /usr/bin/python2

import os

print os.sysconf(os.sysconf_names["SC_CLK_TCK"])
