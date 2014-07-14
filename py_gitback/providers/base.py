#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class GitProvider(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(GitProvider, self).__init__(*args, **kwargs)

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @abc.abstractproperty
    def repos(self):
        raise NotImplementedError

# vim: filetype=python
