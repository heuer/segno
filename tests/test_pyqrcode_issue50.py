# (c) Martijn van Rheenen
# BSD License
"""\
Tests against <https://github.com/mnooner256/pyqrcode/issues/50>

This test was created by Martijn van Rheenen <https://github.com/rheenen>
for PyQRCode. Adapted to Segno to check if it has the same problem.
"""
import pytest
import segno


class FakeString(str):
    """\
    Create a mock class that *acts* like a string as far as needed for the
    QRCode constructor, but raises an exception in case shiftjis encoding is
    used on its value.

    This mimics the behaviour of Python on an environment where this codec is
    not installed.
    """
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)

    def encode(self, encoding=None, errors='strict'):
        if encoding == 'shiftjis':
            raise LookupError("unknown encoding: shiftjis")
        return super(FakeString, self).encode(encoding, errors)


def test_constructing_without_shiftjis_encoding_available():
    content = FakeString("t123456789")
    code = segno.make(content, error="Q")
    assert 'byte' == code.mode


if __name__ == '__main__':
    pytest.main([__file__])
