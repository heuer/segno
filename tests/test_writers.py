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
import pytest
from segno import writers


def test_get_writable_stream():
    buff = io.BytesIO()
    writable, must_close = writers.get_writable(buff, 'wb')
    assert buff == writable
    assert not must_close


def test_get_writable_stream2():
    buff = io.StringIO()
    writable, must_close = writers.get_writable(buff, 'wt')
    assert buff == writable
    assert not must_close


def test_get_writable_not_stream():
    fn = tempfile.NamedTemporaryFile()
    name = fn.name
    fn.close()
    writable, must_close = writers.get_writable(name, 'wb')
    try:
        assert name == writable.name
        writable.write(b'Segno')
        assert must_close
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
        assert name == writable.name
        writable.write('Segno')
        assert must_close
    finally:
        try:
            writable.close()
        except:
            pass
        os.remove(name)


def test_valid_scale():

    def check(scale):
        assert writers.check_valid_scale(scale) is None

    for i in (1, 1.2, .8, 10):
        yield check, i


def test_invalid_scale():

    def check(scale):
        with pytest.raises(ValueError):
            writers.check_valid_scale(scale)

    for scale in (0.0, 0, -1, -.2, int(.8)):
        yield check, scale


def test_valid_border():

    def check(border):
        assert writers.check_valid_border(border) is None

    for i in (None, 0, 0.0, 1, 2):
        yield check, i


def test_invalid_border():

    def check(border):
        with pytest.raises(ValueError):
            writers.check_valid_border(border)

    for border in (.2, -1, 1.3):
        yield check, border


if __name__ == '__main__':
    pytest.main(['-x', __file__])
