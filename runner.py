#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import subprocess

from py_gitback.providers import get_provider
from py_gitback.providers import Provider

# get provider
# find config
# - command line
# - current directory
# - home directory
# get repos
# if workspace directory doesn't exist, create it either from config or current dir
# if archive directory doesn't exist, create it either from config or current dir
# clone repo to _workspace
# run git bundle with the timestamp, from config or current dir
# should be in archive/date/reponame-date (maybe no date), from config

def backup(repos_to_backup=None):
    cwd = os.getcwd()

    config = get_config(os.path.join(cwd, '.py-gitback.config'))
    username = config.get('GitHub', 'username')
    password = config.get('GitHub', 'password')
    provider = get_provider(Provider.GitHub, username=username, password=password)
    create_workspace(os.path.join(cwd, '_workspace'))
    create_archive(os.path.join(cwd, '_archive'))
    create_archive_ymd(os.path.join(cwd, '_archive'))

    repo = provider.repos[0]

    workspace_dir_to_create = os.path.join(cwd, '_workspace', repo.name)
    bundle_dir_to_create = os.path.join(cwd, '_archive', repo.name)

    create_dir(workspace_dir_to_create)
    create_dir(bundle_dir_to_create)

    bundle_file_to_create = os.path.join(bundle_dir_to_create, "{}.bundle".format(repo.name))

    subprocess.check_call(["git", "clone", "--no-hardlinks", "--mirror", repo.clone_url, workspace_dir_to_create])
    os.chdir(workspace_dir_to_create)
    subprocess.check_call(["git", "bundle", "create", bundle_file_to_create, "--all"])


def get_config(dir_path):
    config = ConfigParser.SafeConfigParser()
    config.read([dir_path])
    return config


create_workspace = lambda x: create_dir(x)
create_archive = lambda x: create_dir(x)


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def create_archive_ymd(archive_dir):
    import datetime
    today = datetime.datetime.now()
    today_path = today.strftime("%Y/%m/%d")

    archive_ymd_path = os.path.join(archive_dir, today_path)

    if not os.path.exists(archive_ymd_path):
        os.makedirs(archive_ymd_path)

backup()

# vim: filetype=python
