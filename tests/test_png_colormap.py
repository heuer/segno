# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
PNG related tests.
"""
from __future__ import unicode_literals, absolute_import
import io
import pytest
import segno
from segno import moduletypes as mt
from segno import colors
from png import Reader as PNGReader


def test_greyscale():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    qr.save(buff, kind='png', colormap={mt.TYPE_QUIET_ZONE: 'white'})
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert reader.greyscale


def test_not_greyscale():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    qr.save(buff, kind='png', colormap={mt.TYPE_QUIET_ZONE: None})  # Three "colors": white, black, transparent
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 3 == len(palette)
    assert 0 == palette[0][3]  # Transparent color
    assert (0, 0, 0, 255) in palette  # black
    assert (255, 255, 255, 255) in palette  # white


def test_plte():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    dark = (0, 0, 139)
    colormap = _make_colormapping(dark=dark, light=None)
    qr.save(buff, kind='png', colormap=colormap)
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 2 == len(palette)
    assert 0 == palette[0][3]  # Transparent color
    dark_with_alpha = dark + (255,)
    assert dark_with_alpha in palette


def test_plte_no_transparency():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    dark = (0, 0, 139)
    light = (255, 255, 255)
    colormap = _make_colormapping(dark=dark, light=light)
    qr.save(buff, kind='png', colormap=colormap)
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 2 == len(palette)
    assert dark in palette
    assert light in palette


def test_plte_colors():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    dark = (0, 0, 139)
    light = (255, 255, 255)
    colormap = _make_colormapping(dark=dark, light=light)
    colormap[mt.TYPE_QUIET_ZONE] = 'green'
    colormap[mt.TYPE_FINDER_PATTERN_DARK] = 'purple'
    colormap[mt.TYPE_FINDER_PATTERN_LIGHT] = 'yellow'
    qr.save(buff, kind='png', colormap=colormap)
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 5 == len(palette)
    assert dark in palette
    assert light in palette
    assert colors.color_to_rgb('green') in palette
    assert colors.color_to_rgb('purple') in palette
    assert colors.color_to_rgb('yellow') in palette


def _make_colormapping(dark, light):
    return {mt.TYPE_FINDER_PATTERN_DARK: dark, mt.TYPE_FINDER_PATTERN_LIGHT: light,
            mt.TYPE_ALIGNMENT_PATTERN_DARK: dark, mt.TYPE_ALIGNMENT_PATTERN_LIGHT: light,
            mt.TYPE_SEPARATOR: light, mt.TYPE_DARKMODULE: dark,
            mt.TYPE_DATA_DARK: dark, mt.TYPE_DATA_LIGHT: light,
            mt.TYPE_FORMAT_DARK: dark, mt.TYPE_FORMAT_LIGHT: light,
            mt.TYPE_QUIET_ZONE: light,
            mt.TYPE_VERSION_DARK: dark, mt.TYPE_VERSION_LIGHT: light,
            mt.TYPE_TIMING_DARK: dark, mt.TYPE_TIMING_LIGHT: light}


if __name__ == '__main__':
    pytest.main([__file__])
