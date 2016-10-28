# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
XBM related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import re
import io
from itertools import islice
import pytest
import segno


def test_defaults():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='xbm')
    width, height = qr.symbol_size()
    assert '#define img_width {0}'.format(width) in out.getvalue()
    assert '#define img_height {0}'.format(height) in out.getvalue()
    assert 'static unsigned char img_bits[] = {' in out.getvalue()


def test_name():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='xbm', name='bla_bla')
    width, height = qr.symbol_size()
    assert '#define bla_bla_width {0}'.format(width) in out.getvalue()
    assert '#define bla_bla_height {0}'.format(height) in out.getvalue()
    assert 'static unsigned char bla_bla_bits[] = {' in out.getvalue()


if __name__ == '__main__':
    pytest.main([__file__])
