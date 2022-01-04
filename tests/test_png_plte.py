# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2022 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests if the PNG serializer does not add more colors than needed.

See also issue <https://github.com/heuer/segno/issues/62>
"""
from __future__ import unicode_literals, absolute_import
import io
import pytest
import segno


def test_plte():
    qr = segno.make_qr('test')
    assert qr.version < 7
    dark = 'red'
    buff_1 = io.BytesIO()
    buff_2 = io.BytesIO()
    qr.save(buff_1, kind='png', dark=dark, finder_dark=dark, version_dark='green')
    qr.save(buff_2, kind='png', dark=dark)
    assert buff_1.getvalue() == buff_2.getvalue()


def test_plte2():
    qr = segno.make_qr('test')
    assert qr.version < 7
    dark = 'red'
    buff_1 = io.BytesIO()
    buff_2 = io.BytesIO()
    qr.save(buff_1, kind='png', dark=dark, finder_dark=dark, version_dark='green')
    qr.save(buff_2, kind='png', dark=dark)
    assert buff_1.getvalue() == buff_2.getvalue()


def test_plte3():
    qr = segno.make_qr('test')
    assert qr.version < 7
    dark = 'red'
    buff_1 = io.BytesIO()
    buff_2 = io.BytesIO()
    qr.save(buff_1, kind='png', dark=dark, finder_dark=dark, version_dark='green')
    qr.save(buff_2, kind='png', dark=dark)
    assert buff_1.getvalue() == buff_2.getvalue()


def test_plte_micro():
    qr = segno.make_micro('RAIN')
    dark = 'red'
    buff_1 = io.BytesIO()
    buff_2 = io.BytesIO()
    qr.save(buff_1, kind='png', dark=dark, finder_dark=dark, alignment_dark='green')
    qr.save(buff_2, kind='png', dark=dark)
    assert buff_1.getvalue() == buff_2.getvalue()


def test_plte_micro2():
    qr = segno.make_micro('RAIN')
    dark = 'red'
    buff_1 = io.BytesIO()
    buff_2 = io.BytesIO()
    qr.save(buff_1, kind='png', dark=dark, finder_dark=dark, dark_module='green')
    qr.save(buff_2, kind='png', dark=dark)
    assert buff_1.getvalue() == buff_2.getvalue()


if __name__ == '__main__':
    pytest.main([__file__])
