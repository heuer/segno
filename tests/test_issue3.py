#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #3.
<https://github.com/heuer/segno/issues/3>
"""
import io
import segno
try:
    from .tutils import matrix_looks_valid
# Attempted relative import in non-package
except (ValueError, SystemError, ImportError):
    from tutils import matrix_looks_valid


def test_issue_3():
    qr = segno.make_micro('test')
    assert 'M3' == qr.version
    # This fails since PNG operates with a fixed set of two colors
    qr.save(io.BytesIO(), kind='png')


def test_issue_3_autodetect_micro():
    qr = segno.make('test')
    assert 'M3' == qr.version
    # This fails since PNG operates with a fixed set of two colors
    qr.save(io.BytesIO(), kind='png')


def test_issue_3_matrix():
    qr = segno.make_micro('test')
    is_ok, msg = matrix_looks_valid(qr.matrix)
    assert is_ok, msg


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
