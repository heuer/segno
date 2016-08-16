# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
PNG related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import io
import os
import re
from nose.tools import ok_, eq_, raises
import segno
from png import Reader as PNGReader


@raises(ValueError)
def test_hexcolor_too_short():
    qr = segno.make_qr('test')
    qr.save(io.BytesIO(), kind='png', color='#FFFFF')


@raises(ValueError)
def test_hexcolor_too_short_background():
    qr = segno.make_qr('test')
    qr.save(io.BytesIO(), kind='png', background='#FFFFF')


@raises(ValueError)
def test_hexcolor_too_long():
    qr = segno.make_qr('test')
    qr.save(io.BytesIO(), kind='png', color='#0000000')


@raises(ValueError)
def test_hexcolor_too_long_background():
    qr = segno.make_qr('test')
    qr.save(io.BytesIO(), kind='png', background='#0000000')


@raises(ValueError)
def test_color_eq_background():
    qr = segno.make_qr('test')
    qr.save(io.BytesIO(), kind='png', color='#000', background='#000')

_has_palette = re.compile(br'PLTE').search
_has_transparency = re.compile(br'tRNS').search

def test_greyscale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='#000', background='#fff')
    ok_(not _has_palette(out.getvalue()))
    ok_(not _has_transparency(out.getvalue()))


def test_greyscale2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='white', background='black')
    ok_(not _has_palette(out.getvalue()))
    ok_(not _has_transparency(out.getvalue()))


def test_greyscale_trans():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='#000', background=None)
    ok_(not _has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_greyscale_trans2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color=None, background='white')
    ok_(not _has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='blue', background='white')
    ok_(_has_palette(out.getvalue()))
    ok_(not _has_transparency(out.getvalue()))


def test_color_trans():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='blue', background=None)
    ok_(_has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_color_trans2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color=None, background='green')
    ok_(_has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_color_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='#0000ffcc', background='white')
    ok_(_has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_color_rgba2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='#000', background='#0000ffcc')
    ok_(_has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_color_rgba_and_trans():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color='#0000ffcc', background=None)
    ok_(_has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_color_rgba_and_trans2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png', color=None, background='#0000ffcc')
    ok_(_has_palette(out.getvalue()))
    ok_(_has_transparency(out.getvalue()))


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 12
    width, height = qr.symbol_size(scale=scale)
    qr.save(out, kind='png', scale=12)
    out.seek(0)
    png_width, png_height, matrix = _get_png_info(file=out)
    eq_((width, height), (png_width, png_height))


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

    `is_greyscale`
        Indiciates if this function must convert RGB colors into black/white
        (supported values: (0, 0, 0) = black and (255, 255, 255) = white)
    """
    def bw_color(r, g, b):
        rgb = r, g, b
        if rgb == (0, 0, 0):
            return 0
        elif rgb == (255, 255, 255):
            return 1
        else:
            raise ValueError('Unexpected RGB tuple: {0})'.format(rgb))
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
    return os.path.join(os.path.dirname(__file__), 'ref/{0}'.format(filename))


def _get_png_info(**kw):
    """\
    Returns the width, height and the pixels of the provided PNG file.
    """
    reader = PNGReader(**kw)
    w, h, pixels, meta = reader.asDirect()
    return w, h, _make_pixel_array(pixels, meta['greyscale'])


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
