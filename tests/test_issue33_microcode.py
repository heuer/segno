#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 33 and 37
<https://github.com/heuer/segno/issues/33>
<https://github.com/heuer/segno/issues/37>
"""
import pytest
import segno
from segno import consts
from segno import encoder
try:
    from .tutils import read_matrix
# Attempted relative import in non-package
except (ValueError, SystemError, ImportError):
    from tutils import read_matrix


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
@pytest.mark.parametrize('version', [None, 'm1'])
def test_m1_50041(data, version):
    qr = segno.make(data, version=version)
    assert 'M1' == qr.designator
    ref_matrix = read_matrix('issue-33-m1-50041')[0]
    assert ref_matrix == qr.matrix


@pytest.mark.parametrize('data', ['1234', 1234])
@pytest.mark.parametrize('version', [None, 'm1'])
def test_m1_1234(data, version):
    qr = segno.make(data, version=version)
    assert 'M1' == qr.designator
    ref_matrix = read_matrix('issue-33-m1-1234')[0]
    assert ref_matrix == qr.matrix


@pytest.mark.parametrize('data', ['12345', 12345])
@pytest.mark.parametrize('version', [None, 'm1'])
def test_m1_12345(data, version):
    qr = segno.make(data, version=version)
    assert 'M1' == qr.designator
    ref_matrix = read_matrix('issue-33-m1-12345')[0]
    assert ref_matrix == qr.matrix


def test_m3_wikipedia():
    qr = segno.make('Wikipedia', version='m3', error='l')
    assert 'M3-L' == qr.designator
    ref_matrix = read_matrix('issue-33-m3-l-wikipedia')[0]
    assert ref_matrix == qr.matrix


def test_m3_max_numeric():
    qr = segno.make('12345678901234567890123', version='m3', error='l')
    assert 'M3-L' == qr.designator
    ref_matrix = read_matrix('issue-33-m3-l-12345678901234567890123')[0]
    assert ref_matrix == qr.matrix


def test_jump_from_m3_to_m4_dont_boost_error():
    qr = segno.make('123456789012345678901234', boost_error=False)
    assert 'M4-L' == qr.designator
    ref_matrix = read_matrix('issue-33-m3-l-to-m4-l-jump')[0]
    assert ref_matrix == qr.matrix


def test_jump_from_m3_to_m4_boost_error():
    qr = segno.make('123456789012345678901234')
    assert 'M4-M' == qr.designator
    ref_matrix = read_matrix('issue-33-m3-l-to-m4-m-jump')[0]
    assert ref_matrix == qr.matrix


if __name__ == '__main__':
    pytest.main([__file__])
