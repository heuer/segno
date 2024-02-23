#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
EPS related tests.
"""
import re
import io
import pytest
import segno


def test_illegal_color_float():
    color = (.1, 1.1, .1)
    qr = segno.make_qr('test')
    out = io.StringIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='eps', dark=color)


def test_illegal_color_float2():
    color = (-.1, 1.0, .1)
    qr = segno.make_qr('test')
    out = io.StringIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='eps', dark=color)


def test_illegal_color_int():
    color = (255, 255, 256)
    qr = segno.make_qr('test')
    out = io.StringIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='eps', dark=color)


def test_illegal_color_int2():
    color = (-1, 1, 1)
    qr = segno.make_qr('test')
    out = io.StringIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='eps', dark=color)


def test_default_color():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps')
    assert 'setrgbcolor' not in out.getvalue()


def test_color():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', dark='#195805')
    assert 'setrgbcolor' in out.getvalue()


def test_color_omit_black():
    qr = segno.make_qr('test')
    out = io.StringIO()
    # Black does not need setrgbcolor since it is the default stroke color
    qr.save(out, kind='eps', dark='#000')
    assert 'setrgbcolor' not in out.getvalue()


def test_color_omit_black2():
    qr = segno.make_qr('test')
    out = io.StringIO()
    # Black does not need setrgbcolor since it is the default stroke color
    qr.save(out, kind='eps', dark='Black')
    assert 'setrgbcolor' not in out.getvalue()


def test_color_omit_black3():
    qr = segno.make_qr('test')
    out = io.StringIO()
    # Black does not need setrgbcolor since it is the default stroke color
    qr.save(out, kind='eps', dark=(0, 0, 0))
    assert 'setrgbcolor' not in out.getvalue()


def test_background():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', light='#EEE')
    assert 'setrgbcolor' in out.getvalue()
    assert 'clippath' in out.getvalue()


def test_default_scale():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps')
    assert 'scale' not in out.getvalue()


def test_scale():
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.save(out, kind='eps', scale=2)
    assert '2 2 scale' in out.getvalue()


def test_scale_float():
    qr = segno.make_qr('test')
    out = io.StringIO()
    scale = 1.34
    qr.save(out, kind='eps', scale=scale)
    assert f'{scale} {scale} scale' in out.getvalue()


def eps_as_matrix(buff, border):
    """\
    Reads the path in the EPS and returns it as list of 0, 1 lists.

    :param io.StringIO buff: Buffer to read the matrix from.
    """
    eps = buff.getvalue()
    h, w = re.search(r'^%%BoundingBox: 0 0 ([0-9]+) ([0-9]+)', eps,
                     flags=re.MULTILINE).groups()
    if h != w:
        raise ValueError(f'Expected equal height/width, got height="{h}" width="{w}"')
    size = int(w) - 2 * border
    path = re.search(r'^newpath[\s+](.+?)(^stroke)', eps,
                     flags=re.DOTALL | re.MULTILINE).group(1).strip()
    res = []
    res_row = None
    absolute_x = -border
    for x, y, op in re.findall(r'(-?[0-9]+(?:\.[0-9]+)?)\s+(-?[0-9]+(?:\.[0-9]+)?)\s+([a-z]+)', path):
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
                raise ValueError(f'Unexpected border width. Expected "{border}", got "{x}"')
        else:
            absolute_x += x
            bit = 0 if op == 'm' else 1
            length = absolute_x if x < 0 else x
            res_row.extend([bit] * length)
    res_row.extend([0] * (size - len(res_row)))
    return res


if __name__ == '__main__':
    pytest.main([__file__])
