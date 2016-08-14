# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Text output related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import io
from itertools import islice
from nose.tools import eq_
import segno


def test_write_txt():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.txt(out, border=0)
    expected = '11111110011'
    val = out.getvalue()
    eq_(expected, val[:len(expected)])


def txt_as_matrix(buff, border):
    """\
    Returns the text QR code as list of [0,1] lists.

    :param io.StringIO buff: Buffer to read the matrix from.
    """
    res = []
    code = buff.getvalue().splitlines()
    len_without_border = len(code) - border
    for l in islice(code, border, len_without_border):
        res.append([int(clr) for clr in islice(l, border, len_without_border)])
    return res


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
