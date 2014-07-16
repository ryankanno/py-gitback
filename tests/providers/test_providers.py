#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from py_gitback.providers import Provider
import unittest


class TestProviders(unittest.TestCase):

    def test_provider_enum(self):
        ok_(len(list(Provider)) == 2)
        ok_(Provider.Local in list(Provider))
        ok_(Provider.GitHub in list(Provider))

# vim: filetype=python
