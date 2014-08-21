#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging
import os

from py_gitback.utilities import get_abs_date_dir
from py_gitback.utilities import get_provider_from_config
from py_gitback.utilities import get_repo_objs_from_provider
from py_utilities.compression.tar_utilities import create_tarball
from py_utilities.fs.fs_utilities import mkdir_p

import subprocess
import sys
import traceback

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def init_argparser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-c', '--config', action='store',
                        help='backup config file',
                        default=os.path.join(os.getcwd(), '.py-gitback.conf'))
    parser.add_argument('-s', '--staging', action='store', dest='staging_dir',
                        help='staging directory',
                        default=os.path.join(os.getcwd(), '_staging'))
    parser.add_argument('-a', '--archive', action='store', dest='archive_dir',
                        help='archive directory',
                        default=os.path.join(os.getcwd(), '_archive'))
    parser.add_argument('-r', '--repo', action='append',
                        dest='repos',
                        help='repo to backup',
                        default=[])
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase chattiness of script')
    return parser


def backup(args):

    if args.repos:

        provider = get_provider_from_config(args.config)

        today = datetime.datetime.now().date()
        abs_date_dir = get_abs_date_dir(args.archive_dir, today)

        mkdir_p(args.staging_dir)
        mkdir_p(args.archive_dir)
        mkdir_p(abs_date_dir)

        repo_objs = get_repo_objs_from_provider(provider, args.repos)

        if repo_objs:
            for repo in repo_objs:
                repo_dir_to_create = os.path.join(args.staging_dir, repo.name)
                bundle_dir_to_create = os.path.join(abs_date_dir, repo.name)

                mkdir_p(repo_dir_to_create)
                mkdir_p(bundle_dir_to_create)

                bundle_file_to_create = os.path.join(
                    bundle_dir_to_create, "{}.bundle".format(repo.name))

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
    else:
        logging.error("Please provide repos to backup.")


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
