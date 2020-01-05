# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
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


def test_colormap_empty():
    assert not utils.colormap()


def test_colormap_dark():
    cm = utils.colormap(dark='blue')
    # Finder dark, version dark, format dark , timing dark, alignment dark, data dark, dark module
    assert 7 == len(cm)
    assert all([clr >> 8 > 0 for clr in cm])
    values = set(cm.values())
    assert 1 == len(values)
    assert 'blue' in values


def test_colormap_light():
    cm = utils.colormap(light='white')
    # Finder light, version light, format light , timing light, alignment light,
    # data light, quiet zone, separator
    assert 8 == len(cm)
    assert all([clr >> 8 == 0 for clr in cm])
    values = set(cm.values())
    assert 1 == len(values)
    assert 'white' in values


def test_colormap():
    cm = utils.colormap(dark='blue', alignment_dark='red')
    # Finder dark, version dark, format dark , timing dark, alignment dark, data dark, dark module
    assert 7 == len(cm)
    assert all([clr >> 8 > 0 for clr in cm])
    values = set(cm.values())
    assert 2 == len(values)
    assert 'red' == cm[consts.TYPE_ALIGNMENT_PATTERN_DARK]
    assert 'blue' in values


def test_colormap_singlevalue():
    cm = utils.colormap(quiet_zone='red')
    assert 1 == len(cm)
    assert 'red' == cm[consts.TYPE_QUIET_ZONE]


if __name__ == '__main__':
    pytest.main([__file__])
