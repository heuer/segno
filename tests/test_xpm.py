#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
XPM output related tests.
"""
import io
import re
import segno


def test_write_xpm_indicator():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='xpm')
    expected = '/* XPM */\n'
    val = out.getvalue()
    assert expected == val[:len(expected)]


def test_dark_transparent():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='xpm', dark=None, light='white')
    expected = '/* XPM */\n'
    val = out.getvalue()
    assert expected == val[:len(expected)]
    assert re.search(r'^"X c None"', val, flags=re.MULTILINE)


def test_light_transparent():
    qr = segno.make_qr('test', error='m', boost_error=False)
    out = io.StringIO()
    qr.save(out, kind='xpm', light=None)
    expected = '/* XPM */\n'
    val = out.getvalue()
    assert expected == val[:len(expected)]
    assert re.search(r'^"  c None"', val, flags=re.MULTILINE)


_DATA_PATTERN = re.compile(r'{([^}]+)};')


def _img_data(s):
    m = _DATA_PATTERN.search(s)
    data = m.group(1).replace('"', '').replace('\n', '').split(',')
    return data


def test_write_xpm_width_height():
    scale = 5
    border = 2
    qr = segno.make_qr('test')
    width, height = qr.symbol_size(scale=scale, border=border)
    out = io.StringIO()
    qr.save(out, kind='xpm', border=border, scale=scale)
    img_data = _img_data(out.getvalue())[0]
    assert img_data.startswith(f'{width} {height}')


def xpm_as_matrix(buff, border):
    """\
    Returns the XPM QR code as list of [0, 1] lists.

    :param io.StringIO buff: Buffer to read the matrix from.
    """
    res = []
    img_data = _img_data(buff.getvalue())
    height = int(img_data[0].split(' ')[0])
    img_data = img_data[3:]
    for i, row in enumerate(img_data):
        if i < border:
            continue
        if i >= height - border:
            break
        r = row[border:-border] if border else row
        res.append([(1 if b == 'X' else 0) for b in r])
    return res


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
