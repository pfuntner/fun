"""
     A simple unit test class.  To run:

       1) `cd toys/test`
       2) `python -m unittest test1`
"""

import re
import os
import logging

from unittest import TestCase
import random

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

class Tests(TestCase):
  def __init__(self, *args, **vargs):
    # print 'args = {args}, vargs = {vargs}'.format(**locals())
    super(Tests, self).__init__(*args, **vargs)
    # print 'dir: {} '.format(dir(self))
    # print 'os: {}'.format(os.environ)
    log.setLevel(int(os.environ.get('LOG_LEVEL') or '30'))

  def test1(self):
    """
    This test randomly succeeds or fails
    :return: None
    """

    log.info('This is a test')
    self.assertTrue((random.randint(0,9) % 2) == 0)#! /usr/bin/env python

