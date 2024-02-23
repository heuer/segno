#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
PDF related tests.
"""
import re
import io
import zlib
import pytest
import segno


def test_default_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 1
    scale_cmd = f'{scale} 0 0 {scale} 0 0 cm'
    qr.save(out, kind='pdf', compresslevel=0)
    assert scale_cmd not in _find_graphic(out)


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 2
    scale_cmd = f'{scale} 0 0 {scale} 0 0 cm'
    qr.save(out, kind='pdf', scale=scale, compresslevel=0)
    assert scale_cmd in _find_graphic(out)


def test_scale_float():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 1.34
    scale_cmd = f'{scale} 0 0 {scale} 0 0 cm'
    qr.save(out, kind='pdf', scale=scale, compresslevel=0)
    assert scale_cmd in _find_graphic(out)


def test_background_none():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pdf')
    graphic = _find_graphic(out)
    assert 'rg' not in graphic
    assert 're' not in graphic


def test_background_set():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pdf', light='yellow')
    graphic = _find_graphic(out)
    assert 'rg' in graphic
    assert 're' in graphic


def test_stokecolor_default():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pdf')
    graphic = _find_graphic(out)
    assert 'RG' not in graphic


def test_stokecolor_black():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pdf', dark='black')
    graphic = _find_graphic(out)
    assert 'RG' not in graphic


def test_stokecolor_black2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pdf', dark='#000')
    graphic = _find_graphic(out)
    assert 'RG' not in graphic


def test_stokecolor_set():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='pdf', dark='#EEE')
    graphic = _find_graphic(out)
    assert 'RG' in graphic


def test_illegal_color_float():
    color = (.1, 1.1, .1)
    qr = segno.make_qr('test')
    out = io.BytesIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='pdf', dark=color)


def _find_graphic(out):
    val = out.getvalue()
    start = b'stream\r\n'
    compressed_graphic = val[val.find(start) + len(start):val.find(b'\r\nendstream')]
    return zlib.decompress(compressed_graphic).decode('ascii')


def pdf_as_matrix(buff, border):
    """\
    Reads the path in the PDF and returns it as list of 0, 1 lists.

    :param io.BytesIO buff: Buffer to read the matrix from.
    :param int border: The QR code border
    """
    pdf = buff.getvalue()
    h, w = re.search(br'/MediaBox \[0 0 ([0-9]+) ([0-9]+)]', pdf,
                     flags=re.MULTILINE).groups()
    if h != w:
        raise ValueError(f'Expected equal height/width, got height="{h}" width="{w}"')
    size = int(w) - 2 * border

    graphic = _find_graphic(buff)
    res = [[0] * size for i in range(size)]
    for x1, y1, x2, y2 in re.findall(r'\s*(-?\d+)\s+(-?\d+)\s+m\s+'
                                     r'(-?\d+)\s+(-?\d+)\s+l', graphic):
        x1, y1, x2, y2 = (int(i) for i in (x1, y1, x2, y2))
        y = abs(y1)
        res[y][x1:x2] = [1] * (x2 - x1)
    return res


if __name__ == '__main__':
    pytest.main([__file__])
