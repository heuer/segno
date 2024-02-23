#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
CLI colormap (PNG) related tests.
"""
import io
import os
import tempfile
import pytest
from segno import cli, writers as colors
from png import Reader as PNGReader


def _make_tmp_png_filename():
    f = tempfile.NamedTemporaryFile('w', suffix='.png', delete=False)
    f.close()
    return f.name


def test_greyscale():
    fn = _make_tmp_png_filename()
    res = cli.main(['--quiet-zone=white', f'--output={fn}', 'test'])
    with open(fn, 'rb') as f:
        data = io.BytesIO(f.read())
    os.unlink(fn)
    assert 0 == res
    reader = PNGReader(file=data)
    reader.preamble()
    assert reader.greyscale


def test_not_greyscale():
    fn = _make_tmp_png_filename()
    res = cli.main(['--quiet-zone=transparent', f'--output={fn}',
                    'test'])
    with open(fn, 'rb') as f:
        data = io.BytesIO(f.read())
    os.unlink(fn)
    assert 0 == res
    reader = PNGReader(file=data)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 3 == len(palette)
    assert 0 == palette[0][3]  # Transparent color
    assert (0, 0, 0, 255) in palette  # black
    assert (255, 255, 255, 255) in palette  # white


def test_plte_colors():
    fn = _make_tmp_png_filename()
    res = cli.main(['--quiet-zone=green', '--finder-dark=purple',
                    '--finder-light=yellow', f'--output={fn}', 'test'])
    with open(fn, 'rb') as f:
        data = io.BytesIO(f.read())
    os.unlink(fn)
    assert 0 == res
    reader = PNGReader(file=data)
    reader.preamble()
    assert not reader.greyscale
    palette = reader.palette()
    assert 5 == len(palette)
    assert (0, 0, 0) in palette
    assert (255, 255, 255) in palette
    assert colors._color_to_rgb('green') in palette
    assert colors._color_to_rgb('purple') in palette
    assert colors._color_to_rgb('yellow') in palette


if __name__ == '__main__':
    pytest.main([__file__])
