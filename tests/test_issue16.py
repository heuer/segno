# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #16.
<https://github.com/heuer/segno/issues/16>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import segno


def test_boost_error_automatic():
    qr = segno.make_qr('ABCDEF')
    assert '1-H' == qr.designator


def test_boost_error_automatic_disabled():
    qr = segno.make_qr('ABCDEF', boost_error=False)
    assert '1-M' == qr.designator


def test_boost_error_automatic_arg_error():
    qr = segno.make_qr('ABCDEF', error='l')
    assert '1-M' == qr.designator


def test_boost_error_disabled_arg_error():
    qr = segno.make_qr('ABCDEF', error='l', boost_error=False)
    assert '1-L' == qr.designator


if __name__ == '__main__':
    import pytest
    pytest.main(['-x', __file__])

