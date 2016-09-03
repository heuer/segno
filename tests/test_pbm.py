# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
PBM related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import io
import pytest
import segno


def test_p4():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pbm')
    assert out.getvalue().startswith(b'P4')


def test_not_plain():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pbm', plain=False)
    assert out.getvalue().startswith(b'P4')


def test_p1():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pbm', plain=True)
    assert out.getvalue().startswith(b'P1')


if __name__ == '__main__':
    pytest.main([__file__])

