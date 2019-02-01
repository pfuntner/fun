#! /usr/bin/python

import os

print os.sysconf(os.sysconf_names["SC_CLK_TCK"])
