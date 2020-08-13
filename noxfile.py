# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Nox test runner configuration.
"""
import os
from functools import partial
import shutil
import nox


@nox.session(python="3")
def docs(session):
    """\
    Build the documentation.
    """
    session.install('-Ur', 'requirements.rtd')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'output'))
    doctrees, html, man = map(partial(os.path.join, output_dir), ['doctrees', 'html', 'man'])
    shutil.rmtree(output_dir, ignore_errors=True)
    session.install('.')
    session.cd('docs')
    session.run('sphinx-build', '-W', '-b', 'html', '-d', doctrees, '.', html)
    session.run('sphinx-build', '-W', '-b', 'man', '-d', doctrees, '.', man)


@nox.session(python='3')
def coverage(session):
    """\
    Run coverage.
    """
    session.install('coverage', '-Ur', 'requirements.testing.txt')
    session.install('.')
    session.run('coverage', 'erase')
    session.run('coverage', 'run', './tests/alltests.py')
    session.run('coverage', 'report', '--include=segno*')
    session.run('coverage', 'html', '--include=segno*')


@nox.session(python=['2.7', '3.7', 'pypy', 'pypy3'])
def test(session):
    """\
    Run test suite.
    """
    if session.python == 'pypy':
        # See <https://github.com/heuer/segno/issues/80>
        session.run('pip', 'uninstall', '-y', 'pip')
        session.run('easy_install', 'pip==20.1')
    session.install('-Ur', 'requirements.testing.txt')
    session.install('.')
    session.run('py.test')
