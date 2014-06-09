#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = []

here = os.path.dirname(os.path.realpath(__file__))

# Metadata

meta = {}
re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_version = re.compile(r'VERSION\s*=.*?\((.*?)\)')
strip_quotes = lambda s: s.strip("\"'")


def add_version(match):
    return {'VERSION': match.group(1).replace(" ", "").replace(",", ".")}


def add_meta(match):
    attr_name, attr_value = m.groups()
    return {attr_name: strip_quotes(attr_value)}


patterns = {
    re_meta: add_meta,
    re_version: add_version
}


with open(os.path.join(here, 'py_gitback/__init__.py'), 'r') as f:
    for line in f:
        for pattern, handler in patterns.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))

# Requires

requires = ['github3.py', 'enum34', 'py-utilities==0.0.2']
tests_require = ['flake8', 'mock', 'nose', 'nosexcover']

with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(here, 'CHANGES')) as f:
    changes = f.read()

classifiers = [
]

setup(
    name='py-gitback',
    version=meta['VERSION'],
    description='',
    long_description=readme + '\n\n' + changes,
    author=meta['author'],
    author_email=meta['email'],
    url="",
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'py_gitback': 'py_gitback'},
    install_requires=requires,
    license=meta['license'],
    tests_require=tests_require,
    classifiers=classifiers,
)

# vim: filetype=python
