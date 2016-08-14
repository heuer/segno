# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Terminal output related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import io
from nose.tools import ok_
import segno


def test_terminal():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.terminal(out, border=0)
    val = out.getvalue()
    expected = ''.join(['\033[7m  \033[0m'] * 7) + ' ' + '\033[7m  \033[0m'
    ok_(expected, val[:len(expected)])


def terminal_as_matrix(buff, border):
    """\
    Returns the text QR code as list of [0,1] lists.
    """
    res = []
    for l in buff:
        row = [int(i) for i in l]
        res.append(row)
    return res


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
