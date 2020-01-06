# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Module types (DEPRECATED, use segno.consts).

To distinguish between dark and light modules without taking the concrete
value into account, use::

    if m >> 8:
        print('dark module')

    if not m >> 8:
        print('light module')
"""
from . import consts
import warnings

warnings.warn('This module is deprecated since 0.3.6. Use the constants in segno.consts', DeprecationWarning)

TYPE_FINDER_PATTERN_LIGHT = consts.TYPE_FINDER_PATTERN_LIGHT
TYPE_FINDER_PATTERN_DARK = consts.TYPE_FINDER_PATTERN_DARK
TYPE_SEPARATOR = consts.TYPE_SEPARATOR
TYPE_ALIGNMENT_PATTERN_LIGHT = consts.TYPE_ALIGNMENT_PATTERN_LIGHT
TYPE_ALIGNMENT_PATTERN_DARK = consts.TYPE_ALIGNMENT_PATTERN_DARK
TYPE_TIMING_LIGHT = consts.TYPE_TIMING_LIGHT
TYPE_TIMING_DARK = consts.TYPE_TIMING_DARK
TYPE_FORMAT_LIGHT = consts.TYPE_FORMAT_LIGHT
TYPE_FORMAT_DARK = consts.TYPE_FORMAT_DARK
TYPE_VERSION_LIGHT = consts.TYPE_VERSION_LIGHT
TYPE_VERSION_DARK = consts.TYPE_VERSION_DARK
TYPE_DARKMODULE = consts.TYPE_DARKMODULE
TYPE_DATA_LIGHT = consts.TYPE_DATA_LIGHT
TYPE_DATA_DARK = consts.TYPE_DATA_DARK
TYPE_QUIET_ZONE = consts.TYPE_QUIET_ZONE