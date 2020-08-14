#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Setup script.
"""
from __future__ import unicode_literals
from setuptools import setup
import os
import io
import re


def read(*filenames, **kwargs):
    base_path = os.path.dirname(os.path.realpath(__file__))
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(os.path.join(base_path, filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


version = re.search(r'''^__version__ = ["']([^'"]+)['"]''',
                    read('segno/__init__.py'), flags=re.MULTILINE).group(1)

setup(
    version=version,
    long_description=read('README.rst', 'CHANGES.rst'),
)
