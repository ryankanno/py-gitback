#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def ensure_dir(dir):
    try:
        os.makedirs(dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

# vim: filetype=python
