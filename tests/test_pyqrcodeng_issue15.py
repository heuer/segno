#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue <https://github.com/pyqrcode/pyqrcodeNG/issues/15>.

Adapted for Segno to check if it suffers from the same problem.
"""
import pytest
import segno


def test_version_too_small():
    with pytest.raises(segno.DataOverflowError) as ex:
        segno.make('A' * 26, version=1)
    assert 'does not fit' in str(ex.value)


def test_version_and_error_provided():
    # QR Code version 1-L: Max. 25 alphanumeric chars
    qr = segno.make('A' * 25, version=1, error='l')
    assert '1-L' == qr.designator
    assert 'alphanumeric' == qr.mode


def test_version_and_error_provided2():
    qr = segno.make('A' * 25, version=1)  # No error level defined
    assert '1-L' == qr.designator
    assert 'alphanumeric' == qr.mode


def test_numeric_defaults():
    qr = segno.make('1' * 17, micro=False)  # Capacity of a 1-H (numeric): 17
    assert '1-H' == qr.designator
    assert 'numeric' == qr.mode


def test_numeric_explicit_error():
    qr = segno.make('1' * 41, error='l')  # Capacity of a 1-L (numeric): 41
    assert '1-L' == qr.designator
    assert 'numeric' == qr.mode


if __name__ == '__main__':
    pytest.main([__file__])
