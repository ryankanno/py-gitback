#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def get_abs_date_dir(root_dir, date):
    return os.path.join(os.path.abspath(root_dir),
                        date.strftime("%Y/%m/%d"))

# vim: filetype=python
