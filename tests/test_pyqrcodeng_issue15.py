# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue <https://github.com/pyqrcode/pyqrcodeNG/issues/15>.

Adapted for Segno to check if it suffers from the same problem.
"""
from __future__ import absolute_import, unicode_literals
import pytest
import segno


def test_version_too_small():
    with pytest.raises(segno.DataOverflowError):
        segno.make('A' * 26, version=1)


def test_version_and_error_provided():
    # QR Code version 1-L: Max. 25 alphanumeric chars
    qr = segno.make('A' * 25, version=1, error='l')
    assert '1-L' == qr.designator
    assert 'alphanumeric' == qr.mode


def test_version_and_error_provided2():
    qr = segno.make('A' * 25, version=1)  # No error level defined
    assert '1-L' == qr.designator
    assert 'alphanumeric' == qr.mode


if __name__ == '__main__':
    pytest.main([__file__])
