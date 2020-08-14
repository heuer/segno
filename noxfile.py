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
import sys
from functools import partial
import shutil
import nox

nox.options.sessions = ['test-2.7', 'test-3.7', 'test-pypy', 'test-pypy3']


@nox.session(python=['2.7', '3.7', '3.8', 'pypy', 'pypy3'])
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


@nox.session(python='3')
def docs(session):
    """\
    Build the documentation.
    """
    session.install('-Ur', 'requirements.rtd')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'output'))
    shutil.rmtree(output_dir, ignore_errors=True)
    doctrees, html, man = map(partial(os.path.join, output_dir), ['doctrees', 'html', 'man'])
    session.install('.')
    session.cd('docs')
    session.run('sphinx-build', '-W', '-b', 'html', '-d', doctrees, '.', html)
    session.run('sphinx-build', '-W', '-b', 'man', '-d', doctrees, '.', man)
    sys.path.insert(0, os.path.abspath('..'))
    import segno
    if 'dev' not in segno.__version__:
        shutil.copyfile(os.path.join(man, 'segno.1'),
                        os.path.abspath(os.path.join(os.path.dirname(__file__), 'man', 'segno.1')))


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


@nox.session(python='3')
def lint(session):
    """\
    Run flake8
    """
    session.install('flake8')
    session.run('flake8', 'segno')
