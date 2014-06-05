#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from nose.tools import ok_
import os
from py_gitback.utilities import ensure_dir
from py_gitback.utilities import get_abs_date_dir
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

    def test_get_abs_date_dir(self):
        date = datetime.date(2012, 1, 11)
        tmp_ensure_date_dir = os.path.join(self.temp_dir, 'ensure_date')
        abs_date_dir = get_abs_date_dir(tmp_ensure_date_dir, date)
        ok_('ensure_date/2012/01/11' in abs_date_dir)

# vim: filetype=python
