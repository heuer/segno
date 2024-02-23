#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #18.
<https://github.com/heuer/segno/issues/18>
"""
import segno


def test_issue_18():
    qr = segno.make_qr('')
    assert 1 == qr.version
    assert 'byte' == qr.mode
    assert 'H' == qr.error


def test_issue_18_micro():
    qr = segno.make_micro('')
    assert 'M3' == qr.version
    assert 'byte' == qr.mode
    assert 'M' == qr.error


def test_issue_18_automatic():
    qr = segno.make('')
    assert 'M3' == qr.version
    assert 'byte' == qr.mode
    assert 'M' == qr.error


def test_issue_18_zero():
    qr = segno.make_qr(0)
    assert 1 == qr.version
    assert 'numeric' == qr.mode
    assert 'H' == qr.error


def test_issue_18_zero_micro():
    qr = segno.make_micro(0)
    assert 'M1' == qr.version
    assert 'numeric' == qr.mode
    assert qr.error is None


def test_issue_18_zero_automatic():
    qr = segno.make(0)
    assert 'M1' == qr.version
    assert 'numeric' == qr.mode
    assert qr.error is None


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
