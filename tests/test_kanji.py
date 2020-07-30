# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against Kanji encoding.
"""
from __future__ import absolute_import, unicode_literals
import pytest
import segno
from segno import consts, encoder


def test_detect_kanji():
    qr = segno.make('続きを読む')
    assert 'kanji' == qr.mode
    assert qr.is_micro
    assert 'M3-L' == qr.designator


def test_detect_kanji_encoder():
    qr = encoder.encode('続きを読む')
    assert 1 == len(qr.segments)
    segment = qr.segments[0]
    assert consts.MODE_KANJI == segment.mode
    assert 5 == segment.char_count


def test_detect_kanji_encoder2():
    qr = encoder.encode('漢字')
    assert 1 == len(qr.segments)
    segment = qr.segments[0]
    assert consts.MODE_KANJI == segment.mode
    assert 2 == segment.char_count


if __name__ == '__main__':
    pytest.main([__file__])
