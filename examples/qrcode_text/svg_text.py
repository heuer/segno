# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Example how to add additional text to a SVG QR code.
"""
import io
import re
from xml.sax.saxutils import escape
import segno
from segno.writers import _color_to_webcolor as webcolor


def qr_with_text(qrcode: segno.QRCode, *, text: str = None, font_size: int = 12,
                 font_color=False, line_spacing: int = None, scale: int = 1,
                 border: int = None, dark='#000', light='#fff', finder_dark=False,
                 finder_light=False, data_dark=False, data_light=False,
                 version_dark=False, version_light=False, format_dark=False,
                 format_light=False, alignment_dark=False, alignment_light=False,
                 timing_dark=False, timing_light=False, separator=False,
                 dark_module=False, quiet_zone=False, **kw) -> io.BytesIO:
    """\
    Adds a text (i.e. the content of the QR code) to the QR code.

    See `segno.QRCode.save <https://segno.readthedocs.io/en/latest/api.html#segno.QRCode.save>`_
    and `SVG <https://segno.readthedocs.io/en/latest/api.html#svg>`_ for a detailed
    description of the parameters.

    :param segno.QRCode qrcode: The QR code.
    :param str text: The text to add to the QR code.
    :param int font_size: Font size.
    :param font_color: See dark for valid values.
    :param int line_spacing: Spacing between the lines. If not provided, it
            is the half of the font size.
    :param scale: The scale.
    :param int border: Number indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for Micro QR Codes).
    :param dark: Color of the dark modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as hexadecimal
            format (``#RGB``, ``#RRGGBB`` ``RRGGBBAA``), or web color
            name (i.e. ``red``).
    :param light: Color of the light modules (default: white).
            See `color` for valid values. If light is set to ``None`` the
            light modules will be transparent.
    :param finder_dark: Color of the dark finder modules (default: same as ``dark``)
    :param finder_light: Color of the light finder modules (default: same as ``light``)
    :param data_dark: Color of the dark data modules (default: same as ``dark``)
    :param data_light: Color of the light data modules (default: same as ``light``)
    :param version_dark: Color of the dark version modules (default: same as ``dark``)
    :param version_light: Color of the light version modules (default: same as ``light``)
    :param format_dark: Color of the dark format modules (default: same as ``dark``)
    :param format_light: Color of the light format modules (default: same as ``light``)
    :param alignment_dark: Color of the dark alignment modules (default: same as ``dark``)
    :param alignment_light: Color of the light alignment modules (default: same as ``light``)
    :param timing_dark: Color of the dark timing pattern modules (default: same as ``dark``)
    :param timing_light: Color of the light timing pattern modules (default: same as ``light``)
    :param separator: Color of the separator (default: same as ``light``)
    :param dark_module: Color of the dark module (default: same as ``dark``)
    :param quiet_zone: Color of the quiet zone modules (default: same as ``light``)
    """
    def calc_font_size(txt) -> int:
        return round(len(txt) * font_size / 1.5), font_size

    svg = io.BytesIO()
    qrcode.save(svg, kind='svg', scale=scale, border=border, dark=dark,
                light=light, finder_dark=finder_dark, finder_light=finder_light,
                data_dark=data_dark, data_light=data_light, version_dark=version_dark,
                version_light=version_light, format_dark=format_dark,
                format_light=format_light, alignment_dark=alignment_dark,
                alignment_light=alignment_light, timing_dark=timing_dark,
                timing_light=timing_light, separator=separator,
                dark_module=dark_module, quiet_zone=quiet_zone, **kw)
    svg.seek(0)
    if text is None:
        text = kw.get('title')
    if text is None:
        # That was easy, nothing to do, just return the SVG
        return svg
    encoding = kw.get('encoding', 'utf-8')
    qr_width, qr_height = qrcode.symbol_size(scale, border)
    width, height = qr_width, qr_height
    text_buff = io.BytesIO()
    write = text_buff.write
    write_str = lambda s: write(s.encode(encoding))
    border = border if border is not None else qrcode.default_border_size
    border_offset = scale * border
    font_color = webcolor(font_color or dark)
    write_str('<text y="{}" font-size="{}" font-family="mono" fill="{}">'
              .format(qr_height, font_size, font_color))
    line_spacing = line_spacing or font_size // 2
    for line in text.splitlines():
        write_str('<tspan x="{}" dy="{}">'.format(border_offset, font_size + line_spacing))
        write_str(escape(line))
        write(b'</tspan>')
        fw, fh = calc_font_size(line)
        if fw > width:
            width = fw
        height += fh + line_spacing
    height += line_spacing
    write(b'</text></svg>')
    # Add the text to the SVG generated by Segno.
    # The </svg> is part of the text_buff
    res = re.sub(b'</svg>', text_buff.getvalue(), svg.getvalue())
    res = re.sub('width="{}"'.format(qr_width).encode(encoding),
                 'width="{}"'.format(width).encode(encoding), res)
    res = re.sub('height="{}"'.format(qr_height).encode(encoding),
                 'height="{}"'.format(height).encode(encoding), res)
    svg = io.BytesIO(res)
    svg.seek(0)
    return svg


if __name__ == '__main__':
    content = 'If the rain comes\n' \
              'They run and hide their heads\n' \
              'They might as well be dead\n' \
              'If the rain comes\n' \
              'If the rain comes'
    qr = segno.make(content)
    svg = qr_with_text(qr, text=content, scale=6, dark='darkblue', light='#eee',
                       data_dark='steelblue').getvalue()
    with open('rain-1.svg', 'wb') as f:
        f.write(svg)
    svg = qr_with_text(qr, text=content, scale=6).getvalue()
    with open('rain-2.svg', 'wb') as f:
        f.write(svg)
    svg = qr_with_text(qr, text=content, scale=6, font_size=32).getvalue()
    with open('rain-3.svg', 'wb') as f:
        f.write(svg)
    svg = qr_with_text(qr, text=content).getvalue()
    with open('rain-4.svg', 'wb') as f:
        f.write(svg)
    svg = qr_with_text(qr, text=content, border=0, scale=3).getvalue()
    with open('rain-5.svg', 'wb') as f:
        f.write(svg)
    svg = qr_with_text(qr, title='Rain', scale=3, font_color='darkred').getvalue()
    with open('rain-6.svg', 'wb') as f:
        f.write(svg)
