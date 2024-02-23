#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #16.
<https://github.com/heuer/segno/issues/16>
"""
import segno


def test_boost_error_automatic():
    qr = segno.make_qr('ABCDEF')
    assert '1-H' == qr.designator


def test_boost_error_automatic_disabled():
    qr = segno.make_qr('ABCDEF', boost_error=False)
    assert '1-L' == qr.designator


def test_boost_error_automatic_arg_error():
    qr = segno.make_qr('ABCDEF', error='l')
    assert '1-H' == qr.designator


def test_boost_error_disabled_arg_error():
    qr = segno.make_qr('ABCDEF', error='l', boost_error=False)
    assert '1-L' == qr.designator


def test_boost_error_m1():
    qr = segno.make('01234')
    assert qr.is_micro
    assert 'M1' == qr.version
    assert qr.error is None


def test_boost_error_micro():
    qr = segno.make('A', error='l')
    assert qr.is_micro
    assert 'M2' == qr.version
    assert 'M' == qr.error


def test_boost_error_micro_boost_disabled():
    qr = segno.make('A', error='l', boost_error=False)
    assert qr.is_micro
    assert 'M2' == qr.version
    assert 'L' == qr.error


def test_boost_error_m3():
    qr = segno.make('A', error='l', version='M3')
    assert qr.is_micro
    assert 'M3' == qr.version
    assert 'M' == qr.error


def test_boost_error_m3_boost_disabled():
    qr = segno.make('A', error='l', version='M3', boost_error=False)
    assert qr.is_micro
    assert 'M3' == qr.version
    assert 'L' == qr.error


def test_boost_error_m4():
    qr = segno.make('A', error='l', version='M4')
    assert qr.is_micro
    assert 'M4' == qr.version
    assert 'Q' == qr.error


def test_boost_error_m4_boost_disabled():
    qr = segno.make('A', error='l', version='M4', boost_error=False)
    assert qr.is_micro
    assert 'M4' == qr.version
    assert 'L' == qr.error


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
