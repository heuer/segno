#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue <https://github.com/pyqrcode/pyqrcodeNG/pull/13/>.

The initial test was created by Mathieu <https://github.com/albatros69>,
see the above mentioned pull request.

Adapted for Segno to check if it suffers from the same problem.
"""
import segno


def test_autodetect():
    data = 'Émetteur'
    qr = segno.make(data)
    assert qr.mode == 'byte'


def test_encoding():
    encoding = 'iso-8859-15'
    data = 'Émetteur'
    qr = segno.make(data.encode(encoding))
    assert qr.mode == 'byte'
    qr2 = segno.make(data, encoding=encoding)
    assert qr2 == qr


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
