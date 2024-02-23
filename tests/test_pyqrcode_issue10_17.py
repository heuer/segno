#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue <https://github.com/mnooner256/pyqrcode/issues/17#issuecomment-419731805>
and <https://github.com/heuer/pyqrcode/issues/10>
"""
import segno


def test_issue_10_17():
    qr = segno.make_qr('John’s Pizza')
    assert 1 == qr.version
    assert 'byte' == qr.mode
    assert 'M' == qr.error


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
