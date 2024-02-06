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
import io
import pytest
import cv2 as cv
import numpy as np
from segno.helpers import make_epc_qr


def decode(qrcode):
    out = io.BytesIO()
    qrcode.save(out, scale=3, kind='png')
    out.seek(0)
    img = cv.imdecode(np.frombuffer(out.getvalue(), np.uint8), flags=cv.IMREAD_COLOR)
    detector = cv.QRCodeDetector()
    decoded, points, qrcode_bin = detector.detectAndDecode(img)
    return decoded or None


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
