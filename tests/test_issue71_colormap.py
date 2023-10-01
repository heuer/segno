# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 71
<https://github.com/heuer/segno/issues/71>
"""
from __future__ import absolute_import, unicode_literals
import pytest
from segno import consts, writers


def test_issue71():
    width, height = 45, 45  # Version 7
    cm = writers._make_colormap(width, height, dark='blue', light='white', finder_dark=None, finder_light=None)
    assert cm[consts.TYPE_FINDER_PATTERN_DARK] is None
    assert cm[consts.TYPE_FINDER_PATTERN_LIGHT] is None


if __name__ == '__main__':
    pytest.main([__file__])
