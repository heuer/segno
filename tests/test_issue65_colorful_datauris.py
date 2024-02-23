#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #65.
<https://github.com/heuer/segno/issues/65>
"""
import io
import base64
import pytest
import segno
from urllib.parse import quote


def test_png_colorful():
    dark = 'darkred'
    data_dark = 'darkorange'
    data_light = 'yellow'
    qr = segno.make('Penny Lane', error='h')
    out = io.BytesIO()
    qr.save(out, 'png', dark=dark, data_dark=data_dark, data_light=data_light)
    data_uri = qr.png_data_uri(dark=dark, data_dark=data_dark,
                               data_light=data_light)
    assert data_uri
    d = base64.b64decode(data_uri[len('data:image/png;base64,'):])
    assert out.getvalue() == d


def test_svg_colorful():
    from segno.writers import _replace_quotes as replace_quotes
    dark = 'darkred'
    data_dark = 'darkorange'
    data_light = 'yellow'
    qr = segno.make('Penny Lane', error='h')
    out = io.BytesIO()
    qr.save(out, 'svg', xmldecl=False, nl=False, dark=dark, data_dark=data_dark,
            data_light=data_light)
    data_uri = qr.svg_data_uri(dark=dark, data_dark=data_dark,
                               data_light=data_light)
    assert data_uri
    d = data_uri[len('data:image/svg+xml;charset=utf-8,'):]
    assert quote(replace_quotes(out.getvalue()), safe=b'') == d


if __name__ == '__main__':
    pytest.main([__file__])
