# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test if the keywords "color" and "background" are still supported.
"""
from __future__ import unicode_literals, absolute_import
import io
import pytest
import segno


def test_colorbackground():
    qr = segno.make('The Beatles')
    out_new = io.BytesIO()
    out_old = io.BytesIO()
    qr.save(out_new, kind='png', dark='blue', light='yellow')
    qr.save(out_old, kind='png', color='blue', background='yellow')
    assert out_new.getvalue() == out_old.getvalue()

if __name__ == '__main__':
    pytest.main([__file__])
