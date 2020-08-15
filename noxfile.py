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
from itertools import chain
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
    sphinx_build = partial(session.run, 'sphinx-build', '-W', '-d', doctrees, '.')
    sphinx_build('-b', 'html', html)
    sphinx_build('-b', 'man', man)
    sys.path.insert(0, os.path.abspath('..'))
    import segno
    if 'dev' not in segno.__version__:
        shutil.copyfile(os.path.join(man, 'segno.1'),
                        os.path.abspath(os.path.join(os.path.dirname(__file__), 'man', 'segno.1')))
        session.log("'man/segno.1' has been modified, don't forget to commit")


@nox.session(python='3')
def coverage(session):
    """\
    Run coverage.
    """
    session.install('coverage', '-Ur', 'requirements.testing.txt')
    session.install('.')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'html'))
    cover = partial(session.run, 'coverage')
    cover('erase')
    cover('run', './tests/alltests.py')
    cover('report')
    cover('html', '-d', output_dir)


@nox.session(python='3')
def lint(session):
    """\
    Run flake8
    """
    session.install('flake8')
    session.run('flake8', 'segno')


#
# Release related tasks
# 1. nox -e start-release -- version-number
# 2. run tests, update docs, update changes
# 3. nox -e finish-release -- version-number
# 4. git push / git push origin --tags
# 5. nox -e upload-release -- version-number
#


@nox.session(name='start-release')
def start_release(session):
    """\
    Prepares a release.

    * Creates a new branch release-VERSION_NUMBER
    * Changes the version number in segno.__version__ to VERSION_NUMBER
    """
    version = _validate_version(session)
    release_branch = 'release-{}'.format(version)
    session.run('git', 'checkout', '-b', release_branch, 'develop', external=True)
    init_py = os.path.abspath(os.path.join(os.path.dirname(__file__), 'segno/__init__.py'))
    session.run('sed', '-i', "s/__version__ = '{0}.dev.'/__version__ = '{0}'/".format(version), init_py, external=True)
    session.log('Now on branch "{}". Run the tests, run nox -e docs. Update CHANGES'.format(release_branch))
    session.log('When done, call nox -e finish-release')


@nox.session(name='finish-release')
def finish_release(session):
    """\
    Finishes the release.

    * Merges the branch release-VERSION_NUMBER into master
    * Creates a tag VERSION_NUMBER
    * Increments the development version
    * Creates sdist and bdist_wheel
    """
    version = _validate_version(session)
    release_branch = 'release-{}'.format(version)
    session.install('setuptools', 'wheel')
    git = partial(session.run, 'git', external=True)
    git('checkout', 'master')
    git('merge', '--no-ff', release_branch, '-m', '"Merge release branch {}"'.format(release_branch))
    git('tag', '-a', version, '-m', '"Release {}"'.format(version))
    git('checkout', 'develop')
    git('merge', '--no-ff', release_branch, '-m', '"Merge release branch {}"'.format(release_branch))
    git('branch', '-d', release_branch)
    version_parts = version.split('.')
    patch = str(int(version_parts[2]) + 1)
    next_version = '.'.join(chain(version_parts[:2], patch)) + '.dev'
    init_py = os.path.abspath(os.path.join(os.path.dirname(__file__), 'segno/__init__.py'))
    session.run('sed', '-i', "s/__version__ = '{0}'/__version__ = '{1}'/".format(version, next_version), init_py, external=True)
    git('add', 'segno/__init__.py')
    git('commit', '-m', '"Incremented development version"')
    git('checkout', 'master')
    session.run('python', 'setup.py', 'sdist', 'bdist_wheel')
    session.log('Finished. Run git push / git push origin --tags and nox -e upload-release')


@nox.session(name='upload-release')
def upload_release(session):
    """\
    Uploads a release to PyPI
    """
    version = _validate_version(session)
    session.install('twine')
    twine = partial(session.run, 'twine')
    twine('check', 'dist/*')
    twine('upload', 'dist/*')


def _validate_version(session):
    if not session.posargs:
        session.error('No release version provided')
    elif len(session.posargs) > 1:
        session.error('Too many arguments')
    return session.posargs[0]
