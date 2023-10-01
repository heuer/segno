# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 - 2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #105.
<https://github.com/heuer/segno/issues/105>

Requires pyzbar and additional libs (libzbar0).
"""
from __future__ import absolute_import, unicode_literals
import io
import pytest
from segno.helpers import make_epc_qr
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


@pytest.mark.parametrize('text', ['/',
                                  'Heiz-/Nebenkosten'])
def test_epc_slash(text):
    name = "This is a Test"
    iban = 'FR1420041010050500013M02606'
    amount = 111.7
    kw = dict(name=name, iban=iban, text=text, amount=amount)
    qr_code = make_epc_qr(**kw)
    assert qr_code
    decoded = decode(qr_code)
    assert text in decoded


if __name__ == '__main__':
    pytest.main([__file__])
