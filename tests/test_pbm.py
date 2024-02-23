#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
PBM related tests.
"""
import re
import io
from itertools import islice
import pytest
import segno


def test_p4():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pbm')
    assert out.getvalue().startswith(b'P4')


def test_not_plain():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pbm', plain=False)
    assert out.getvalue().startswith(b'P4')


def test_p1():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pbm', plain=True)
    assert out.getvalue().startswith(b'P1')


_is_size = re.compile(br'^([0-9]+)\s+[0-9]+$').match


def _move_to_raster(buff, border):
    """\
    Returns an iterator and the si
    """
    code = buff.getvalue().splitlines()
    len_without_border = 0
    code_iter = iter(code)
    for line in code_iter:
        if line.startswith(b'P') or line.startswith(b'#'):
            continue
        m = _is_size(line)
        if m:
            len_without_border = int(m.group(1)) - border
            break
    return code_iter, len_without_border


def pbm_p1_as_matrix(buff, border):
    """\
    Returns the text QR code as list of [0, 1] lists.

    :param io.BytesIO buff: Buffer to read the matrix from.
    :param int border: The QR code border
    """
    res = []
    code_iter, len_without_border = _move_to_raster(buff, border)
    for line in islice(code_iter, border, len_without_border):
        row = [int(i) for i in islice(line.decode('ascii'), border,
                                      len_without_border)]
        res.append(row)
    return res


if __name__ == '__main__':
    pytest.main([__file__])
