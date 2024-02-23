#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
PPM related tests.
"""
import re
import io
from struct import unpack
import pytest
import segno


def test_invalid_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='ppm', dark=None)


def test_not_plain():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='ppm')
    assert out.getvalue().startswith(b'P6')


_size = re.compile(br'^P6\s+(?:#[^\n]+\s*)([0-9]+)\s+(?:[0-9]+\s+[0-9]+\n)').match


def _image_data(buff):
    """\
    Returns the image data and the size of the matrix.
    """
    code = buff.getvalue()
    m = _size(code)
    if m:
        size = int(m.group(1))
    else:
        raise Exception('Internal error: PPM header not found')
    return code[m.end():], size


def ppm_bw_as_matrix(buff, border):
    """\
    Returns the QR code as list of [0, 1] lists.

    :param io.BytesIO buff: Buffer to read the matrix from.
    """
    res = []
    data, size = _image_data(buff)
    rgb_data = [unpack('>3B', data[i:i + 3]) for i in range(0, len(data), 3)]
    for i, offset in enumerate(range(0, len(rgb_data), size)):
        if i < border:
            continue
        if i >= size - border:
            break
        row_data = rgb_data[offset + border:offset + size - border]
        res.append([(0x0, 0x1)[rgb == (0, 0, 0)] for rgb in row_data])
    return res


if __name__ == '__main__':
    pytest.main([__file__])
