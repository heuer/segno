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
import re
import segno


def test_terminal():
    # Test with default options
    qr = segno.make_qr('test')
    expected = ''
    for bit in qr.matrix[0]:
        if not bit:
            expected += '\033[7m  \033[0m'
        else:
            expected += '\033[49m  \033[0m'
    out = io.StringIO()
    qr.terminal(out, border=0)
    val = out.getvalue()
    assert expected == val[:len(expected)]



_COLOR_PATTERN = re.compile(r'\033\[\d+m\s+\033\[0m')

def terminal_as_matrix(buff, border):
    """\
    Returns the text QR code as list of [0,1] lists.
    """
    res = []
    colors = ('\033[7m  \033[0m', '\033[49m  \033[0m')
    code = buff.getvalue().splitlines()
    h_border = border * len(colors[0])
    for l in code[border:len(code) - border]:
        res.append([colors.index(color) for color in _COLOR_PATTERN.findall(l[h_border:len(l) - h_border])])
    return res


if __name__ == '__main__':
    import pytest
    pytest.main(['-x', __file__])

