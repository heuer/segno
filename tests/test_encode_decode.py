# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 - 2023 -- Lars Heuer
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


def test_stackoverflow_issue():
    # See <https://stackoverflow.com/questions/63303624/generating-and-reading-qr-codes-with-special-characters>
    # and <https://github.com/NaturalHistoryMuseum/pyzbar/issues/14>
    content = 'Thomsôn Gonçalves Ámaral,325.432.123-21'
    qr = segno.make(content, encoding='utf-8')
    assert 'byte' == qr.mode
    assert content == decode(qr).encode('shift-jis').decode('utf-8')


def test_pyqrcode_issue76():
    # See <https://github.com/mnooner256/pyqrcode/issues/76>
    content = 'АБВГД'
    qr = segno.make(content, micro=False)
    assert 'kanji' == qr.mode
    assert content == decode(qr)
    qr = segno.make(content, encoding='utf-8', micro=False)
    assert 'byte' == qr.mode
    assert content == decode(qr)
    qr = segno.make(content.encode('utf-8'), micro=False)
    assert 'byte' == qr.mode
    assert content == decode(qr)


if __name__ == '__main__':
    pytest.main([__file__])
