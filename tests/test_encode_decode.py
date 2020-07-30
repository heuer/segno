# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test suite which decodes generated QR Codes.

Requires pyzbar and additional libs (libzbar0).
"""
from __future__ import absolute_import, unicode_literals
import io
import pytest
import segno
from segno.utils import matrix_iter
ZBAR_AVAILABLE = True
try:
    import pyzbar
    from pyzbar.pyzbar import decode as zbardecode
except ImportError:
    ZBAR_AVAILABLE = False
    pytestmark = pytest.mark.skip

if ZBAR_AVAILABLE:
    def qr_to_bytes(qrcode, scale):
        assert not qrcode.is_micro
        buff = io.BytesIO()
        for row in matrix_iter(qrcode.matrix, version=qrcode._version, scale=scale):
            buff.write(bytearray(0x0 if b else 0xff for b in row))
        return buff.getvalue()

    def decode(qrcode):
        scale = 3
        width, height = qrcode.symbol_size(scale=scale)
        qr_bytes = qr_to_bytes(qrcode, scale)
        decoded = zbardecode((qr_bytes, width, height))
        assert 1 == len(decoded)
        assert 'QRCODE' == decoded[0].type
        return decoded[0].data.decode('utf-8')


@pytest.mark.parametrize('content, mode',
                         [('漢字', 'kanji'),
                          ('続きを読む', 'kanji'),
                          ('Märchenbücher', 'byte'),
                          ('汉字', 'byte'),
                          ])
def test_encode_decode(content, mode):
    qr = segno.make_qr(content)
    assert mode == qr.mode
    assert content == decode(qr)


if __name__ == '__main__':
    pytest.main([__file__])
