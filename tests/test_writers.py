# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the ``writers`` module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import os
import io
import tempfile
from nose.tools import ok_, eq_, raises
from segno import writers


def test_get_writable_stream():
    buff = io.BytesIO()
    writable, must_close = writers.get_writable(buff, 'wb')
    eq_(buff, writable)
    ok_(not must_close)


def test_get_writable_stream2():
    buff = io.StringIO()
    writable, must_close = writers.get_writable(buff, 'wt')
    eq_(buff, writable)
    ok_(not must_close)


def test_get_writable_not_stream():
    fn = tempfile.NamedTemporaryFile()
    name = fn.name
    fn.close()
    writable, must_close = writers.get_writable(name, 'wb')
    try:
        eq_(name, writable.name)
        writable.write(b'Segno')
        ok_(must_close)
    finally:
        try:
            writable.close()
        except:
            pass
        os.remove(name)


def test_get_writable_not_stream2():
    fn = tempfile.NamedTemporaryFile()
    name = fn.name
    fn.close()
    writable, must_close = writers.get_writable(name, 'wt')
    try:
        eq_(name, writable.name)
        writable.write('Segno')
        ok_(must_close)
    finally:
        try:
            writable.close()
        except:
            pass
        os.remove(name)


def test_valid_scale():

    def check(scale):
        ok_(writers.check_valid_scale(scale) is None)

    for i in (1, 1.2, .8, 10):
        yield check, i


def test_invalid_scale():

    @raises(ValueError)
    def check(scale):
        writers.check_valid_scale(scale)

    for scale in (0.0, 0, -1, -.2, int(.8)):
        yield check, scale


def test_valid_border():

    def check(border):
        ok_(writers.check_valid_border(border) is None)

    for i in (None, 0, 0.0, 1, 2):
        yield check, i


def test_invalid_border():

    @raises(ValueError)
    def check(border):
        writers.check_valid_border(border)

    for border in (.2, -1, 1.3):
        yield check, border


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
