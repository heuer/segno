# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test removal of support for "colormap" (introduced in release 0.3.4).
Supported till 0.3.9 with DeprecationWarning, removed in 0.4.0.
"""
from __future__ import unicode_literals, absolute_import
import io
import pytest
import segno


def test_deprecation():
    from segno import consts as mt
    qr = segno.make('Yellow Submarine', error='h')
    colormap = {mt.TYPE_FINDER_PATTERN_DARK: 'darkred', mt.TYPE_ALIGNMENT_PATTERN_DARK: 'darkred',
                mt.TYPE_TIMING_DARK: 'darkred', mt.TYPE_DARKMODULE: 'darkred', mt.TYPE_DATA_DARK: 'darkorange',
                mt.TYPE_DATA_LIGHT: 'yellow', mt.TYPE_FORMAT_DARK: 'darkred'}
    with pytest.raises(TypeError):
        qr.save(io.BytesIO(), kind='png', scale=5, colormap=colormap)


if __name__ == '__main__':
    pytest.main([__file__])
