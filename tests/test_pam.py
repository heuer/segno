# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
PAM related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import re
import io
import pytest
import segno
try:
    range = xrange
except NameError:
    pass


def test_invalid_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='pam', color=None)


def test_bw():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam')
    assert b'BLACKANDWHITE' in out.getvalue()


def test_grayscale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam', background=None)
    assert b'GRAYSCALE_ALPHA' in out.getvalue()


def test_rgb():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam', color='red')
    assert b'RGB' in out.getvalue()
    assert b'RGB_ALPHA' not in out.getvalue()


def test_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam', color='red', background=None)
    assert b'RGB' in out.getvalue()
    assert b'RGB_ALPHA' in out.getvalue()


if __name__ == '__main__':
    pytest.main([__file__])
