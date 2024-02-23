#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
PAM related tests.
"""
import re
import io
import pytest
import segno


def test_invalid_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='pam', dark=None)


def test_bw():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam')
    assert b'BLACKANDWHITE' in out.getvalue()


def test_grayscale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam', light=None)
    assert b'GRAYSCALE_ALPHA' in out.getvalue()


def test_rgb():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam', dark='red')
    assert b'RGB' in out.getvalue()
    assert b'RGB_ALPHA' not in out.getvalue()


def test_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pam', dark='red', light=None)
    assert b'RGB' in out.getvalue()
    assert b'RGB_ALPHA' in out.getvalue()


_size = re.compile(br'^WIDTH\s+([0-9]+)$').match


def _image_data(buff):
    """\
    Returns the image data and the size of the matrix.
    """
    seen_size = False
    size = 0
    code = buff.getvalue().splitlines()
    code_iter = iter(code)
    for line in code_iter:
        if line.startswith(b'ENDHDR'):
            break
        if seen_size:
            continue
        m = _size(line)
        if m:
            size = int(m.group(1))
            seen_size = True
    return next(code_iter), size


def pam_bw_as_matrix(buff, border):
    """\
    Returns the QR code as list of [0, 1] lists.

    :param io.BytesIO buff: Buffer to read the matrix from.
    :param int border: The QR code border
    """
    res = []
    data, size = _image_data(buff)
    for i, offset in enumerate(range(0, len(data), size)):
        if i < border:
            continue
        if i >= size - border:
            break
        row_data = bytearray(data[offset + border:offset + size - border])
        # Invert bytes since PAM uses 0x0 = black, 0x1 = white
        res.append([b ^ 0x1 for b in row_data])
    return res


if __name__ == '__main__':
    pytest.main([__file__])
