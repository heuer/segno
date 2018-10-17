# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2018 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the ``utils.matrix_iter_details`` function.
"""
from __future__ import absolute_import, unicode_literals, print_function
import io
import os
import pytest
from segno import encoder, utils


def read_matrix(name):
    """\
    Helper function to read a matrix from /ref_matrix. The file extension .txt
    is added automatically.

    :return: A tuple of bytearrays
    """
    matrix = []
    with io.open(os.path.join(os.path.dirname(__file__), 'feature_decompose/{0}.txt'.format(name)), 'rt') as f:
        for row in f:
            matrix.append(bytearray([int(i) for i in row if i != '\n']))
    return matrix


def test_finder_pattern_dark_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_FINDER_PATTERN_DARK] for v in row]))
    expected = read_matrix('v1-finder-dark')
    assert expected == res


def test_finder_pattern_dark_light_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_FINDER_PATTERN_LIGHT] for v in row]))
    expected = read_matrix('v1-finder-light')
    assert expected == res


def test_finder_pattern_dark_and_light_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v in (utils.TYPE_FINDER_PATTERN_DARK, utils.TYPE_FINDER_PATTERN_LIGHT)] for v in row]))
    expected = read_matrix('v1-finder-dark-and-light')
    assert expected == res


def test_finder_pattern_dark_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_FINDER_PATTERN_DARK] for v in row]))
    expected = read_matrix('m2-finder-dark')
    assert expected == res


def test_finder_pattern_dark_light_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_FINDER_PATTERN_LIGHT] for v in row]))
    expected = read_matrix('m2-finder-light')
    assert expected == res


def test_finder_pattern_dark_and_light_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v in (utils.TYPE_FINDER_PATTERN_DARK, utils.TYPE_FINDER_PATTERN_LIGHT)] for v in row]))
    expected = read_matrix('m2-finder-dark-and-light')
    assert expected == res


def test_separator_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_SEPARATOR] for v in row]))
    expected = read_matrix('v1-separator')
    assert expected == res


def test_separator_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_SEPARATOR] for v in row]))
    expected = read_matrix('m2-separator')
    assert expected == res


def test_darkmodule_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_DARKMODULE] for v in row]))
    expected = read_matrix('v1-darkmodule')
    assert expected == res


def test_no_darkmodule_mqr():
    # Micro QR Codes don't have a dark module.
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.extend([v == utils.TYPE_DARKMODULE for v in row])
    assert True not in res


def test_timing_dark_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_TIMING_DARK] for v in row]))
    expected = read_matrix('v1-timing-dark')
    assert expected == res


def test_timing_light_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_TIMING_LIGHT] for v in row]))
    expected = read_matrix('v1-timing-light')
    assert expected == res


def test_timing_dark_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_TIMING_DARK] for v in row]))
    expected = read_matrix('m2-timing-dark')
    assert expected == res


def test_timing_light_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_TIMING_LIGHT] for v in row]))
    expected = read_matrix('m2-timing-light')
    assert expected == res


def test_timing_dark_and_light_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v in (utils.TYPE_TIMING_DARK, utils.TYPE_TIMING_LIGHT)] for v in row]))
    expected = read_matrix('m2-timing-dark-and-light')
    assert expected == res


def test_alignment_dark():
    qr = encoder.encode('A', version=12)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_ALIGNMENT_PATTERN_DARK] for v in row]))
    expected = read_matrix('v12-alignment-dark')
    assert expected == res


def test_alignment_light():
    qr = encoder.encode('A', version=12)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_ALIGNMENT_PATTERN_LIGHT] for v in row]))
    expected = read_matrix('v12-alignment-light')
    assert expected == res


def test_alignment_dark_and_light():
    qr = encoder.encode('A', version=12)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v in (utils.TYPE_ALIGNMENT_PATTERN_LIGHT, utils.TYPE_ALIGNMENT_PATTERN_DARK)] for v in row]))
    expected = read_matrix('v12-alignment-dark-and-light')
    assert expected == res


def test_version_dark():
    qr = encoder.encode('A', version=7)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_VERSION_DARK] for v in row]))
    expected = read_matrix('v7-version-dark')
    assert expected == res


def test_version_light():
    qr = encoder.encode('A', version=7)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_VERSION_LIGHT] for v in row]))
    expected = read_matrix('v7-version-light')
    assert expected == res


def test_version_dark_and_light():
    qr = encoder.encode('A', version=7)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v in (utils.TYPE_VERSION_LIGHT, utils.TYPE_VERSION_DARK)] for v in row]))
    expected = read_matrix('v7-version-dark-and-light')
    assert expected == res


def test_version_no_version():
    # The version information is not available in QR Codes < 7
    qr = encoder.encode('A', version=6)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.extend([v in (utils.TYPE_VERSION_LIGHT, utils.TYPE_VERSION_DARK) for v in row])
    assert True not in res


def test_format_dark_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v == utils.TYPE_FORMAT_DARK] for v in row]))
    expected = read_matrix('v1-format-dark')
    assert expected == res


def test_format_light_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_FORMAT_LIGHT] for v in row]))
    expected = read_matrix('v1-format-light')
    assert expected == res


def test_format_dark_and_light_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=0):
        res.append(bytearray([(0x2, 0x1)[v in (utils.TYPE_FORMAT_DARK, utils.TYPE_FORMAT_LIGHT)] for v in row]))
    expected = read_matrix('v1-format-dark-and-light')
    assert expected == res


def test_quietzone_default_qr():
    qr = encoder.encode('A', micro=False)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_QUIET_ZONE] for v in row]))
    expected = read_matrix('v1-quietzone-4')
    assert expected == res


def test_quietzone_custom_qr():
    qr = encoder.encode('A', micro=False)
    border = 1
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=border):
        res.append(bytearray([(0x2, 0x0)[v == utils.TYPE_QUIET_ZONE] for v in row]))
    expected = read_matrix('v1-quietzone-1')
    assert expected == res


def test_quietzone_default_mqr():
    qr = encoder.encode('A', micro=True)
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version):
        res.append(bytearray([(0x1, 0x0)[v == utils.TYPE_QUIET_ZONE] for v in row]))
    expected = read_matrix('m2-quietzone-2')
    assert expected == res


def test_quietzone_custom_mqr():
    qr = encoder.encode('A', micro=True)
    border = 5
    res = []
    for row in utils.matrix_iter_detail(qr.matrix, qr.version, border=border):
        res.append(bytearray([(0x1, 0x0)[v == utils.TYPE_QUIET_ZONE] for v in row]))
    expected = read_matrix('m2-quietzone-5')
    assert expected == res


if __name__ == '__main__':
    pytest.main([__file__])
