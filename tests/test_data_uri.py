# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against Segno data URI.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
from nose.tools import ok_, eq_
import segno


def test_data_svg():
    qr = segno.make_qr('A')
    val = qr.svg_data_uri()
    ok_(val)
    expected = "data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%27"
    eq_(expected, val[:len(expected)])
    ok_(val.endswith('%3C%2Fsvg%3E'))


def test_data_svg_minimal_encoding():
    qr = segno.make_qr('A')
    val = qr.svg_data_uri(encode_minimal=True)
    ok_(val)
    expected = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='"
    eq_(expected, val[:len(expected)])
    ok_(val.endswith('%3C/svg%3E'))


def test_data_svg_no_charset():
    qr = segno.make_qr('A')
    val = qr.svg_data_uri(omit_charset=True)
    ok_(val)
    expected = "data:image/svg+xml,%3Csvg%20xmlns%3D%27"
    eq_(expected, val[:len(expected)])
    ok_(val.endswith('%3C%2Fsvg%3E'))


def test_data_png():
    qr = segno.make_qr('A')
    val = qr.png_data_uri()
    ok_(val)
    ok_(val.startswith('data:image/png;base64,'))


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.core.runmodule()
