# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Utility functions useful for writers or QR Code objects.
"""
from __future__ import absolute_import, unicode_literals
from . import consts
from itertools import chain
try:  # pragma: no cover
    range = xrange
except NameError:  # pragma: no cover
    pass


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


def check_valid_scale(scale):
    """\
    Raises a :py:exc:`ValueError` iff `scale` is negative or zero.

    :param scale: float or integer indicating a scaling factor.
    """
    if scale <= 0:
        raise ValueError('The scale must not be negative or zero. '
                         'Got: "{0}"'.format(scale))


def check_valid_border(border):
    """\
    Raises a ValueError iff `border` is negative.

    :param int border: Indicating the size of the quiet zone.
    """
    if border is not None and (int(border) != border or border < 0):
        raise ValueError('The border must not a non-negative integer value. '
                         'Got: "{0}"'.format(border))


def matrix_to_lines(matrix, x, y, incby=1):
    """\
    Converts the `matrix` into an iterable of ((x1, y1), (x2, y2)) tuples which
    represent a sequence (horizontal line) of dark modules.

    The path starts at the 1st row of the matrix and moves down to the last
    row.

    :param matrix: An iterable of bytearrays.
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


def matrix_iter(matrix, version, scale=1, border=None):
    """\
    Returns an iterator / generator over the provided matrix which includes
    the border and the scaling factor.

    If either the `scale` or `border` value is invalid, a :py:exc:`ValueError`
    is raised.

    :param matrix: An iterable of bytearrays.
    :param int version: A version constant.
    :param int scale: The scaling factor (default: ``1``).
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :raises: :py:exc:`ValueError` if an illegal scale or border value is provided
    """
    check_valid_border(border)
    scale = int(scale)
    check_valid_scale(scale)
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale=1, border=0)

    def get_bit(i, j):
        return 0x1 if (0 <= i < height and 0 <= j < width and matrix[i][j]) else 0x0

    for i in range(-border, height + border):
        for s in range(scale):
            yield chain.from_iterable(([get_bit(i, j)] * scale for j in range(-border, width + border)))


# Constants for detailed iterator, see utils.matrix_iter_detail
TYPE_FINDER_PATTERN_LIGHT = 6
"""\
Light finder module
"""
TYPE_FINDER_PATTERN_DARK = TYPE_FINDER_PATTERN_LIGHT << 8
"""\
Dark finder module.
"""
TYPE_SEPARATOR = 8
"""\
Separator around the finder patterns (light module)
"""
TYPE_ALIGNMENT_PATTERN_LIGHT = 10
"""\
Light alignment pattern module.
"""
TYPE_ALIGNMENT_PATTERN_DARK = TYPE_ALIGNMENT_PATTERN_LIGHT << 8
"""\
Dark alignment pattern module.
"""
TYPE_TIMING_LIGHT = 12
"""\
Light timing pattern module.
"""
TYPE_TIMING_DARK = TYPE_TIMING_LIGHT << 8
"""\
Dark timing patten module.
"""
TYPE_FORMAT_LIGHT = 14
"""\
Light format information module.
"""
TYPE_FORMAT_DARK = TYPE_FORMAT_LIGHT << 8
"""\
Dark format information module.
"""
TYPE_VERSION_LIGHT = 16
"""\
Light version information module.
"""
TYPE_VERSION_DARK = TYPE_VERSION_LIGHT << 8
"""\
Dark version information module.
"""
TYPE_DARKMODULE = 512
"""\
A single dark module which occurs in QR Codes (but not in Micro QR Codes).
"""
TYPE_DATA_LIGHT = 4
"""\
Light module in the encoding area (either a data module or an error correction module).
"""
TYPE_DATA_DARK = TYPE_DATA_LIGHT << 8
"""\
Dark module in the encoding area (either a data module or an error correction module).
"""
TYPE_QUIET_ZONE = 18
"""\
Border of light modules.
"""

def matrix_iter_detail(matrix, version, scale=1, border=None):
    """\
    Returns an iterator / generator over the provided matrix which includes
    the border and the scaling factor.

    This iterator / generator returns different values for dark / light modules
    and therefor the different parts (like the finder patterns, alignment patterns etc.)
    are distinguishable. If this information isn't necessary, use the
    :py:func:`matrix_iter()` function because it is much cheaper and faster.

    If either the `scale` or `border` value is invalid, a py:exc:`ValueError`
    is raised.

    :param matrix: An iterable of bytearrays.
    :param int version: A version constant.
    :param int scale: The scaling factor (default: ``1``).
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :raises: :py:exc:`ValueError` if an illegal scale or border value is provided

    """
    from segno import encoder
    check_valid_border(border)
    scale = int(scale)
    check_valid_scale(scale)
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale=1, border=0)
    is_micro = version < 1
    # Create an empty matrix with invalid 0x2 values
    alignment_matrix = encoder.make_matrix(version, reserve_regions=False, add_timing=False)
    encoder.add_alignment_patterns(alignment_matrix, version)

    def get_bit(i, j):
        # Check if we operate upon the matrix or the "virtual" border
        if 0 <= i < height and 0 <= j < width:
            val = matrix[i][j]
            if not is_micro:
                # Alignment pattern
                alignment_val = alignment_matrix[i][j]
                if alignment_val != 0x2:
                    return (TYPE_ALIGNMENT_PATTERN_LIGHT, TYPE_ALIGNMENT_PATTERN_DARK)[alignment_val]
                if version > 6:  # Version information
                    if i < 6 and width - 12 < j < width - 8 \
                            or height - 12 < i < height - 8 and j < 6:
                        return (TYPE_VERSION_LIGHT, TYPE_VERSION_DARK)[val]
                # Dark module
                if i == height - 8 and j == 8:
                    return TYPE_DARKMODULE
            # Timing - IMPORTANT: Check alignment (see above) in advance!
            if not is_micro and ((i == 6 and j > 7 and j < width - 8) or (j == 6 and i > 7 and i < height - 8)) \
                    or is_micro and (i == 0 and j > 7 or j == 0 and i > 7):
                return (TYPE_TIMING_LIGHT, TYPE_TIMING_DARK)[val]
            # Format - IMPORTANT: Check timing (see above) in advance!
            if i == 8 and (j < 9 or (not is_micro and j > width - 10)) \
                    or j == 8 and (i < 8 or not is_micro and i > height - 9):
                return (TYPE_FORMAT_LIGHT, TYPE_FORMAT_DARK)[val]
            # Finder pattern
            # top left             top right
            if i < 7 and (j < 7 or (not is_micro and j > width - 8)) \
                or not is_micro and i > height - 8 and j < 7:  # bottom left
                return (TYPE_FINDER_PATTERN_LIGHT, TYPE_FINDER_PATTERN_DARK)[val]
            # Separator
            # top left              top right
            if i < 8 and (j < 8 or (not is_micro and j > width - 9)) \
                or not is_micro and (i > height - 9 and j < 8):  # bottom left
                return TYPE_SEPARATOR
            return (TYPE_DATA_LIGHT, TYPE_DATA_DARK)[val]
        else:
            return TYPE_QUIET_ZONE

    for i in range(-border, height + border):
        for s in range(scale):
            yield chain.from_iterable(([get_bit(i, j)] * scale for j in range(-border, width + border)))
