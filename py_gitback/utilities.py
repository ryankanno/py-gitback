#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import os
import tarfile


def ensure_dir(dir):
    try:
        os.makedirs(dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise


def get_abs_date_dir(root_dir, date):
    return os.path.join(os.path.abspath(root_dir),
                        date.strftime("%Y/%m/%d"))


def tarball(tarball_filename, dir_to_tarball):
    with tarfile.open(tarball_filename, "w:gz") as tar:
        tar.add(dir_to_tarball, arcname=os.path.basename(dir_to_tarball))

# vim: filetype=python
