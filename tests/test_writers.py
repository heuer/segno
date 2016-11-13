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


def test_writable_stream():
    buff = io.BytesIO()
    with writers.writable(buff, 'wb') as f:
        f.write(b'x')
    assert not buff.closed


def test_writable_stream2():
    buff = io.StringIO()
    with writers.writable(buff, 'wt') as f:
        f.write('x')
    assert not buff.closed


def test_writable_stream3():
    buff = io.StringIO()
    with pytest.raises(Exception):
        with writers.writable(buff, 'wt') as f:
            f.write('x')
            raise Exception()
    assert not f.closed


def test_writable_not_stream():
    fn = tempfile.NamedTemporaryFile()
    name = fn.name
    fn.close()
    try:
        with writers.writable(name, 'wb') as f:
            assert name == f.name
            f.write(b'Segno')
    finally:
        os.remove(name)


def test_writable_not_stream2():
    fn = tempfile.NamedTemporaryFile()
    name = fn.name
    fn.close()
    try:
        with writers.writable(name, 'wt') as f:
            assert name == f.name
            f.write('Segno')
    finally:
        os.remove(name)


def test_writable_not_stream3():
    fn = tempfile.NamedTemporaryFile()
    name = fn.name
    fn.close()
    with pytest.raises(Exception):
        with writers.writable(name, 'wb') as f:
            assert name == f.name
            f.write(b'Segno')
            raise Exception()
    assert f.closed


if __name__ == '__main__':
    pytest.main([__file__])
