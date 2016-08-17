# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
EPS related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import re
import io
from nose.tools import ok_, raises
import segno


@raises(ValueError)
def test_illegal_color_float():
    color = (.1, 1.1, .1)
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', color=color)


@raises(ValueError)
def test_illegal_color_float2():
    color = (-.1, 1.0, .1)
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', color=color)


@raises(ValueError)
def test_illegal_color_int():
    color = (255, 255, 256)
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', color=color)


@raises(ValueError)
def test_illegal_color_int2():
    color = (-1, 1, 1)
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', color=color)


def test_default_color():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps')
    ok_('setrgbcolor' not in out.getvalue())


def test_color():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', color='#195805')
    ok_('setrgbcolor' in out.getvalue())


def test_color_omit_black():
    qr = segno.make_qr('test')
    out = io.StringIO()
    # Black does not need setrgbcolor since it is the default stroke color
    qr.save(out, kind='eps', color='#000')
    ok_('setrgbcolor' not in out.getvalue())


def test_color_omit_black2():
    qr = segno.make_qr('test')
    out = io.StringIO()
    # Black does not need setrgbcolor since it is the default stroke color
    qr.save(out, kind='eps', color='Black')
    ok_('setrgbcolor' not in out.getvalue())


def test_color_omit_black3():
    qr = segno.make_qr('test')
    out = io.StringIO()
    # Black does not need setrgbcolor since it is the default stroke color
    qr.save(out, kind='eps', color=(0, 0, 0))
    ok_('setrgbcolor' not in out.getvalue())


def test_background():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', background='#EEE')
    ok_('setrgbcolor' in out.getvalue())
    ok_('clippath' in out.getvalue())


def test_default_scale():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps')
    ok_('scale' not in out.getvalue())


def test_scale():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', scale=2)
    ok_('2 2 scale' in out.getvalue())


def test_scale_float():
    qr = segno.make_qr('test')
    out = io.StringIO()
    scale = 1.34
    qr.save(out, kind='eps', scale=scale)
    ok_('{0} {0} scale'.format(scale) in out.getvalue())


def eps_as_matrix(buff, border):
    """\
    Reads the path in the EPS and returns it as list of 0, 1 lists.

    :param io.StringIO buff: Buffer to read the matrix from.
    """
    eps = buff.getvalue()
    h, w = re.search(r'^%%BoundingBox: 0 0 ([0-9]+) ([0-9]+)', eps,
                     flags=re.MULTILINE).groups()
    if h != w:
        raise ValueError('Expected equal height/width, got height="{}" width="{}"'.format(h, w))
    size = int(w) - 2 * border
    path = re.search(r'^newpath[\s+](.+?)(^stroke)', eps,
                     flags=re.DOTALL|re.MULTILINE).group(1).strip()
    res = []
    res_row = None
    absolute_x = -border
    for x, y, op in re.findall(r'(\-?[0-9]+(?:\.[0-9]+)?)\s+(\-?[0-9]+(?:\.[0-9]+)?)\s+([a-z]+)', path):
        x = int(x)
        y = float(y)
        if y != 0.0:  # New row
            if res_row:
                res_row.extend([0] * (size - len(res_row)))
            res_row = []
            res.append(res_row)
        if op == 'moveto':
            absolute_x = 0
            if x != border:
                raise ValueError('Unexpected border width. Expected "{}", got "{}"'.format(border, x))
        else:
            absolute_x += x
            bit = 0 if op == 'm' else 1
            length = absolute_x if x < 0 else x
            res_row.extend([bit] * length)
    res_row.extend([0] * (size - len(res_row)))
    return res


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
