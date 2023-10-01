# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Utility functions for test cases.
"""
import os
import io


def matrix_looks_valid(matrix):
    """\
    Returns if the matrix contains just ``0x0`` and ``0x1`` values.
    Does not check if the matrix represents a valid (Micro) QR Code.

    :param matrix: tuple of bytearrays
    :return:
    """
    invalid_values = []
    for i, row in enumerate(matrix):
        for j, bit in enumerate(row):
            if bit not in (0x0, 0x1):
                invalid_values.append((i, j, bit))
    if not invalid_values:
        return True, ''
    msg = 'Invalid values: '
    for i, j, bit in invalid_values:
        msg += '\nrow: {0}, col {1}, value: {2}'.format(i, j, bit)
    return False, msg


def read_matrix(name):
    """\
    Helper function to read a matrix from /ref_matrix. The file extension .txt
    is added automatically.

    :return: A tuple of bytearrays
    """
    matrix = []
    with io.open(os.path.join(os.path.dirname(__file__), 'ref_matrix/{0}.txt'.format(name)), 'rt') as f:
        for row in f:
            matrix.append(bytearray([int(i) for i in row if i != '\n']))
    return tuple(matrix), (len(matrix[0]), len(matrix))
