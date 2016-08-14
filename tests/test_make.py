# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the encoder module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
from nose.tools import eq_, ok_, raises
import segno
from segno import consts

_DATA_AUTODETECT = (
    # Input, expected version, expected mode
    ('123456', 'numeric'),
    (123456, 'numeric'),
    (+123456, 'numeric'),
    ('+123456', 'alphanumeric'),
    (-1234, 'alphanumeric'),
    ('-1234', 'alphanumeric'),
    ('123A', 'alphanumeric'),
    ('123a', 'byte'),
    (consts.ALPHANUMERIC_CHARS, 'alphanumeric'),
    ('HELLO WORLD', 'alphanumeric'),
    ('HELLO\nWORLD', 'byte'),
    ('MÄRCHENBUCH', 'byte'),
    ('ABCDEFGHIJ1234567890\n', 'byte'),
    ('®', 'byte'),
    ('http://www.example.org/', 'byte'),
    ('http://www.example.org/path/index.html', 'byte'),
    ('点', 'kanji'),
    ('茗', 'kanji'),
    ('漢字', 'kanji'),
    ('外来語', 'kanji'),
    ('外来語'.encode('utf-8'), 'byte'),
)


def test_valid_mode_autodetection():
    def check_qr(data, expected_mode):
        qr = segno.make_qr(data)
        eq_(expected_mode, qr.mode)

    def check_auto(data, expected_mode):
        qr = segno.make(data)
        eq_(expected_mode, qr.mode)

    for data, mode in _DATA_AUTODETECT:
        yield check_qr, data, mode
        yield check_auto, data, mode


def test_default_encoding():
    qr = segno.make('Märchenbücher', error='m', micro=False)
    # 1 since the data fits into version 1 if ISO/IEC 8859-1 (the default
    # encoding) is used
    eq_(1, qr.version)
    eq_('byte', qr.mode)


def test_encoding_latin1():
    qr = segno.make('Märchenbücher', error='m', encoding='latin1', micro=False)
    eq_(1, qr.version)
    eq_('byte', qr.mode)


def test_encoding_utf8():
    qr = segno.make('Märchenbücher', error='m', encoding='utf-8', micro=False)
    eq_(2, qr.version)
    eq_('byte', qr.mode)


def test_kanji_enforce_byte():
    data = '点'
    qr = segno.make_qr(data)
    eq_('kanji', qr.mode)
    qr = segno.make_qr(data, encoding='utf-8')
    eq_('byte', qr.mode)


def test_kanji_enforce_byte2():
    data = '点'
    qr = segno.make_qr(data.encode('utf-8'))
    eq_('byte', qr.mode)


def test_kanji_bytes():
    data = '外来語'
    qr = segno.make_qr(data.encode('shift_jis'))
    eq_('kanji', qr.mode)


def test_kanji_mode_byte():
    data = '外来語'
    qr = segno.make_qr(data, mode='byte')
    eq_('byte', qr.mode)


def test_kanji_mode_byte2():
    data = '漢字'.encode('shift_jis')
    qr = segno.make_qr(data, mode='byte')
    eq_('byte', qr.mode)


def test_create_micro():
    qr = segno.make_micro('1')
    ok_(qr.is_micro)
    eq_('M1', qr.version)


def test_enforce_qrcode():
    content = 'HELLO WORLD'
    qr = segno.make(content)
    ok_(qr.is_micro)
    eq_('M3', qr.version)
    qr = segno.make_qr(content)
    ok_(not qr.is_micro)
    eq_(1, qr.version)
    qr = segno.make(content, micro=False)
    ok_(not qr.is_micro)
    eq_(1, qr.version)


def test_m1_has_no_error_level():
    qr = segno.make('1')
    ok_(qr.is_micro)
    eq_('M1', qr.version)
    ok_(qr.error is None)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
