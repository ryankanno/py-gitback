#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
from .providers import get_provider
from .providers import Provider


def get_abs_date_dir(root_dir, date):
    return os.path.join(os.path.abspath(root_dir),
                        date.strftime("%Y/%m/%d"))


def get_config(config_path):
    config = ConfigParser.SafeConfigParser()
    config.read([config_path])
    return config


def get_provider_from_config(config_path):
    config = get_config(config_path)
    username = config.get('GitHub', 'username')
    password = config.get('GitHub', 'password')
    return get_provider(Provider.GitHub, username=username, password=password)


def get_repo_objs_from_provider(provider, repos):
    repo_objs = []
    for repo in provider.repos:
        if repo.name.lower() in repos:
            repo_objs.append(repo)
    return repo_objs

# vim: filetype=python
