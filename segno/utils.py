# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Utility functions useful for writers or QR Code objects.
"""
from __future__ import absolute_import, unicode_literals


def get_default_border_size(version):
    """\
    Returns the default border size (quiet zone) for the provided version.

    :param int version: 1 .. 40 or a Micro QR Code version constant.
    :rtype: int
    """
    return 4 if version > 0 else 2


def get_border(version, border):
    """\
    Returns `border` if not ``None``, otherwise the default border size for
    the provided QR Code.

    :param int version: 1 .. 40 or a Micro QR Code version constant
    :param int border: The size of the quiet zone or ``None``.

    :rtype: int
    """
    return border if border is not None else get_default_border_size(version)


def get_symbol_size(version, scale=1, border=None):
    """\
    Returns the symbol size (width x height) with the provided border and
    scaling factor.

    :param int version: A version constant.
    :param scale: Indicates the size of a single module (default: 1).
            The size of a module depends on the used output format; i.e.
            in a PNG context, a scaling factor of 2 indicates that a module
            has a size of 2 x 2 pixel. Some outputs (i.e. SVG) accept
            floating point values.
    :type scale: int or float
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :rtype: tuple (width, height)
    """
    if border is None:
        border = get_default_border_size(version)
                                               # M4 = 0, M3 = -1 ...
    dim = version * 4 + 17 if version > 0 else (version + 4) * 2 + 9
    dim += 2 * border
    dim *= scale
    return dim, dim


def matrix_to_lines(matrix, x, y, incby=1):
    """\
    Converts the `matrix` into an iterable of ((x1, y1), (x2, y2)) tuples which
    represent a sequence (horizontal line) of dark modules.

    The path starts at the 1st row of the matrix and moves down to the last
    row.

    :param x: Initial position on the x-axis.
    :param y: Initial position on the y-axis.
    :param incby: Value to move along the y-axis (default: 1).
    :rtype: iterable of (x1, y1), (x2, y2) tuples
    """
    y -= incby  # Move along y-axis so we can simply increment y in the loop
    last_bit = 0x1
    for row in matrix:
        x1 = x
        x2 = x
        y += incby
        for bit in row:
            if last_bit != bit and not bit:
                yield (x1, y), (x2, y)
                x1 = x2
            x2 += 1
            if not bit:
                x1 += 1
            last_bit = bit
        if last_bit:
            yield (x1, y), (x2, y)
            last_bit = 0x0
