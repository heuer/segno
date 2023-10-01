# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against Segno data URI.
"""
from __future__ import absolute_import
import segno


def test_data_svg():
    qr = segno.make_qr('A')
    val = qr.svg_data_uri()
    assert val
    expected = "data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%27"
    assert expected == val[:len(expected)]
    assert val.endswith('%3C%2Fsvg%3E')


def test_data_svg_minimal_encoding():
    qr = segno.make_qr('A')
    val = qr.svg_data_uri(encode_minimal=True)
    assert val
    expected = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='"
    assert expected == val[:len(expected)]
    assert val.endswith('%3C/svg%3E')


def test_data_svg_no_charset():
    qr = segno.make_qr('A')
    val = qr.svg_data_uri(omit_charset=True)
    assert val
    expected = "data:image/svg+xml,%3Csvg%20xmlns%3D%27"
    assert expected == val[:len(expected)]
    assert val.endswith('%3C%2Fsvg%3E')


def test_data_png():
    qr = segno.make_qr('A')
    val = qr.png_data_uri()
    assert val
    assert val.startswith('data:image/png;base64,')


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
