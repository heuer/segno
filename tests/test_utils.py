#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the ``utils`` module.
"""
import pytest
from segno import utils


def test_get_border_qr():
    matrix_size = 21, 21  # Version 1
    border = utils.get_border(matrix_size, None)
    assert 4 == border
    border = utils.get_border(matrix_size, 3)
    assert 3 == border


def test_get_border2():
    matrix_size = 11, 11  # M1
    border = utils.get_border(matrix_size, 1)
    assert 1 == border
    border = utils.get_border(matrix_size, None)
    assert 2 == border


def test_get_border3():
    matrix_size = 29, 29  # Version 3
    border = utils.get_border(matrix_size, 0)
    assert 0 == border
    border = utils.get_border(matrix_size, None)
    assert 4 == border


def test_get_symbol_size():
    matrix_size = 21, 21  # QR Code version 1
    border = 0
    width, height = utils.get_symbol_size(matrix_size, border=border)
    assert matrix_size == (width, height)
    border = 4
    width, height = utils.get_symbol_size(matrix_size)
    assert (matrix_size[0] + 2 * border, matrix_size[1] + 2 * border) == (width, height)


def test_get_symbol_size_micro():
    matrix_size = 13, 13  # M2
    border = 0
    width, height = utils.get_symbol_size(matrix_size, border=border)
    assert matrix_size == (width, height)
    border = 2
    width, height = utils.get_symbol_size(matrix_size)
    assert (matrix_size[0] + 2 * border, matrix_size[1] + 2 * border) == (width, height)


@pytest.mark.parametrize('scale', [1, 1.2, .8, 10])
def test_valid_scale(scale):
    assert utils.check_valid_scale(scale) is None


@pytest.mark.parametrize('scale', (0.0, 0, -1, -.2, int(.8)))
def test_invalid_scale(scale):
    with pytest.raises(ValueError):
        utils.check_valid_scale(scale)


@pytest.mark.parametrize('border', (None, 0, 0.0, 1, 2))
def test_valid_border(border):
    assert utils.check_valid_border(border) is None


@pytest.mark.parametrize('border', (.2, -1, 1.3))
def test_invalid_border(border):
    with pytest.raises(ValueError):
        utils.check_valid_border(border)


if __name__ == '__main__':
    pytest.main([__file__])
