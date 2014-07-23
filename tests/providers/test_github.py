#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from py_gitback.providers import GitHubProvider
import unittest


class TestGithubProvider(unittest.TestCase):

    def test_provider_name(self):
        provider = GitHubProvider("foo", "bar")
        ok_(provider.name == GitHubProvider.ProviderName)
        ok_(GitHubProvider.ProviderName == "GitHub")

# vim: filetype=python
