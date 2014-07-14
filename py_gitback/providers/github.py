#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import GitProvider
from github3 import login


class GitHubProvider(GitProvider):
    ProviderName = "GitHub"

    def __init__(self, username, password, *args, **kwargs):
        super(GitHubProvider, self).__init__(*args, **kwargs)
        self._username = username
        self._password = password
        self._client = login(self._username, self._password)

    @property
    def name(self):
        return self.ProviderName

    @property
    def repos(self):
        return [r.refresh() for r in self._client.iter_repos(self._username)]

# vim: filetype=python
