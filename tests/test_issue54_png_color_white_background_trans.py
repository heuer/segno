# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #54.
<https://github.com/heuer/segno/issues/54>
"""
from __future__ import unicode_literals, absolute_import
import io
from png import Reader as PNGReader
import segno


def test_issue_54():
    qr = segno.make('The Beatles')
    assert 'M4-M' == qr.designator
    out = io.BytesIO()
    scale = 5
    qr.save(out, kind='png', scale=scale, color='white', background=None)
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
    assert (0,) == reader.transparent


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])

