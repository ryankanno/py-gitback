#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime
import os
import subprocess

from py_gitback.providers import get_provider
from py_gitback.providers import Provider
from py_gitback.utilities import get_abs_date_dir
from py_utilities.compression.tar_utilities import create_tarball
from py_utilities.fs.fs_utilities import mkdir_p


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

    workspace_dir = os.path.join(cwd, '_workspace')
    archive_dir = os.path.join(cwd, '_archive')

    today = datetime.datetime.now().date()
    abs_date_dir = get_abs_date_dir(archive_dir, today)

    mkdir_p(workspace_dir)
    mkdir_p(archive_dir)
    mkdir_p(abs_date_dir)

    repo = provider.repos[0]

    repo_dir_to_create = os.path.join(workspace_dir, repo.name)
    bundle_dir_to_create = os.path.join(abs_date_dir, repo.name)

    mkdir_p(repo_dir_to_create)
    mkdir_p(bundle_dir_to_create)

    bundle_file_to_create = os.path.join(bundle_dir_to_create, "{}.bundle".format(repo.name))

    subprocess.check_call(["git", "clone", "--no-hardlinks", "--mirror", repo.clone_url, repo_dir_to_create])
    os.chdir(repo_dir_to_create)
    subprocess.check_call(["git", "bundle", "create", bundle_file_to_create, "--all"])

    create_tarball([bundle_dir_to_create], repo.name, abs_date_dir)


def get_config(dir_path):
    config = ConfigParser.SafeConfigParser()
    config.read([dir_path])
    return config

# backup()

# vim: filetype=python
