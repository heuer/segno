#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
PNG related tests.
"""
import io
import os
import re
import pytest
import segno
from png import Reader as PNGReader


def test_hexcolor_too_short():
    qr = segno.make_qr('test')
    with pytest.raises(ValueError):
        qr.save(io.BytesIO(), kind='png', dark='#FFFFF')


def test_hexcolor_too_short_background():
    qr = segno.make_qr('test')
    with pytest.raises(ValueError):
        qr.save(io.BytesIO(), kind='png', light='#FFFFF')


def test_hexcolor_too_long():
    qr = segno.make_qr('test')
    with pytest.raises(ValueError):
        qr.save(io.BytesIO(), kind='png', dark='#0000000')


def test_hexcolor_too_long_background():
    qr = segno.make_qr('test')
    with pytest.raises(ValueError):
        qr.save(io.BytesIO(), kind='png', light='#0000000')


def test_dark_eq_light():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='#000', light='#000')
    assert out.getvalue()


_has_palette = re.compile(br'PLTE').search
_has_transparency = re.compile(br'tRNS').search


def test_greyscale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='#000', light='#fff')
    assert not _has_palette(out.getvalue())
    assert not _has_transparency(out.getvalue())


def test_greyscale2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='white', light='black')
    assert not _has_palette(out.getvalue())
    assert not _has_transparency(out.getvalue())


def test_greyscale_trans():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='#000', light=None)
    assert not _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_greyscale_trans2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark=None, light='white')
    assert not _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='blue', light='white')
    assert _has_palette(out.getvalue())
    assert not _has_transparency(out.getvalue())


def test_color_trans():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='blue', light=None)
    assert _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_color_trans2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark=None, light='green')
    assert _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_color_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='#0000ffcc', light='white')
    assert _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_color_rgba2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='#000', light='#0000ffcc')
    assert _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_color_rgba_and_trans():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark='#0000ffcc', light=None)
    assert _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_color_rgba_and_trans2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dark=None, light='#0000ffcc')
    assert _has_palette(out.getvalue())
    assert _has_transparency(out.getvalue())


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 12
    width, height = qr.symbol_size(scale=scale)
    qr.save(out, kind='png', scale=12)
    out.seek(0)
    png_width, png_height, matrix = _get_png_info(file=out)
    assert (width, height) == (png_width, png_height)


def test_nodpi():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png')
    out.seek(0)
    assert b'pHYs' not in out.getvalue()


def test_nodpi_zero():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dpi=0)
    out.seek(0)
    assert b'pHYs' not in out.getvalue()


def test_dpi_negative():
    qr = segno.make('test')
    out = io.BytesIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='png', dpi=-3)


def test_dpi():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', dpi=300)
    out.seek(0)
    assert b'pHYs' in out.getvalue()
    # pHYs 11811 (11811 meters = 300 dpi / 0.0254)
    assert b'\x70\x48\x59\x73\x00\x00\x2E\x23\x00\x00\x2E\x23\x01\x78\xA5\x3F\x76' in out.getvalue()


def png_as_matrix(buff, border):
    """\
    Reads the PNG from the provided buffer and returns the code matrix (list
    of lists containing 0 .. 1 values).
    """
    buff.seek(0)
    w, h, pixels = _get_png_info(file=buff)
    # PNG: white = 1, black = 0. QR code: white = 0, black = 1
    from_idx, to_idx = border, -border
    if border == 0:
        from_idx = 0
        to_idx = len(pixels)
    res = []
    for row in pixels[from_idx:to_idx]:
        res.append([bit ^ 0x1 for bit in row[from_idx:to_idx]])
    return res


def _make_pixel_array(pixels, is_greyscale):
    """\
    Returns a list of lists. Each list contains 0 and/or 1.
    0 == black, 1 == white.

    :param bool is_greyscale: Indiciates if this function must convert RGB colors
            into black/white (supported values: (0, 0, 0) = black and
            (255, 255, 255) = white)
    """
    def bw_color(r, g, b):
        rgb = r, g, b
        if rgb == (0, 0, 0):
            return 0
        elif rgb == (255, 255, 255):
            return 1
        else:
            raise ValueError(f'Unexpected RGB tuple: {rgb})')
    res = []
    if is_greyscale:
        res = [list(row[:]) for row in pixels]
    else:
        for row in pixels:
            it = [iter(row)] * 3
            res.append([bw_color(r, g, b) for r, g, b in zip(*it)])
    return res


def _get_reference_filename(filename):
    """\
    Returns an absolute path to the "reference" filename.
    """
    return os.path.join(os.path.dirname(__file__), f'ref/{filename}')


def _get_png_info(**kw):
    """\
    Returns the width, height and the pixels of the provided PNG file.
    """
    reader = PNGReader(**kw)
    w, h, pixels, meta = reader.asDirect()
    return w, h, _make_pixel_array(pixels, meta['greyscale'])


if __name__ == '__main__':
    pytest.main([__file__])
