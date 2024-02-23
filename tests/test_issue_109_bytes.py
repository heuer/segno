#
# Copyright (c) 2022 -2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #109.
<https://github.com/heuer/segno/issues/109>

Requires pyzbar and additional libs (libzbar0).
"""
import platform
import io
import pytest
import segno
try:
    from pyzbar.pyzbar import decode as zbardecode
except (ImportError, FileNotFoundError):  # The latter may occur under Windows
    pytestmark = pytest.mark.skip

_libc, _ = platform.libc_ver()

if _libc != 'glibc':  # Does not work with zbar/musl
    pytestmark = pytest.mark.skip


def decode(qrcode):
    scale = 3
    width, height = qrcode.symbol_size(scale=scale)
    out = io.BytesIO()
    for row in qrcode.matrix_iter(scale=scale):
        out.write(bytearray(0x0 if b else 0xff for b in row))
    decoded = zbardecode((out.getvalue(), width, height))
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
