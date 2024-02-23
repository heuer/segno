#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #23.
<https://github.com/heuer/segno/issues/23>
"""
import segno


def test_boost_error_automatic():
    qr = segno.make('http://www.example.org/')
    assert '2-M' == qr.designator


def test_boost_error_disabled():
    qr = segno.make('http://www.example.org/', error='q', boost_error=False)
    assert '3-Q' == qr.designator


def test_boost_error_automatic2():
    qr = segno.make('http://www.example.org/', error='q')
    assert '3-H' == qr.designator


def test_boost_error_disabled2():
    qr = segno.make('http://www.example.org/', error='l', boost_error=False)
    assert '2-L' == qr.designator


def test_boost_error_disabled3():
    qr = segno.make('http://www.example.org/', error='h')
    assert '3-H' == qr.designator


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
