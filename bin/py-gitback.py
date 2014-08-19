#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging
import os

from py_gitback.utilities import get_abs_date_dir
from py_gitback.utilities import get_provider_from_config
from py_utilities.compression.tar_utilities import create_tarball
from py_utilities.fs.fs_utilities import mkdir_p

import subprocess
import sys
import traceback

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def init_argparser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--config', action='store',
                        help='template configuration data', required=True)
    parser.add_argument('-w', '--working', action='store',
                        help='working directory', required=True)
    parser.add_argument('-a', '--archive', action='store',
                        help='archive directory', required=True)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase chattiness of script')
    return parser


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
    config_path = os.path.join(cwd, '.py-gitback.config')
    provider = get_provider_from_config(config_path)

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

    bundle_file_to_create = os.path.join(bundle_dir_to_create,
                                         "{}.bundle".format(repo.name))

    subprocess.check_call(
        ["git",
         "clone",
         "--no-hardlinks",
         "--mirror",
         repo.clone_url,
         repo_dir_to_create])

    os.chdir(repo_dir_to_create)

    subprocess.check_call(
        ["git",
         "bundle",
         "create",
         bundle_file_to_create,
         "--all"])

    create_tarball([bundle_dir_to_create], repo.name, abs_date_dir)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = init_argparser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    try:
        backup(args)
    except:
        trace = traceback.format_exc()
        logging.error("OMGWTFBBQ: {0}".format(trace))
        sys.exit(1)

    # Yayyy-yah
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# vim: filetype=python
