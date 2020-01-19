# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test removal of support for "colormap" (introduced in release 0.3.4) still works
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
    out_legacy = io.BytesIO()
    with pytest.deprecated_call():
        qr.save(out_legacy, kind='png', scale=5, colormap=colormap)
    out_new = io.BytesIO()
    qr.save(out_new, kind='png', scale=5, finder_dark='darkred', alignment_dark='darkred',
            timing_dark='darkred', dark_module='darkred', data_dark='darkorange', data_light='yellow',
            format_dark='darkred')
    assert out_new.getvalue() == out_legacy.getvalue()


if __name__ == '__main__':
    pytest.main([__file__])
