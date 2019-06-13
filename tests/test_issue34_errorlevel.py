# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 34
<https://github.com/heuer/segno/issues/34>
"""
from __future__ import absolute_import, unicode_literals
import pytest
import segno
from segno import consts
from segno import encoder
try:
    from .tutils import read_matrix
except (ValueError, SystemError):  # Attempted relative import in non-package
    from tutils import read_matrix


def test_m3_wikipedia():
    qr = segno.make('Wikipedia', version='m3')
    assert 'M3-L' == qr.designator
    ref_matrix = read_matrix('issue-33-m3-l-wikipedia')
    assert ref_matrix == qr.matrix


if __name__ == '__main__':
    pytest.main([__file__])
