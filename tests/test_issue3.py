# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #3.
<https://github.com/heuer/segno/issues/3>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import io
from nose.tools import ok_, eq_
import segno


def test_issue_3():
    qr = segno.make_micro('test')
    eq_('M3', qr.version)
    # This fails since PNG operates with a fixed set of two colors
    qr.save(io.BytesIO(), kind='png')


def test_issue_3_autodetect_micro():
    qr = segno.make('test')
    eq_('M3', qr.version)
    # This fails since PNG operates with a fixed set of two colors
    qr.save(io.BytesIO(), kind='png')


def test_issue_3_matrix():
    def check(row_no, row):
        for i in range(len(row)):
            ok_(row[i] in (0x0, 0x1), 'Error in row {0}. Found "{1}" at {2}' \
                                      .format(row_no, row[i], i))
    qr = segno.make_micro('test')
    for row_no, row in enumerate(qr.matrix):
        yield check, row_no, row


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
