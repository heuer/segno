#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #4.
<https://github.com/heuer/segno/issues/4>
"""
from segno import consts, encoder


def test_issue_4():
    qr = encoder.encode(0)
    assert consts.VERSION_M1 == qr.version
    assert qr.error is None


def test_issue_4_autodetect_micro():
    qr = encoder.encode(1)
    assert consts.VERSION_M1 == qr.version
    assert qr.error is None


def test_issue_4_explicit_error():
    qr = encoder.encode(1, error=None)
    assert consts.VERSION_M1 == qr.version
    assert qr.error is None


def test_issue_4_explicit_error2():
    qr = encoder.encode(1, error='m')
    assert consts.VERSION_M2 == qr.version
    assert consts.ERROR_LEVEL_M == qr.error


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
