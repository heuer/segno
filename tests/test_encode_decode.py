#
# Copyright (c) 2020 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test suite which decodes generated QR Codes.

Requires pyzbar and additional libs (libzbar0).
"""
import io
import pytest
import segno
import platform
try:
    from pyzbar.pyzbar import decode as zbardecode
except (ImportError, FileNotFoundError):  # The latter may occur under Windows
    pytestmark = pytest.mark.skip

_libc, _ = platform.libc_ver()
IS_MUSL = _libc != 'glibc'


def decode(qrcode):
    if qrcode.is_micro:
        raise Exception('Cannot decode Micro QR codes')
    scale = 3
    width, height = qrcode.symbol_size(scale=scale)
    out = io.BytesIO()
    for row in qrcode.matrix_iter(scale=scale):
        out.write(bytearray(0x0 if b else 0xff for b in row))
    decoded = zbardecode((out.getvalue(), width, height))
    assert 1 == len(decoded)
    assert 'QRCODE' == decoded[0].type
    return decoded[0].data.decode('utf-8')


@pytest.mark.parametrize('content, mode',
                         [('漢字', 'kanji'),
                          ('続きを読む', 'kanji'),
                          ('汉字', 'byte'),
                          ])
def test_encode_decode(content, mode):
    qr = segno.make_qr(content)
    assert mode == qr.mode
    assert content == decode(qr)


@pytest.mark.skipif(IS_MUSL, reason="zbar does not support latin1 with musl")
def test_encode_decode_latin1():  # See <https://github.com/heuer/segno/issues/134>
    content = 'Märchenbücher'
    qr = segno.make_qr(content)
    assert 'byte' == qr.mode
    assert content == decode(qr)


def test_stackoverflow_issue():
    # See <https://stackoverflow.com/questions/63303624/generating-and-reading-qr-codes-with-special-characters>
    # and <https://github.com/NaturalHistoryMuseum/pyzbar/issues/14>
    content = 'Thomsôn Gonçalves Ámaral,325.432.123-21'
    qr = segno.make(content, encoding='utf-8')
    assert 'byte' == qr.mode
    decoded = decode(qr).encode('shift-jis').decode('utf-8')
    assert content == decoded


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
