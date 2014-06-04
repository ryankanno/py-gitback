#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
import os
from py_gitback.utilities import ensure_dir
import shutil
import tempfile
import unittest


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.gettempdir()

    def tearDown(self):
        tmp_foo = os.path.join(self.temp_dir, 'foobar2')
        if os.path.exists(tmp_foo):
            shutil.rmtree(tmp_foo)

    def test_ensure_dir(self):
        tmp_foobar2 = os.path.join(self.temp_dir, 'foobar2')
        tmp_foobar3 = os.path.join(self.temp_dir, 'foobar2', 'foobar3')
        ensure_dir(tmp_foobar2)
        ok_(os.path.exists(tmp_foobar2))
        ok_(not os.path.exists(tmp_foobar3))

# vim: filetype=python
