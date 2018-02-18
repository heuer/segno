# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2018 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the ``utils`` module.
"""
from __future__ import absolute_import, unicode_literals
import pytest
from segno import utils, consts


def test_get_border():
    border = utils.get_border(1, None)
    assert 4 == border
    border = utils.get_border(1, 3)
    assert 3 == border


def test_get_border2():
    border = utils.get_border(consts.VERSION_M1, 1)
    assert 1 == border
    border = utils.get_border(consts.VERSION_M1, None)
    assert 2 == border


def test_get_border3():
    border = utils.get_border(3, 0)
    assert 0 == border
    border = utils.get_border(3, None)
    assert 4 == border


def test_get_symbol_size():
    version = 1
    matrix_size = 21
    border = 0
    width, height = utils.get_symbol_size(version, border=border)
    assert (matrix_size, matrix_size) == (width, height)
    border = 4
    width, height = utils.get_symbol_size(1)
    assert (matrix_size + 2 * border, matrix_size + 2 * border) ==  (width, height)


def test_get_symbol_size_micro():
    version = consts.VERSION_M2
    matrix_size = 13
    border = 0
    width, height = utils.get_symbol_size(version, border=border)
    assert (matrix_size, matrix_size) == (width, height)
    border = 2
    width, height = utils.get_symbol_size(version)
    assert (matrix_size + 2 * border, matrix_size + 2 * border) == (width, height)


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
