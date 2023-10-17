# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Example how to add additional text to a QR code.

See <https://github.com/lincolnloop/python-qrcode/issues/199>
"""
import io
import os
from functools import partial
from PIL import Image, ImageColor, ImageDraw, ImageFont
import segno


def qr_with_text(qrcode: segno.QRCode, *, text: str = None,
                 font_path: str = None, font_size: int = 12, font_color=False,
                 line_spacing: int = None, scale: int = 1, border: int = None,
                 dark='#000', light='#fff', finder_dark=False, finder_light=False,
                 data_dark=False, data_light=False, version_dark=False,
                 version_light=False, format_dark=False, format_light=False,
                 alignment_dark=False, alignment_light=False, timing_dark=False,
                 timing_light=False, separator=False, dark_module=False,
                 quiet_zone=False) -> Image:
    """\
    Adds a text (i.e. the content of the QR code) to the QR code.

    See `segno.QRCode.save <https://segno.readthedocs.io/en/latest/api.html#segno.QRCode.save>`_
    and `PNG <https://segno.readthedocs.io/en/latest/api.html#png>`_ for a detailed
    description of the parameters.

    :param segno.QRCode qrcode: The QR code.
    :param str text: The text to add to the QR code.
    :param str font_path: Path to the font
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
    png = io.BytesIO()
    qrcode.save(png, kind='png', scale=scale, border=border, dark=dark,
                light=light, finder_dark=finder_dark, finder_light=finder_light,
                data_dark=data_dark, data_light=data_light, version_dark=version_dark,
                version_light=version_light, format_dark=format_dark,
                format_light=format_light, alignment_dark=alignment_dark,
                alignment_light=alignment_light, timing_dark=timing_dark,
                timing_light=timing_light, separator=separator,
                dark_module=dark_module, quiet_zone=quiet_zone)
    png.seek(0)
    img = Image.open(png)
    if text is None:
        return img
    font_path = font_path or os.path.join(os.path.dirname(__file__), 'font', 'DejaVuSansMono.ttf')
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    x, y = scale * (border if border is not None else qrcode.default_border_size), height
    line_spacing = line_spacing or font_size // 2
    lines = text.splitlines()
    # Calculate the additional space required for the text
    for line in lines:
        try:  # Pillow versions < 10
            fw, fh = font.getsize(line)
        except AttributeError:
            fw, fh = font.getbbox(line)[2:4]
        if fw > width:
            width = fw + font_size
        height += fh + line_spacing
    has_palette = img.mode == 'P'
    if has_palette:
        # The palette of the resulting image may be different from the
        # palette of the original image. To avoid problems with pasting the
        # QR code image into the resulting image, convert the QR code image to RGBA
        # This operation is reverted after drawing the text
        img = img.convert('RGBA')
    res_img = Image.new(img.mode, (width, height), color=quiet_zone or light)
    res_img.paste(img)
    draw = ImageDraw.Draw(res_img)
    font_color = font_color or dark
    draw_text = partial(draw.text, font=font, fill=ImageColor.getcolor(font_color, img.mode))
    for line in lines:
        draw_text((x, y), line)
        y += font_size + line_spacing
    if has_palette:
        res_img = res_img.convert('P')
    return res_img


if __name__ == '__main__':
    content = 'I read the news today, oh boy\n' \
              'About a lucky man who made the grade\n' \
              'And though the news was rather sad\n' \
              'Well, I just had to laugh\n' \
              'I saw the photograph'
    qr = segno.make(content)
    qr_with_text(qr, text=content, scale=6, dark='darkblue', light='#ffffb2',
                 quiet_zone='#eee').save('a-day-in-the-life-1.png')
    qr_with_text(qr, text=content, scale=6, dark='darkblue', quiet_zone='#eee',
                 font_color='darkgreen').save('a-day-in-the-life-2.png')
    qr_with_text(qr, text=content, scale=6).save('a-day-in-the-life-3.png')
    qr_with_text(qr, text=content, scale=6, font_size=32).save('a-day-in-the-life-4.png')
    qr_with_text(qr, text=content).save('a-day-in-the-life-5.png')
    qr_with_text(qr, text=content, border=0, scale=3).save('a-day-in-the-life-6.png')
