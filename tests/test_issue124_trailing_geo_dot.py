# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
""""\
Test against PR 124
<https://github.com/heuer/segno/pull/124>
"""
from __future__ import unicode_literals, absolute_import
import pytest
from segno import helpers


def test_remove_trailing_zero_and_dot():
    data = helpers.make_geo_data(38.0, -77.0)
    assert 'geo:38,-77' == data


if __name__ == '__main__':
    pytest.main([__file__])
