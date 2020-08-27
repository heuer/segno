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
import re
from functools import partial
from itertools import chain
import shutil
import nox

nox.options.sessions = ['test-2.7', 'test-3.7', 'test-pypy', 'test-pypy3']
default_py = '3.7'


@nox.session(python=['2.7', '3.7', '3.8', 'pypy', 'pypy3'])
def test(session):
    """\
    Run test suite.
    """
    if session.python == 'pypy':
        # See <https://github.com/heuer/segno/issues/80>
        pip_ver = session.run('pip', '--version', silent=True)
        m = re.search(r'pip ([0-9.]+)', pip_ver)
        assert m
        if m.group(1) in ('20.2', '20.2.1', '20.2.2'):
            session.run('pip', 'uninstall', '-y', 'pip')
            session.run('easy_install', 'pip==20.1.1')
    session.install('-Ur', 'requirements-testing.txt')
    session.install('.')
    session.run('py.test')


@nox.session(python=default_py)
def docs(session):
    """\
    Build the documentation.
    """
    session.install('-Ur', 'requirements-rtd.txt')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'output'))
    shutil.rmtree(output_dir, ignore_errors=True)
    doctrees, html, man = map(partial(os.path.join, output_dir), ['doctrees', 'html', 'man'])
    session.install('.')
    session.cd('docs')
    sphinx_build = partial(session.run, 'sphinx-build', '-W', '-d', doctrees, '.')
    sphinx_build('-b', 'html', html)
    sphinx_build('-b', 'man', man)
    sys.path.insert(0, os.path.abspath('..'))
    import segno
    if 'dev' not in segno.__version__:
        shutil.copyfile(os.path.join(man, 'segno.1'),
                        os.path.abspath(os.path.join(os.path.dirname(__file__), 'man', 'segno.1')))
        session.log("'man/segno.1' has been modified, don't forget to commit")


@nox.session(python=default_py)
def coverage(session):
    """\
    Run coverage.
    """
    session.install('coverage', '-Ur', 'requirements-testing.txt')
    session.install('.')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'html'))
    cover = partial(session.run, 'coverage')
    cover('erase')
    cover('run', './tests/alltests.py')
    cover('report')
    cover('html', '-d', output_dir)


@nox.session(python=default_py)
def lint(session):
    """\
    Run flake8
    """
    session.install('flake8', 'mypy')
    session.run('mypy', 'segno')
    session.run('flake8', 'segno')


@nox.session(python=default_py)
def benchmarks(session):
    """\
    Run the benchmarks and create the charts.
    """
    session.install('qrcode', 'Pillow', 'pyqrcode', 'pypng', 'qrcodegen', 'pygal')
    session.install('.')
    sandbox_dir = os.path.join(os.path.dirname(__file__), 'sandbox')
    session.run('python', os.path.join(sandbox_dir, 'benchmarks.py'))
    session.run('python', os.path.join(sandbox_dir, 'make_charts.py'))


#
# Release related tasks
# 1. nox -e start-release -- version-number
# 2. run tests, update docs, update changes
# 3. nox -e finish-release -- version-number
# 4. git push / git push origin --tags
# 5. nox -e build-release -- version-number
# 6. nox -e upload-release
#


@nox.session(name='start-release', python=default_py)
def start_release(session):
    """\
    Prepares a release.

    * Creates a new branch release-VERSION_NUMBER
    * Changes the version number in segno.__version__ to VERSION_NUMBER
    """
    session.install('packaging')
    git = partial(session.run, 'git', external=True)
    git('checkout', 'master')
    prev_version = _get_current_version(session)
    version = _validate_version(session)
    valid_version = bool(int(session.run('python', '-c', 'from packaging.version import parse;'
                                                         'prev_version = parse("{0}");'
                                                         'next_version = parse("{1}");'
                                                         'print(1 if prev_version < next_version else 0)'
                                         .format(prev_version, version), silent=True)))
    if not valid_version:
        session.error('Invalid version')
    release_branch = 'release-{}'.format(version)
    git('checkout', '-b', release_branch, 'develop')
    _change_version(session, prev_version, version)
    git('add', 'segno/__init__.py')
    session.log('Now on branch "{}". Run the tests, run nox -e docs. Update CHANGES'.format(release_branch))
    session.log('When done, call nox -e finish-release -- {}'.format(version))


@nox.session(name='finish-release', python=default_py)
def finish_release(session):
    """\
    Finishes the release.

    * Merges the branch release-VERSION_NUMBER into master
    * Creates a tag VERSION_NUMBER
    * Increments the development version
    """
    version = _validate_version(session)
    release_branch = 'release-{}'.format(version)
    git = partial(session.run, 'git', external=True)
    git('checkout', 'master')
    git('merge', '--no-ff', release_branch, '-m', 'Merge release branch {}'.format(release_branch))
    git('tag', '-a', version, '-m', 'Release {}'.format(version))
    git('branch', '-d', release_branch)
    version_parts = version.split('.')
    patch = str(int(version_parts[2]) + 1)
    next_version = '.'.join(chain(version_parts[:2], patch)) + '.dev'
    _change_version(session, version, next_version)
    git('add', 'segno/__init__.py')
    git('commit', '-m', 'Incremented development version')
    session.log('Finished. Run git push / git push origin --tags and '
                'nox -e build-release -- {} / nox -e upload-release'.format(version))


@nox.session(name='build-release', python=default_py)
def build_release(session):
    """\
    Builds a release: Creates sdist and wheel
    """
    version = _validate_version(session)
    git = partial(session.run, 'git', external=True)
    git('fetch')
    git('fetch', '--tags')
    git('checkout', version)
    session.install('setuptools', 'wheel')
    shutil.rmtree('dist', ignore_errors=True)
    session.run('python', 'setup.py', 'sdist', 'bdist_wheel')
    git('checkout', 'master')


@nox.session(name='upload-release', python=default_py)
def upload_release(session):
    """\
    Uploads a release to PyPI
    """
    session.install('twine')
    twine = partial(session.run, 'twine')
    twine('check', 'dist/*')
    twine('upload', 'dist/*')


def _validate_version(session):
    if not session.posargs:
        session.error('No release version provided')
    elif len(session.posargs) > 1:
        session.error('Too many arguments')
    version = session.posargs[0]
    if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', version):
        session.error('Invalid version number: "{}"'.format(version))
    return version


def _get_current_version(session):
    """\
    Returns the current Segno version.
    """
    fn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'segno/__init__.py'))
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^__version__ = ["\']([^"\']+)["\']$', content, flags=re.MULTILINE)
    if m:
        return m.group(1)
    session.error('Cannot find any version information')


def _change_version(session, previous_version, next_version):
    """\
    Changes the segno.__init__.__version__ from previous_version to next_version.
    """
    fn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'segno/__init__.py'))
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(r'^(__version__ = ["\'])({0})(["\'])$'
                         .format(re.escape(previous_version)),
                         r'\g<1>{}\g<3>'.format(next_version), content,
                         flags=re.MULTILINE)
    if content != new_content:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return
    session.error('Cannot modify version. Provided: "{}" (previous) "{}" (next)'
                  .format(previous_version, next_version))
