# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
PDF related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import re
import io
import zlib
import segno


def test_default_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 1
    scale_cmd = '{0} 0 0 {0} 0 0 cm'.format(scale)
    qr.save(out, kind='pdf', compresslevel=0)
    assert scale_cmd not in _find_graphic(out)


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 2
    scale_cmd = '{0} 0 0 {0} 0 0 cm'.format(scale)
    qr.save(out, kind='pdf', scale=scale, compresslevel=0)
    assert scale_cmd in _find_graphic(out)


def test_scale_float():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 1.34
    scale_cmd = '{0} 0 0 {0} 0 0 cm'.format(scale)
    qr.save(out, kind='pdf', scale=scale, compresslevel=0)
    assert scale_cmd in _find_graphic(out)


def _find_graphic(out):
    val = out.getvalue()
    start = b'stream\r\n'
    compressed_graphic = val[val.find(start) + len(start):val.find(b'\r\nendstream')]
    return zlib.decompress(compressed_graphic).decode('ascii')


def pdf_as_matrix(buff, border):
    """\
    Reads the path in the PDF and returns it as list of 0, 1 lists.

    :param io.BytesIO buff: Buffer to read the matrix from.
    """
    pdf = buff.getvalue()
    h, w = re.search(br'/MediaBox \[0 0 ([0-9]+) ([0-9]+)\]', pdf,
                     flags=re.MULTILINE).groups()
    if h != w:
        raise ValueError('Expected equal height/width, got height="{}" width="{}"'.format(h, w))
    size = int(w) - 2 * border

    graphic = _find_graphic(buff)
    res = [[0] * size for i in range(size)]
    for x1, y1, x2, y2 in re.findall(r'\s*(\-?\d+)\s+(\-?\d+)\s+m\s+'
                                        r'(\-?\d+)\s+(\-?\d+)\s+l', graphic):
        x1, y1, x2, y2 = [int(i) for i in (x1, y1, x2, y2)]
        y = abs(y1)
        res[y][x1:x2] = [1] * (x2 - x1)
    return res


if __name__ == '__main__':
    import pytest
    pytest.main(['-x', __file__])

