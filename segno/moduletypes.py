# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Module types (EXPERIMENTAL).

To distinguish between dark and light modules without taking the concrete
value into account, use::

    if m >> 8:
        print('dark module')

    if not m >> 8:
        print('light module')
"""
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
