#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
LaTex output related tests.
"""
import re
import io
import segno


def test_write_tex():
    # Test with default options
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='tex', border=4)
    assert r'\pgfpathmoveto{\pgfqpoint{4pt}{-4pt}}' in out.getvalue()


def test_write_tex_url():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    url = 'http://www.example.org/~xxx#aaa'
    qr.save(out, kind='tex', border=4, url=url)
    assert r'\href{' + url + '}' in out.getvalue()


def test_write_tex_omit_url():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    url = ''
    qr.save(out, kind='tex', border=4, url=url)
    assert r'\href' not in out.getvalue()


def test_write_tex_omit_url2():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='tex', border=4)
    assert r'\href' not in out.getvalue()


def test_write_tex_color():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='tex', border=4)
    assert r'\color' not in out.getvalue()


def test_write_tex_color2():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='tex', border=4, dark='green')
    assert r'\color{green}' in out.getvalue()


_COMMAND_PATTERN = re.compile(r'pgfpath(move|line)to{\\pgfqpoint{(-?[0-9]+)pt}{(-?[0-9]+)pt}')


def tex_as_matrix(buff, border):
    """\
    Returns the LaTeX QR code as list of [0,1] lists.

    :param io.StringIO buff: Buffer to read the matrix from.
    """
    res = []
    last_y = None
    res_row = None
    size = 0
    prev_x = border
    for m in _COMMAND_PATTERN.finditer(buff.getvalue()):
        op, x, y = m.groups()
        x, y = int(x), int(y)
        length = x - prev_x
        prev_x = x
        if y != last_y:
            length = x - border
            if res_row is not None:
                res_row.extend([0] * (size - len(res_row)))
                if not size:
                    size = len(res_row)
            last_y = y
            res_row = []
            res.append(res_row)
        if op == 'move':
            res_row.extend([0] * length)
        elif op == 'line':
            res_row.extend([1] * length)
    res_row.extend([0] * (size - len(res_row)))
    return res


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
