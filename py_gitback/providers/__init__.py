#!/usr/bin/env python
# -*- coding: utf-8 -*-

from github import GitHubProvider
from enum import Enum
from enum import unique


@unique
class Provider(Enum):
    Local = 1
    GitHub = 2


def get_provider(provider_enum, *args, **kwargs):
    assert provider_enum in list(Provider)
    return {
        Provider.GitHub: GitHubProvider
    }.get(provider_enum)(*args, **kwargs)

# vim: filetype=python
