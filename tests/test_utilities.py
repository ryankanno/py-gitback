#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import NoSectionError
import datetime
from nose.tools import ok_
from nose.tools import raises
import os
from py_gitback.providers import GitHubProvider
from py_gitback.utilities import get_abs_date_dir
from py_gitback.utilities import get_config
from py_gitback.utilities import get_provider_from_config
import shutil
import tempfile
import unittest


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.gettempdir()
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.config_file = os.path.join(self.cwd, '.', 'data', 'foo.config')

    def tearDown(self):
        tmp_foo = os.path.join(self.temp_dir, 'foobar2')
        if os.path.exists(tmp_foo):
            shutil.rmtree(tmp_foo)

    def test_get_config_with_valid_config_returns_valid_data(self):
        print self.config_file
        print os.path.exists(self.config_file)
        config = get_config(self.config_file)
        ok_(config.get('Default', 'Foo') == 'Bar')

    @raises(NoSectionError)
    def test_get_config_with_invalid_config_raises_error(self):
        bad_config_file = os.path.join(self.cwd, '.', 'data', 'foo.configadsf')
        config = get_config(bad_config_file)
        config.get('Default', 'Foo')

    def test_get_abs_date_dir(self):
        date = datetime.date(2012, 1, 11)
        tmp_ensure_date_dir = os.path.join(self.temp_dir, 'ensure_date')
        abs_date_dir = get_abs_date_dir(tmp_ensure_date_dir, date)
        ok_('ensure_date/2012/01/11' in abs_date_dir)

    def test_get_provider_from_config(self):
        config_file = os.path.join(self.cwd, '.', 'data', 'py-gitback.config')
        provider = get_provider_from_config(config_file)
        ok_(provider.name == GitHubProvider.ProviderName)
        ok_(GitHubProvider.ProviderName == "GitHub")
        ok_(provider._username == "foo")
        ok_(provider._password == "bar")


# vim: filetype=python
