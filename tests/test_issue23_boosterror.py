# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2017 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #23.
<https://github.com/heuer/segno/issues/23>
"""
from __future__ import unicode_literals, absolute_import
import segno


def test_boost_error_automatic():
    qr = segno.make('http://www.example.org/bla/bla/')
    assert '3-Q' == qr.designator


def test_boost_error_disabled():
    qr = segno.make('http://www.example.org/bla/bla/', error='q', boost_error=False)
    assert '3-Q' == qr.designator


def test_boost_error_disabled2():
    qr = segno.make('http://www.example.org/bla/bla/', error='h', boost_error=False)
    assert '4-H' == qr.designator


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
