#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Text output related tests.
"""
import io
from itertools import islice
import segno


def test_write_txt():
    # Test with default options
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='txt', border=0)
    expected = '11111110011'
    val = out.getvalue()
    assert expected == val[:len(expected)]


def txt_as_matrix(buff, border):
    """\
    Returns the text QR code as list of [0,1] lists.

    :param io.StringIO buff: Buffer to read the matrix from.
    """
    res = []
    code = buff.getvalue().splitlines()
    len_without_border = len(code) - border
    for line in islice(code, border, len_without_border):
        res.append([int(clr) for clr in islice(line, border,
                                               len_without_border)])
    return res


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
