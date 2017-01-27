# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 33
<https://github.com/heuer/segno/issues/33>
"""
from __future__ import absolute_import, unicode_literals
import pytest
import segno
from segno import consts
from segno import encoder
try:
    from .utils import read_matrix
except (ValueError, SystemError):  # Attempted relative import in non-package
    from utils import read_matrix


def test_format_info_figure25():
    # 7.9.1 QR Code symbols (page 55)
    version = 1
    mask_pattern = 5
    error = consts.ERROR_LEVEL_M
    # 100000011001110
    assert 0x40ce == encoder.calc_format_info(version, error, mask_pattern)


def test_format_info_figure26():
    # 7.9.2 Micro QR Code symbols (page 57)
    version = consts.VERSION_M1
    mask_pattern = 3
    error = None
    # 100101100011100
    assert 0x4b1c == encoder.calc_format_info(version, error, mask_pattern)


@pytest.mark.parametrize('data', ['50041', 50041])
def test_m1_50041(data):
    qr = segno.make(data, version='m1')
    assert 'M1' == qr.designator
    ref_matrix = read_matrix('issue-33-m1-50041')
    assert ref_matrix == qr.matrix



if __name__ == '__main__':
    pytest.main([__file__])
