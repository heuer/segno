# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue <https://github.com/pyqrcode/pyqrcodeNG/pull/13/>
"""
from __future__ import absolute_import, unicode_literals
import segno


def test_autodetect():
    data = 'Émetteur'
    qr = segno.make(data)
    assert qr.mode == 'byte'


def test_force_byte():
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00:~\x9bU\x00\x00\x00\nIDAT\x08[c\xf8\x0f\x00\x01\x01\x01\x00\x9b\xd7\x1d\r\x00\x00\x00\x00IEND\xaeB`\x82'
    qr = segno.make(data)
    assert qr.mode == 'byte'


def test_encoding():
    encoding = 'iso-8859-15'
    data = 'Émetteur'.encode(encoding)
    qr = segno.make(data)
    assert qr.mode == 'byte'
    data2 = 'Émetteur'
    qr2 = segno.make(data2, encoding=encoding)
    assert qr2 == qr


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
