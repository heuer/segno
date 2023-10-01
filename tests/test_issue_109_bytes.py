# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 -2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #109.
<https://github.com/heuer/segno/issues/109>

Requires pyzbar and additional libs (libzbar0).
"""
from __future__ import absolute_import, unicode_literals
import io
import pytest
import segno
try:
    FileNotFoundError
except NameError:  # Py2
    FileNotFoundError = OSError
try:
    from pyzbar.pyzbar import decode as zbardecode
except (ImportError, FileNotFoundError):  # The latter may occur under Windows
    pytestmark = pytest.mark.skip


def qr_to_bytes(qrcode, scale):
    if qrcode.is_micro:
        raise Exception('zbar cannot decode Micro QR codes')
    buff = io.BytesIO()
    for row in qrcode.matrix_iter(scale=scale):
        buff.write(bytearray(0x0 if b else 0xff for b in row))
    return buff.getvalue()


def decode(qrcode):
    scale = 3
    width, height = qrcode.symbol_size(scale=scale)
    qr_bytes = qr_to_bytes(qrcode, scale)
    decoded = zbardecode((qr_bytes, width, height))
    assert 1 == len(decoded)
    assert 'QRCODE' == decoded[0].type
    return decoded[0].data.decode('utf-8').encode('cp932')


def test_issue_109_bytes():
    data = b'\xb8\xd6\x90\xaf'
    qr_code = segno.make(data, micro=False, mode='byte')
    assert qr_code
    decoded = decode(qr_code)
    assert data == decoded


def test_issue_109_bytes_auto():
    data = b'\xb8\xd6\x90\xaf'
    qr_code = segno.make(data, micro=False)
    assert qr_code
    decoded = decode(qr_code)
    assert data == decoded


if __name__ == '__main__':
    pytest.main([__file__])
