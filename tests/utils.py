# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Utility functions for test cases.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""


def matrix_looks_valid(matrix):
    """\
    Returns if the matrix contains just ``0x0`` and ``0x1`` values.
    Does not check if the the matrix represents a valid (Micro) QR Code.

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
