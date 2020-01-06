# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test if the keywords "color" and "background" are still supported.
"""
from __future__ import unicode_literals, absolute_import
import os
import io
import tempfile
import pytest
import segno
from segno import cli


def test_colorbackground():
    qr = segno.make('The Beatles')
    out_new = io.BytesIO()
    out_old = io.BytesIO()
    qr.save(out_new, kind='png', dark='blue', light='yellow')
    qr.save(out_old, kind='png', color='blue', background='yellow')
    assert out_new.getvalue() == out_old.getvalue()


def test_colorbackground_cli():
    content = 'The Beatles'
    qr = segno.make(content, micro=False)
    out_new = io.BytesIO()
    qr.save(out_new, kind='png', scale=10, dark='blue', light=None)
    f = tempfile.NamedTemporaryFile('w', suffix='.png', delete=False)
    f.close()
    fn = f.name
    cli.main(['--color=blue', '--background=transparent', '--scale=10', '--output={0}'.format(fn), content])
    with open(fn, 'rb') as f:
        content_cli = f.read()
    os.unlink(fn)
    assert out_new.getvalue() == content_cli


if __name__ == '__main__':
    pytest.main([__file__])
