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
import pytest
import segno
from segno import writers as colors
from png import Reader as PNGReader


def test_greyscale():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    qr.save(buff, kind='png', quiet_zone='white')
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert reader.greyscale


def test_not_greyscale():
    qr = segno.make_qr('test')
    buff = io.BytesIO()
    qr.save(buff, kind='png', quiet_zone=None)  # Three "colors": white, black, transparent
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
    qr.save(buff, kind='png', dark=dark, light=None)
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
    qr.save(buff, kind='png', dark=dark, light=light)
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
    qr.save(buff, kind='png', dark=dark, light=light, quiet_zone='green',
            finder_dark='purple', finder_light='yellow')
    buff.seek(0)
    reader = PNGReader(file=buff)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 5 == len(palette)
    assert dark in palette
    assert light in palette
    assert colors._color_to_rgb('green') in palette
    assert colors._color_to_rgb('purple') in palette
    assert colors._color_to_rgb('yellow') in palette


if __name__ == '__main__':
    pytest.main([__file__])
