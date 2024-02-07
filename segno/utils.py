# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
# type: ignore
"""\
Utility functions useful for writers or QR Code objects.

DOES NOT belong to the public API.
"""
from itertools import chain, repeat
from . import consts

__all__ = ('get_default_border_size', 'get_border', 'get_symbol_size',
           'check_valid_scale', 'check_valid_border', 'matrix_to_lines',
           'matrix_iter', 'matrix_iter_verbose')


def get_default_border_size(matrix_size):
    """\
    Returns the default border size (quiet zone) for the provided version.

    :param tuple(int, int) matrix_size: Tuple of width and height of the matrix.
    :rtype: int
    """
    width, height = matrix_size
    return 4 if width > 17 and width == height else 2


def get_border(matrix_size, border):
    """\
    Returns `border` if not ``None``, otherwise the default border size for
    the provided QR Code.

    :param tuple(int, int) matrix_size: Tuple of width and height of the matrix.
    :param border: The size of the quiet zone or ``None``.
    :type border: int or None

    :rtype: int
    """
    return border if border is not None else get_default_border_size(matrix_size)


def get_symbol_size(matrix_size, scale=1, border=None):
    """\
    Returns the symbol size (width x height) with the provided border and
    scaling factor.

    :param tuple(int, int) matrix_size: Tuple of width and height of the matrix.
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
        border = get_default_border_size(matrix_size)
    width, height = matrix_size
    width += 2 * border
    height += 2 * border
    return width * scale, height * scale


def check_valid_scale(scale):
    """\
    Raises a :py:exc:`ValueError` iff `scale` is negative or zero.

    :param scale: Scaling factor.
    :type scale: float or int
    """
    if scale <= 0:
        raise ValueError('The scale must not be negative or zero. Got: "{0}"'.format(scale))


def check_valid_border(border):
    """\
    Raises a :py:exc:`ValueError` iff `border` is negative.

    :param int border: Indicating the size of the quiet zone.
    """
    if border is not None and (int(border) != border or border < 0):
        raise ValueError('The border must not a non-negative integer value. Got: "{0}"'.format(border))


def matrix_to_lines(matrix, x, y, incby=1):
    """\
    Converts the `matrix` into an iterable of ((x1, y1), (x2, y2)) tuples which
    represent a sequence (horizontal line) of dark modules.

    The path starts at the 1st row of the matrix and moves down to the last row.

    :param matrix: An iterable of bytearrays.
    :param x: Initial position on the x-axis.
    :param y: Initial position on the y-axis.
    :param incby: Value to move along the y-axis (default: 1).
    :rtype: iterable of (x1, y1), (x2, y2) tuples
    """
    y -= incby  # Move along y-axis so we can simply increment y in the loop
    last_bit = 0x1
    for row in matrix:
        x1, x2 = x, x
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


def matrix_iter(matrix, matrix_size, scale=1, border=None):
    """\
    Returns an iterator / generator over the provided matrix which includes
    the border and the scaling factor.

    If either the `scale` or `border` value is invalid, a :py:exc:`ValueError`
    is raised.

    :param matrix: An iterable of bytearrays.
    :param tuple(int, int) matrix_size: Tuple of width and height of the matrix.
    :param int scale: The scaling factor (default: ``1``).
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :raises: :py:exc:`ValueError` if an illegal scale or border value is provided
    """
    check_valid_border(border)
    scale = int(scale)
    check_valid_scale(scale)
    border = get_border(matrix_size, border)
    width, height = matrix_size
    border_row = [0x0] * width
    width_range, height_range = range(-border, width + border), range(-border, height + border)
    for i in height_range:
        r = matrix[i] if 0 <= i < height else border_row
        row = tuple(chain.from_iterable(repeat(r[j] if 0 <= j < width else 0x0, scale) for j in width_range))
        for s in repeat(None, scale):
            yield row


def matrix_iter_verbose(matrix, matrix_size, scale=1, border=None):
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
    :param tuple(int, int) matrix_size: Tuple of width and height of the matrix.
    :param int scale: The scaling factor (default: ``1``).
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :raises: :py:exc:`ValueError` if an illegal scale or border value is provided
    """
    from segno import encoder
    check_valid_border(border)
    scale = int(scale)
    check_valid_scale(scale)
    border = get_border(matrix_size, border)
    width, height = matrix_size
    is_square = width == height
    is_micro = is_square and width < 21  # 21 == QR Code version 1
    # Create an empty matrix with invalid 0x2 values
    alignment_matrix = encoder.make_matrix(width, height, reserve_regions=False, add_timing=False)
    encoder.add_alignment_patterns(alignment_matrix, width, height)

    def get_bit(i, j):
        # Check if we operate upon the matrix or the "virtual" border
        if 0 <= i < height and 0 <= j < width:
            val = matrix[i][j]
            if not is_micro:
                # Alignment pattern
                alignment_val = alignment_matrix[i][j]
                if alignment_val != 0x2:
                    return (consts.TYPE_ALIGNMENT_PATTERN_LIGHT, consts.TYPE_ALIGNMENT_PATTERN_DARK)[alignment_val]
                if is_square and width > 41:  # QR Codes < version 7 do not carry any version information
                    if i < 6 and width - 12 < j < width - 8 \
                            or height - 12 < i < height - 8 and j < 6:
                        return (consts.TYPE_VERSION_LIGHT, consts.TYPE_VERSION_DARK)[val]
                # Dark module
                if i == height - 8 and j == 8:
                    return consts.TYPE_DARKMODULE
            # Timing - IMPORTANT: Check alignment (see above) in advance!
            if not is_micro and ((i == 6 and 7 < j < width - 8) or (j == 6 and 7 < i < height - 8)) \
                    or is_micro and (i == 0 and j > 7 or j == 0 and i > 7):
                return (consts.TYPE_TIMING_LIGHT, consts.TYPE_TIMING_DARK)[val]
            # Format - IMPORTANT: Check timing (see above) in advance!
            if i == 8 and (j < 9 or (not is_micro and j > width - 10)) \
                    or j == 8 and (i < 8 or not is_micro and i > height - 9):
                return (consts.TYPE_FORMAT_LIGHT, consts.TYPE_FORMAT_DARK)[val]
            # Finder pattern
            # top left             top right
            if i < 7 and (j < 7 or (not is_micro and j > width - 8)) \
                    or not is_micro and i > height - 8 and j < 7:  # bottom left
                return (consts.TYPE_FINDER_PATTERN_LIGHT, consts.TYPE_FINDER_PATTERN_DARK)[val]
            # Separator
            # top left              top right
            if i < 8 and (j < 8 or (not is_micro and j > width - 9)) \
                    or not is_micro and (i > height - 9 and j < 8):  # bottom left
                return consts.TYPE_SEPARATOR
            return (consts.TYPE_DATA_LIGHT, consts.TYPE_DATA_DARK)[val]
        else:
            return consts.TYPE_QUIET_ZONE

    width_range, height_range = range(-border, width + border), range(-border, height + border)
    for i in height_range:
        row = tuple(chain.from_iterable(repeat(get_bit(i, j), scale) for j in width_range))
        for s in repeat(None, scale):
            yield row
