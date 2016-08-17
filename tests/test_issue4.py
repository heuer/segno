# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #4.
<https://github.com/heuer/segno/issues/4>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
from nose.tools import ok_, eq_
from segno import consts, encoder


def test_issue_4():
    qr = encoder.encode(0)
    eq_(consts.VERSION_M1, qr.version)
    ok_(qr.error is None)


def test_issue_4_autodetect_micro():
    qr = encoder.encode(1)
    eq_(consts.VERSION_M1, qr.version)
    ok_(qr.error is None)


def test_issue_4_explicit_error():
    qr = encoder.encode(1, error=None)
    eq_(consts.VERSION_M1, qr.version)
    ok_(qr.error is None)


def test_issue_4_explicit_error2():
    qr = encoder.encode(1, error='m')
    eq_(consts.VERSION_M2, qr.version)
    eq_(consts.ERROR_LEVEL_M, qr.error)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
