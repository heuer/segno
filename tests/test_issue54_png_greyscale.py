#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #54.
<https://github.com/heuer/segno/issues/54>
"""
import io
import pytest
from png import Reader as PNGReader
import segno


@pytest.mark.parametrize('dark, light, transparent', [('white', None, (0,)),
                                                      ('white', 'black', None),
                                                      (None, 'black', (1,))])
def test_issue_54_inverted(dark, light, transparent):
    qr = segno.make('The Beatles')
    assert 'M4-M' == qr.designator
    out = io.BytesIO()
    scale = 5
    qr.save(out, kind='png', scale=scale, dark=dark, light=light)
    out.seek(0)
    reader = PNGReader(file=out)
    w, h, pixels, meta = reader.read()
    width, height = qr.symbol_size(scale=scale)
    assert width == w
    assert height == h
    assert meta['greyscale']
    border_row = tuple([0] * w)
    expected_row = tuple([0] * 2 * scale + [1] * 7 * scale + [0])
    for idx, row in enumerate(pixels):
        if idx < 10:
            assert border_row == tuple(row)
        elif idx == 10:
            assert expected_row == tuple(row)[:len(expected_row)]
            break
    assert transparent == reader.transparent


@pytest.mark.parametrize('dark, light, transparent', [('black', None, (1,)),
                                                      ('black', 'white', None),
                                                      (None, 'white', (0,))])
def test_issue_54_notinverted(dark, light, transparent):
    qr = segno.make('The Beatles')
    assert 'M4-M' == qr.designator
    out = io.BytesIO()
    scale = 5
    qr.save(out, kind='png', scale=scale, dark=dark, light=light)
    out.seek(0)
    reader = PNGReader(file=out)
    w, h, pixels, meta = reader.read()
    width, height = qr.symbol_size(scale=scale)
    assert width == w
    assert height == h
    assert meta['greyscale']
    border_row = tuple([1] * w)
    expected_row = tuple([1] * 2 * scale + [0] * 7 * scale + [1])
    for idx, row in enumerate(pixels):
        if idx < 10:
            assert border_row == tuple(row)
        elif idx == 10:
            assert expected_row == tuple(row)[:len(expected_row)]
            break
    assert transparent == reader.transparent


if __name__ == '__main__':
    pytest.main([__file__])
