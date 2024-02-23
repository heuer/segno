#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 34
<https://github.com/heuer/segno/issues/34>
"""
import pytest
import segno
try:
    from .tutils import read_matrix
# Attempted relative import in non-package
except (ValueError, SystemError, ImportError):
    from tutils import read_matrix


def test_m3_wikipedia():
    qr = segno.make('Wikipedia', version='m3')
    assert 'M3-L' == qr.designator
    ref_matrix = read_matrix('issue-33-m3-l-wikipedia')[0]
    assert ref_matrix == qr.matrix


if __name__ == '__main__':
    pytest.main([__file__])
