#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the ``writers`` module.
"""
import os
import io
import tempfile
import pytest
import segno
from segno import consts, writers


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


def test_colormap_dark_light():
    qr = segno.make('123', version=7)
    width, height = len(qr.matrix[0]), len(qr.matrix)
    cm = writers._make_colormap(width, height, dark='blue', light='white')
    assert 15 == len(cm)


def test_colormap_lesser_version_7():
    qr = segno.make('123', version=6)
    width, height = len(qr.matrix[0]), len(qr.matrix)
    cm = writers._make_colormap(width, height, dark='blue', light='white')
    assert 13 == len(cm)
    assert consts.TYPE_VERSION_DARK not in cm
    assert consts.TYPE_VERSION_LIGHT not in cm


def test_colormap_micro():
    qr = segno.make_micro('123')
    width, height = len(qr.matrix[0]), len(qr.matrix)
    cm = writers._make_colormap(width, height, dark='blue', light='white')
    assert 10 == len(cm)
    assert consts.TYPE_VERSION_DARK not in cm
    assert consts.TYPE_VERSION_LIGHT not in cm
    assert consts.TYPE_ALIGNMENT_PATTERN_DARK not in cm
    assert consts.TYPE_ALIGNMENT_PATTERN_LIGHT not in cm
    assert consts.TYPE_DARKMODULE not in cm


if __name__ == '__main__':
    pytest.main([__file__])
