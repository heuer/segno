# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Standard serializers and utility functions for serializers.

The serializers are independent of the :py:class:`segno.QRCode` (and the
:py:class:`segno.encoder.Code`) class; they just need a matrix (tuple of
bytearrays) and the version constant.
"""
from __future__ import absolute_import, unicode_literals, division
import io
import re
import zlib
import codecs
import base64
import gzip
from xml.sax.saxutils import quoteattr, escape
from struct import pack
from itertools import chain
from functools import partial
from functools import reduce
from contextlib import contextmanager
import time
_PY2 = False
try:  # pragma: no cover
    from itertools import zip_longest
    from urllib.parse import quote
except ImportError:  # pragma: no cover
    _PY2 = True
    from itertools import izip_longest as zip_longest
    from urllib import quote
    range = xrange
    str = unicode
    from io import open
from . import colors
from .utils import matrix_to_lines, get_symbol_size, get_border, \
        check_valid_scale, check_valid_border, matrix_iter

# Standard creator name
CREATOR = 'Segno <https://pypi.python.org/pypi/segno/>'


@contextmanager
def writable(file_or_path, mode, encoding=None):
    """\
    Returns a writable file-like object.

    Usage::

        with writable(file_name_or_path, 'wb') as f:
            ...


    :param file_or_path: Either a file-like object or a filename.
    :param str mode: String indicating the writing mode (i.e. ``'wb'``)
    """
    f = file_or_path
    must_close = False
    try:
        file_or_path.write
        if encoding is not None:
            f = codecs.getwriter(encoding)(file_or_path)
    except AttributeError:
        f = open(file_or_path, mode, encoding=encoding)
        must_close = True
    try:
        yield f
    finally:
        if must_close:
            f.close()


def write_svg(matrix, version, out, scale=1, border=None, color='#000',
              background=None, xmldecl=True, svgns=True, title=None, desc=None,
              svgid=None, svgclass='segno', lineclass='qrline', omitsize=False,
              unit=None, encoding='utf-8', svgversion=None, nl=True):
    """\
    Serializes the QR Code as SVG document.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write bytes.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: ``#000``). Any value
            which is supported by SVG can be used. In addition, ``None``
            is a valid value. The resulting path won't have a ``stroke``
            attribute.
    :param background: Optional background color (default: ``None`` = no
            background color). See `color` for valid values.
    :param bool xmldecl: Inidcates if the XML declaration header should be
            written (default: ``True``)
    :param bool svgns: Indicates if the SVG namespace should be written
            (default: ``True``).
    :param str title: Optional title of the generated SVG document.
    :param str desc: Optional description of the generated SVG document.
    :param svgid: The ID of the SVG document (if set to ``None`` (default),
            the SVG element won't have an ID).
    :param svgclass: The CSS class of the SVG document
            (if set to ``None``, the SVG element won't have a class).
    :param lineclass: The CSS class of the path element (which draws the
            "black" modules (if set to ``None``, the path won't have a class).
    :param bool omitsize: Indicates if width and height attributes should be
            omitted (default: ``False``). If these attributes are omitted,
            a ``viewBox`` attribute will be added to the document.
    :param str unit: Unit for width / height and other coordinates.
            By default, the unit is unspecified and all values are
            in the user space.
            Valid values: em, ex, px, pt, pc, cm, mm, in, and percentages
    :param str encoding: Encoding of the XML document. "utf-8" by default.
    :param float svgversion: SVG version (default: None)
    :param bool nl: Indicates if the document should have a trailing newline
            (default: ``True``)
    """
    check_valid_scale(scale)
    check_valid_border(border)
    unit = unit or ''
    if unit and omitsize:
        raise ValueError('The unit "{0}" has no effect if the size '
                         '(width and height) is omitted.'.format(unit))
    with writable(out, 'wt', encoding=encoding) as f:
        write = f.write
        # Write the document header
        if xmldecl:
            write('<?xml version="1.0" encoding="{0}"?>\n'.format(encoding))
        write('<svg')
        if svgns:
            write(' xmlns="http://www.w3.org/2000/svg"')
        if svgversion is not None and svgversion < 2.0:
            write(' version={0}'.format(quoteattr(str(svgversion))))
        border = get_border(version, border)
        width, height = get_symbol_size(version, scale, border)
        if not omitsize:
            write(' width="{0}{2}" height="{1}{2}"'.format(width, height, unit))
        if omitsize or unit:
            write(' viewBox="0 0 {0} {1}"'.format(width, height))
        if svgid:
            write(' id={0}'.format(quoteattr(svgid)))
        if svgclass:
            write(' class={0}'.format(quoteattr(svgclass)))
        write('>')
        if title is not None:
            write('<title>{0}</title>'.format(escape(title)))
        if desc is not None:
            write('<desc>{0}</desc>'.format(escape(desc)))
        allow_css3_colors = svgversion is not None and svgversion >= 2.0
        if background is not None:
            bg_color = colors.color_to_webcolor(background, allow_css3_colors=allow_css3_colors)
            fill_opacity = ''
            if isinstance(bg_color, tuple):
                bg_color, opacity = bg_color
                fill_opacity = ' fill-opacity={0}'.format(quoteattr(str(opacity)))
            write('<path fill="{0}"{1} d="M0 0h{2}v{3}h-{2}z"/>'
                  .format(bg_color, fill_opacity, width, height))
        write('<path')
        if scale != 1:
            write(' transform="scale({0})"'.format(scale))
        if color is not None:
            opacity = None
            stroke_color = colors.color_to_webcolor(color, allow_css3_colors=allow_css3_colors)
            if isinstance(stroke_color, tuple):
                stroke_color, opacity = stroke_color
            write(' stroke={0}'.format(quoteattr(stroke_color)))
            if opacity is not None:
                write(' stroke-opacity={0}'.format(quoteattr(str(opacity))))
        if lineclass:
            write(' class={0}'.format(quoteattr(lineclass)))
        write(' d="')
        # Current pen pointer position
        x, y = border, border + .5  # .5 == stroke-width / 2
        line_iter = matrix_to_lines(matrix, x, y)
        # 1st coord is absolute
        (x1, y1), (x2, y2) = next(line_iter)
        coord = ['M{0} {1}h{2}'.format(x1, y1, x2 - x1)]
        append_coord = coord.append
        x, y = x2, y2
        for (x1, y1), (x2, y2) in line_iter:
            append_coord('m{0} {1}h{2}'.format(x1 - x, int(y1 - y), x2 - x1))
            x, y = x2, y2
        write(''.join(coord))
        # Close path and doc
        write('"/></svg>')
        if nl:
            write('\n')


_replace_quotes = partial(re.compile(br'(=)"([^"]+)"').sub, br"\1'\2'")

def as_svg_data_uri(matrix, version, scale=1, border=None, color='#000',
                    background=None, xmldecl=False, svgns=True, title=None,
                    desc=None, svgid=None, svgclass='segno',
                    lineclass='qrline', omitsize=False, unit='',
                    encoding='utf-8', svgversion=None, nl=False,
                    encode_minimal=False, omit_charset=False):
    """\
    Converts the matrix to a SVG data URI.

    The XML declaration is omitted by default (set ``xmldecl`` to ``True``
    to enable it), further the newline is omitted by default (set ``nl`` to
    ``True`` to enable it).

    Aside from the missing ``out`` parameter and the different ``xmldecl``
    and ``nl`` default values and the additional parameter ``encode_minimal``
    and ``omit_charset`` this function uses the same parameters as the
    usual SVG serializer.

    :param bool encode_minimal: Indicates if the resulting data URI should
                    use minimal percent encoding (disabled by default).
    :param bool omit_charset: Indicates if the ``;charset=...`` should be omitted
                    (disabled by default)
    :rtype: str
    """
    encode = partial(quote, safe=b"") if not encode_minimal else partial(quote, safe=b" :/='")
    buff = io.BytesIO()
    write_svg(matrix, version, buff, scale=scale, color=color, background=background,
              border=border, xmldecl=xmldecl, svgns=svgns, title=title,
              desc=desc, svgclass=svgclass, lineclass=lineclass,
              omitsize=omitsize, encoding=encoding, svgid=svgid, unit=unit,
              svgversion=svgversion, nl=nl)
    return 'data:image/svg+xml{0},{1}' \
                .format(';charset=' + encoding if not omit_charset else '',
                        # Replace " quotes with ' and URL encode the result
                        # See also https://codepen.io/tigt/post/optimizing-svgs-in-data-uris
                        encode(_replace_quotes(buff.getvalue())))


def write_svg_debug(matrix, version, out, scale=15, border=None,
                    fallback_color='fuchsia', color_mapping=None,
                    add_legend=True):
    """\
    Internal SVG serializer which is useful to debugging purposes.

    This function is not exposed to the QRCode class by intention and the
    resulting SVG document is very inefficient (lots of <rect/>s).
    Dark modules are black and light modules are white by default. Provide
    a custom `color_mapping` to override these defaults.
    Unknown modules are red by default.

    :param matrix: The matrix
    :param version: Version constant
    :param out: binary file-like object or file name
    :param scale: Scaling factor
    :param border: Quiet zone
    :param fallback_color: Color which is used for modules which are not 0x0 or 0x1
                and for which no entry in `color_mapping` is defined.
    :param color_mapping: dict of module values to color mapping (optional)
    :param bool add_legend: Indicates if the bit values should be added to the
                matrix (default: True)
    """
    clr_mapping = {
        0x0: '#fff',
        0x1: '#000',
        0x2: 'red',
        0x3: 'orange',
        0x4: 'gold',
        0x5: 'green',
    }
    if color_mapping is not None:
        clr_mapping.update(color_mapping)
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale, border)
    matrix_size = get_symbol_size(version, scale=1, border=0)[0]
    with writable(out, 'wt', encoding='utf-8') as f:
        legend = []
        write = f.write
        write('<?xml version="1.0" encoding="utf-8"?>\n')
        write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {0} {1}">'.format(width, height))
        write('<style type="text/css"><![CDATA[ text { font-size: 1px; font-family: Helvetica, Arial, sans; } ]]></style>')
        write('<g transform="scale({0})">'.format(scale))
        for i in range(matrix_size):
            y = i + border
            for j in range(matrix_size):
                x = j + border
                bit = matrix[i][j]
                if add_legend and bit not in (0x0, 0x1):
                    legend.append((x, y, bit))
                fill = clr_mapping.get(bit, fallback_color)
                write('<rect x="{0}" y="{1}" width="1" height="1" fill="{2}"/>'.format(x, y, fill))
        # legend may be empty if add_legend == False
        for x, y, val in legend:
            write('<text x="{0}" y="{1}">{2}</text>'.format(x+.2, y+.9, val))
        write('</g></svg>\n')


def write_eps(matrix, version, out, scale=1, border=None, color='#000',
              background=None):
    """\
    Serializes the QR Code as EPS document.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write strings.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 point (1/72 inch) per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple (this method
            acceppts floats as R, G, B values), as web color name (like
            "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: ``None`` = no
            background color). See `color` for valid values.
    """
    import textwrap

    def write_line(writemeth, content):
        """\
        Writes `content` and ``LF``.
        """
        # Postscript: Max. 255 characters per line
        for line in textwrap.wrap(content, 254):
            writemeth(line)
            writemeth('\n')

    def rgb_to_floats(clr):
        """\
        Converts the provided color into an acceptable format for Postscript's
         ``setrgbcolor``
        """
        def to_float(c):
            if isinstance(c, float):
                if not 0.0 <= c <= 1.0:
                    raise ValueError('Invalid color "{0}". Not in range 0 .. 1'
                                     .format(c))
                return c
            return 1 / 255.0 * c if c != 1 else c

        return tuple([to_float(i) for i in colors.color_to_rgb(clr)])

    check_valid_scale(scale)
    check_valid_border(border)
    with writable(out, 'wt') as f:
        writeline = partial(write_line, f.write)
        border = get_border(version, border)
        width, height = get_symbol_size(version, scale, border)
        # Write common header
        writeline('%!PS-Adobe-3.0 EPSF-3.0')
        writeline('%%Creator: {0}'.format(CREATOR))
        writeline('%%CreationDate: {0}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        writeline('%%DocumentData: Clean7Bit')
        writeline('%%BoundingBox: 0 0 {0} {1}'.format(width, height))
        # Write the shortcuts
        writeline('/m { rmoveto } bind def')
        writeline('/l { rlineto } bind def')
        stroke_color_is_black = colors.color_is_black(color)
        stroke_color = color if stroke_color_is_black else rgb_to_floats(color)
        if background is not None:
            writeline('{0:f} {1:f} {2:f} setrgbcolor clippath fill'
                      .format(*rgb_to_floats(background)))
            if stroke_color_is_black:
                # Reset RGB color back to black iff stroke color is black
                # In case stroke color != black set the RGB color later
                writeline('0 0 0 setrgbcolor')
        if not stroke_color_is_black:
            writeline('{0:f} {1:f} {2:f} setrgbcolor'.format(*stroke_color))
        if scale != 1:
            writeline('{0} {0} scale'.format(scale))
        writeline('newpath')
        # Current pen position y-axis
        # Note: 0, 0 = lower left corner in PS coordinate system
        y = get_symbol_size(version, scale=1, border=0)[1] + border - .5  # .5 = linewidth / 2
        line_iter = matrix_to_lines(matrix, border, y, incby=-1)
        # EPS supports absolute coordinates as well, but relative coordinates
        # are more compact and IMO nicer; so the 1st coordinate is absolute, all
        # other coordinates are relative
        (x1, y1), (x2, y2) = next(line_iter)
        coord = ['{0} {1} moveto {2} 0 l'.format(x1, y1, x2 - x1)]
        append_coord = coord.append
        x = x2
        for (x1, y1), (x2, y2) in line_iter:
            append_coord(' {0} {1} m {2} 0 l'.format(x1 - x, int(y1 - y), x2 - x1))
            x, y = x2, y2
        writeline(''.join(coord))
        writeline('stroke')
        writeline('%%EOF')


def write_png(matrix, version, out, scale=1, border=None, color='#000',
              background='#fff', compresslevel=9, dpi=None, addad=True):
    """\
    Serializes the QR Code as PNG image.

    By default, the generated PNG will be a greyscale image with a bitdepth
    of 1. If different colors are provided, an indexed-color image with
    the same bitdepth is generated.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write bytes.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as web color name
            (like "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: white).
            See `color` for valid values. In addition, ``None`` is
            accepted which indicates a transparent background.
    :param int dpi: Optional DPI setting. By default (``None``), the PNG won't
            have any DPI information. Note that the DPI value is converted into
            meters since PNG does not support any DPI information.
    :param int compresslevel: Integer indicating the compression level
            (default: 9). 1 is fastest and produces the least
            compression, 9 is slowest and produces the most.
            0 is no compression.
    """

    def png_color(clr):
        return colors.color_to_rgb_or_rgba(clr, alpha_float=False)

    def chunk(name, data):
        """\
        Returns a PNG chunk with checksum.
        """
        chunk_head = name + data
        # See <https://docs.python.org/2/library/zlib.html#zlib.crc32>
        # why crc32() & 0xFFFFFFFF is necessary
        return pack(b'>I', len(data)) + chunk_head \
               + pack(b'>I', zlib.crc32(chunk_head) & 0xFFFFFFFF)

    def scale_row_x_axis(row):
        """\
        Returns each pixel `scale` times.
        """
        for b in row:
            for i in range(scale):
                yield b

    def scanline(row, filter_type=b'\0'):
        """\
        Returns a single scanline.
        """
        return bytearray(chain(filter_type, _pack_bits_into_byte(row)))

    def invert_row_bits(row):
        """\
        Inverts the row bits 0 -> 1, 1 -> 0
        """
        return (b ^ 0x1 for b in row)

    scale = int(scale)
    check_valid_scale(scale)
    check_valid_border(border)
    # Background color index
    bg_color_idx = 0
    trans_color = 1  # white
    stroke_is_transparent, bg_is_transparent = color is None, background is None
    stroke_color = png_color(color) if not stroke_is_transparent else None
    bg_color = png_color(background) if not bg_is_transparent else None
    if stroke_color == bg_color:
        raise ValueError('The stroke color and background color must not be the same')
    stroke_is_black, stroke_is_white = False, False
    bg_is_white, bg_is_black = False, False
    if not stroke_is_transparent:
        stroke_is_black = colors.color_is_black(stroke_color)
        if not stroke_is_black:
            stroke_is_white = colors.color_is_white(stroke_color)
    if not bg_is_transparent:
        bg_is_white = colors.color_is_white(bg_color)
        if not bg_is_white:
            bg_is_black = colors.color_is_black(bg_color)
    transparency = stroke_is_transparent or bg_is_transparent
    is_greyscale = False
    invert_row = False
    if bg_is_white:
        is_greyscale = stroke_is_black or stroke_is_transparent
        invert_row = is_greyscale
        trans_color = int(not is_greyscale)
    elif bg_is_black:
        is_greyscale = stroke_is_transparent or stroke_is_white
    elif bg_is_transparent:
        is_greyscale = stroke_is_black or stroke_is_white
        invert_row = is_greyscale
    palette = None
    if not is_greyscale:
        # PLTE image
        if bg_is_transparent:
            bg_color = colors.invert_color(stroke_color[:3])
            if len(stroke_color) == 4:
                bg_color += (0,)
        elif stroke_is_transparent:
            stroke_color = colors.invert_color(bg_color[:3])
            if len(bg_color) == 4:
                stroke_color += (0,)
        palette = sorted([bg_color, stroke_color], key=len, reverse=True)
        bg_color_idx = palette.index(bg_color)
        # Usually, the background color is the first entry in the PLTE so
        # no bit inverting should be necessary
        invert_row = bg_color_idx > 0
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale, border)
    if dpi:
        dpi = int(dpi)
        if dpi < 0:
            raise ValueError('DPI value must not be negative')
        dpi = int(dpi // 0.0254)
    with writable(out, 'wb') as f:
        write = f.write
        # PNG writing by "hand" since this lib should not rely on PIL/Pillow
        # and PyPNG does not support PNG filters which leads to a suboptimal
        # performance (and file size) if the PNG image should be scaled.
        # I.e. a (unrealistic) scaling factor of 600 would require a 17400 x 17400
        # matrix as input for PyPNG for a 21 x 21 QR Code (+ border = 4) while
        # this algorithm works upon the primary 21 x 21 matrix.
        write(b'\211PNG\r\n\032\n')  # Magic number
        colortype = 3 if not is_greyscale else 0
        if is_greyscale:
            bg_color_idx = int(invert_row)
        # Header:
        # width, height, bitdepth, colortype, compression meth., filter, interlance
        write(chunk(b'IHDR', pack(b'>2I5B', width, height, 1, colortype, 0, 0, 0)))
        if dpi:
            write(chunk(b'pHYs', pack(b'>LLB', dpi, dpi, 1)))
        if colortype == 3:  # Palette
            write(chunk(b'PLTE', b''.join(pack(b'>3B', *clr[:3]) for clr in palette)))
            # <https://www.w3.org/TR/PNG/#11tRNS>
            if len(palette[0]) > 3:  # Color with alpha is the first in the palette
                f.write(chunk(b'tRNS', b''.join(pack(b'>B', clr[3]) for clr in palette if len(clr) > 3)))
            elif transparency:
                f.write(chunk(b'tRNS', pack(b'>B', bg_color_idx)))
        elif is_greyscale and transparency:  # Greyscale with alpha
            # Greyscale with alpha channel
            # <https://www.w3.org/TR/PNG/#11tRNS>
            # 2 bytes for color type == 0 (greyscale)
            write(chunk(b'tRNS', pack(b'>1H', trans_color)))
        # <https://www.w3.org/TR/PNG/#9Filters>
        # This variable holds the "Up" filter which indicates that this scanline
        # is equal to the above scanline (since it is filled with null bytes)
        same_as_above = b''
        row_filters = []
        if invert_row:
            row_filters.append(invert_row_bits)
        if scale > 1:
            # 2 == PNG Filter "Up"  <https://www.w3.org/TR/PNG/#9-table91>
            same_as_above = scanline([0] * width, filter_type=b'\2') * (scale - 1)
            row_filters.append(scale_row_x_axis)
        horizontal_border, vertical_border = b'', b''
        if border > 0:
            # Calculate horizontal and vertical border
            horizontal_border = scanline([bg_color_idx] * width) * border * scale
            vertical_border = [bg_color_idx] * border * scale
        res = bytearray(horizontal_border)
        for row in matrix:
            row = reduce(lambda r, fn: fn(r), row_filters, row)
            # Chain precalculated left border with row and right border
            res += scanline(chain(vertical_border, row, vertical_border))
            res += same_as_above  # This is b'' if no scaling factor was provided
        res += horizontal_border
        if _PY2:
            res = bytes(res)
        write(chunk(b'IDAT', zlib.compress(res, compresslevel)))
        if addad:
            write(chunk(b'tEXt', b'Software\x00' + CREATOR.encode('ascii')))
        write(chunk(b'IEND', b''))


def as_png_data_uri(matrix, version, scale=1, border=None, color='#000',
                    background='#fff', compresslevel=9, addad=True):
    """\
    Converts the provided matrix into a PNG data URI.

    :rtype: str
    """
    buff = io.BytesIO()
    write_png(matrix, version, buff, scale=scale, border=border, color=color,
              background=background, compresslevel=compresslevel, addad=addad)
    return 'data:image/png;base64,{0}' \
                .format(base64.b64encode(buff.getvalue()).decode('ascii'))


def write_pdf(matrix, version, out, scale=1, border=None, color='#000',
              background=None, compresslevel=9):
    """\
    Serializes the QR Code as PDF document.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write bytes.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as web color name
            (like "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: ``None`` = no
            background color). See `color` for valid values.
    :param int compresslevel: Integer indicating the compression level
            (default: 9). 1 is fastest and produces the least
            compression, 9 is slowest and produces the most.
            0 is no compression.
    """

    def write_string(writemeth, s):
        writemeth(s.encode('ascii'))

    def to_pdf_color(clr):
        """\
        Converts the provided color into an acceptable format for PDF's
        "DeviceRGB" color space.
         """
        def to_float(c):
            if isinstance(c, float):
                if not 0.0 <= c <= 1.0:
                    raise ValueError('Invalid color "{0}". Not in range 0 .. 1'
                                     .format(c))
                return c
            return 1 / 255.0 * c if c != 1 else c
        return tuple([to_float(i) for i in colors.color_to_rgb(clr)])

    check_valid_scale(scale)
    check_valid_border(border)
    width, height = get_symbol_size(version, scale, border)
    border = get_border(version, border)
    creation_date = "{0}{1:+03d}'{2:02d}'".format(time.strftime('%Y%m%d%H%M%S'),
                                                  time.timezone // 3600,
                                                  abs(time.timezone) % 60)
    cmds = []
    append_cmd = cmds.append
    if scale > 1:
        append_cmd('{0} 0 0 {0} 0 0 cm'.format(scale))
    if background is not None:
        # If the background color is defined, a rect is drawn in the background
        append_cmd('{} {} {} rg'.format(*to_pdf_color(background)))
        append_cmd('0 0 {} {} re'.format(width, height))
        append_cmd('f q')
    # Set the stroke color only iff it is not black (default)
    if not colors.color_is_black(color):
        append_cmd('{} {} {} RG'.format(*to_pdf_color(color)))
    # Current pen position y-axis
    # Note: 0, 0 = lower left corner in PDF coordinate system
    y = get_symbol_size(version, scale=1, border=0)[1] + border - .5
    # Set the origin in the upper left corner
    append_cmd('1 0 0 1 {0} {1} cm'.format(border, y))
    # PDF supports absolute coordinates, only
    for (x1, y1), (x2, y2) in matrix_to_lines(matrix, 0, 0, incby=-1):
        append_cmd('{0} {1} m {2} {1} l'.format(x1, y1, x2, y2))
    append_cmd('S')
    graphic = zlib.compress((' '.join(cmds)).encode('ascii'), compresslevel)
    with writable(out, 'wb') as f:
        write = f.write
        writestr = partial(write_string, write)
        object_pos = []
        write(b'%PDF-1.4\r%\xE2\xE3\xCF\xD3\r\n')
        for obj in ('obj <</Type /Catalog /Pages 2 0 R>>\r\nendobj\r\n',
                    'obj <</Type /Pages /Kids [3 0 R] /Count 1>>\r\nendobj\r\n',
                    'obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 {0} {1}] /Contents 4 0 R>>\r\nendobj\r\n'.format(width, height),
                    'obj <</Length {0} /Filter /FlateDecode>>\r\nstream\r\n'.format(len(graphic))):
            object_pos.append(f.tell())
            writestr('{0} 0 {1}'.format(len(object_pos), obj))
        write(graphic)
        write(b'\r\nendstream\r\nendobj\r\n')
        object_pos.append(f.tell())
        writestr('{0} 0 obj <</CreationDate(D:{1})/Producer({2})/Creator({2})\r\n>>\r\nendofbj\r\n' \
                 .format(len(object_pos), creation_date, CREATOR))
        object_pos.append(f.tell())
        xref_location = f.tell()
        writestr('xref\r\n0 {0}\r\n0000000000 65535 f\r\n'.format(len(object_pos) + 1))
        for pos in object_pos:
            writestr('{0:010d} {1:05d} n\r\n'.format(pos, 0))
        writestr('trailer <</Size {0}/Root 1 0 R/Info 5 0 R>>\r\n'.format(len(object_pos) + 1))
        writestr('startxref\r\n{0}\r\n%%EOF\r\n'.format(xref_location))


def write_txt(matrix, version, out, border=None, color='1', background='0'):
    """\
    Serializes QR code in a text format.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write text.
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Character to use for the black modules (default: '1')
    :param background: Character to use for the white modules (default: '0')
    """
    row_iter = matrix_iter(matrix, version, scale=1, border=border)
    colours = (str(background), str(color))
    with writable(out, 'wt') as f:
        write = f.write
        for row in row_iter:
            write(''.join([colours[i] for i in row]))
            write('\n')


def write_pbm(matrix, version, out, scale=1, border=None, plain=False):
    """\
    Serializes the matrix as `PBM <http://netpbm.sourceforge.net/doc/pbm.html>`_
    image.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write binary data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param bool plain: Indicates if a P1 (ASCII encoding) image should be
            created (default: False). By default a (binary) P4 image is created.
    """
    row_iter = matrix_iter(matrix, version, scale, border)
    width, height = get_symbol_size(version, scale=scale, border=border)
    with writable(out, 'wb') as f:
        write = f.write
        write('{0}\n'
              '# Created by {1}\n'
              '{2} {3}\n'\
              .format(('P4' if not plain else 'P1'), CREATOR, width, height).encode('ascii'))
        if not plain:
            for row in row_iter:
                write(bytearray(_pack_bits_into_byte(row)))
        else:
            for row in row_iter:
                write(b''.join(str(i).encode('ascii') for i in row))
                write(b'\n')


def write_pam(matrix, version, out, scale=1, border=None, color='#000',
              background='#fff'):
    """\
    Serializes the matrix as `PAM <http://netpbm.sourceforge.net/doc/pam.html>`_
    image.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write binary data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as web color name
            (like "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: white).
            See `color` for valid values. In addition, ``None`` is
            accepted which indicates a transparent background.
    """
    def invert_row_bits(row):
        """\
        Inverts the row bits 0 -> 1, 1 -> 0
        """
        return bytearray([b ^ 0x1 for b in row])

    def row_to_color_values(row, colours):
        return b''.join([colours[b] for b in row])

    if not color:
        raise ValueError('Invalid stroke color "{0}"'.format(color))
    row_iter = matrix_iter(matrix, version, scale, border)
    width, height = get_symbol_size(version, scale=scale, border=border)
    depth, maxval, tuple_type = 1, 1, 'BLACKANDWHITE'
    transparency = False
    stroke_color = colors.color_to_rgb_or_rgba(color, alpha_float=False)
    bg_color = colors.color_to_rgb_or_rgba(background, alpha_float=False) if background is not None else None
    colored_stroke = not (colors.color_is_black(stroke_color) or colors.color_is_white(stroke_color))
    if bg_color is None:
        tuple_type = 'GRAYSCALE_ALPHA' if not colored_stroke else 'RGB_ALPHA'
        transparency = True
        bg_color = colors.invert_color(stroke_color[:3])
        bg_color += (0,)
        if len(stroke_color) != 4:
            stroke_color += (255,)
    elif colored_stroke or not (colors.color_is_black(bg_color) or colors.color_is_white(bg_color)):
        tuple_type = 'RGB'
    is_rgb = tuple_type.startswith('RGB')
    colours = None
    if not is_rgb and transparency:
        depth = 2
        colours = (b'\x01\x00', b'\x00\x01')
    elif is_rgb:
        maxval = max(chain(stroke_color, bg_color))
        depth = 3 if not transparency else 4
        fmt = '>{0}B'.format(depth).encode('ascii')
        colours=(pack(fmt, *bg_color), pack(fmt, *stroke_color))
    row_filter = invert_row_bits if colours is None else partial(row_to_color_values, colours=colours)
    with writable(out, 'wb') as f:
        write = f.write
        write('P7\n'
              '# Created by {0}\n'
              'WIDTH {1}\n'
              'HEIGHT {2}\n'
              'DEPTH {3}\n'
              'MAXVAL {4}\n'
              'TUPLTYPE {5}\n'
              'ENDHDR\n'.format(CREATOR, width, height, depth, maxval, tuple_type).encode('ascii'))
        for row in row_iter:
            write(row_filter(row))


def write_xpm(matrix, version, out, scale=1, border=None, color='#000',
              background='#fff', name='img'):
    """\
    Serializes the matrix as `XPM <https://en.wikipedia.org/wiki/X_PixMap>`_ image.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write binary data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as web color name
            (like "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: white).
            See `color` for valid values. ``None`` indicates a transparent
            background.
    :param str name: Name of the image (must be a valid C-identifier).
            Default: "img".
    """
    row_iter = matrix_iter(matrix, version, scale, border)
    width, height = get_symbol_size(version, scale=scale, border=border)
    stroke_color = colors.color_to_rgb_hex(color)
    bg_color = colors.color_to_rgb_hex(background) if background is not None else 'None'
    with writable(out, 'wt') as f:
        write = f.write
        write('/* XPM */\n'
              'static char *{0}[] = {{\n'
              '"{1} {2} 2 1",\n'
              '"  c {3}",\n'
              '"X c {4}",\n'.format(name, width, height, bg_color, stroke_color))
        for i, row in enumerate(row_iter):
            write(''.join(chain(['"'],  (' ' if not b else 'X' for b in row),
                                ['"{0}\n'.format(',' if i < height - 1 else '')])))
        write('};\n')


def write_xbm(matrix, version, out, scale=1, border=None, name='img'):
    """\
    Serializes the matrix as `XBM <https://en.wikipedia.org/wiki/X_BitMap>`_ image.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write text data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 in the provided unit per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param name: Prefix for the variable names. Default: "img".
                 The prefix is used to construct the variable names:
                 ```#define <prefix>_width``` ```static unsigned char <prefix>_bits[]```
    """
    row_iter = matrix_iter(matrix, version, scale, border)
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale=scale, border=border)
    with writable(out, 'wt') as f:
        write = f.write
        write('#define {0}_width {1}\n'
              '#define {0}_height {2}\n'
              'static unsigned char {0}_bits[] = {{\n'.format(name, width, height))
        for i, row in enumerate(row_iter, start=1):
            iter_ = zip_longest(*[iter(row)] * 8, fillvalue=0x0)
            # Reverse bits since XBM uses little endian
            bits = ['0x{0:02x}'.format(reduce(lambda x, y: (x << 1) + y, bits[::-1])) for bits in iter_]
            write('    ')
            write(', '.join(bits))
            write(',\n' if i < height else '\n')
        write('};\n')


def write_tex(matrix, version, out, scale=1, border=None, color='black', unit='pt', url=None):
    """\
    Serializes the matrix as LaTeX PGF picture.

    Requires the `PGF/TikZ <https://en.wikipedia.org/wiki/PGF/TikZ>`_ package
    (i.e. ``\\usepackage{pgf}``) in the LaTeX source.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write text data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 in the provided unit per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param str color: LaTeX color name. The color name is taken at it is, so
            ensure that it refers either to a default color name or that the
            color was defined previously.
    :param unit: Unit of the drawing (default: ``pt``)
    :param url: Optional URL where the QR Code should point to. Requires the
            "hyperref" package. Default: ``None``.
    """
    def point(x, y):
        return '\\pgfqpoint{{{0}{2}}}{{{1}{2}}}'.format(x, y, unit)

    check_valid_scale(scale)
    check_valid_border(border)
    border = get_border(version, border)
    with writable(out, 'wt') as f:
        write = f.write
        write('% Creator:  {0}\n'.format(CREATOR))
        write('% Date:     {0}\n'.format(time.strftime('%Y-%m-%dT%H:%M:%S')))
        if url:
            write('\\href{{{0}}}{{'.format(url))
        write('\\begin{pgfpicture}\n')
        write('  \\pgfsetlinewidth{{{0}{1}}}\n'.format(scale, unit))
        if color and color != 'black':
            write('  \\color{{{0}}}\n'.format(color))
        x, y = border, -border
        for (x1, y1), (x2, y2) in matrix_to_lines(matrix, x, y, incby=-1):
            write('  \\pgfpathmoveto{{{0}}}\n'.format(point(x1 * scale, y1 * scale)))
            write('  \\pgfpathlineto{{{0}}}\n'.format(point(x2 * scale, y2 * scale)))
        write('  \\pgfusepath{stroke}\n')
        write('\\end{{pgfpicture}}{0}\n'.format('' if not url else '}'))


def write_terminal(matrix, version, out, border=None):
    """\
    Function to write to a terminal which supports ANSI escape codes.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version.
    :param out: Filename or a file-like object supporting to write text.
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    """
    with writable(out, 'wt') as f:
        write = f.write
        colours = ['\033[{0}m'.format(i) for i in (7, 49)]
        for row in matrix_iter(matrix, version, scale=1, border=border):
            prev_bit = -1
            cnt = 0
            for bit in row:
                if bit == prev_bit:
                    cnt += 1
                else:
                    if cnt:
                        write(colours[prev_bit])
                        write('  ' * cnt)
                        write('\033[0m')  # reset color
                    prev_bit = bit
                    cnt = 1
            if cnt:
                write(colours[prev_bit])
                write('  ' * cnt)
                write('\033[0m')  # reset color
            write('\n')


def write_terminal_win(matrix, version, border=None):  # pragma: no cover
    """\
    Function to write a QR Code to a MS Windows terminal.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    """
    import sys
    import struct
    import ctypes
    write = sys.stdout.write
    std_out = ctypes.windll.kernel32.GetStdHandle(-11)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(std_out, csbi)
    if not res:
        raise OSError('Cannot find information about the console. '
                      'Not running on the command line?')
    default_color = struct.unpack(b'hhhhHhhhhhh', csbi.raw)[4]
    set_color = partial(ctypes.windll.kernel32.SetConsoleTextAttribute, std_out)
    colours = (240, default_color)
    for row in matrix_iter(matrix, version, scale=1, border=border):
        prev_bit = -1
        cnt = 0
        for bit in row:
            if bit == prev_bit:
                cnt += 1
            else:
                if cnt:
                    set_color(colours[prev_bit])
                    write('  ' * cnt)
                prev_bit = bit
                cnt = 1
        if cnt:
            set_color(colours[prev_bit])
            write('  ' * cnt)
        set_color(default_color)  # reset color
        write('\n')


def _pack_bits_into_byte(iterable):
    """\
    Packs eight bits into one byte.

    If the length of the iterable is not a multiple of eight, ``0x0`` is used
    to fill-up the missing values.
    """
    return (reduce(lambda x, y: (x << 1) + y, e)
            for e in zip_longest(*[iter(iterable)] * 8, fillvalue=0x0))


_VALID_SERIALISERS = {
    'svg': write_svg,
    'svg_debug': write_svg_debug,
    'png': write_png,
    'eps': write_eps,
    'txt': write_txt,
    'pdf': write_pdf,
    'ans': write_terminal,
    'pbm': write_pbm,
    'pam': write_pam,
    'tex': write_tex,
    'xbm': write_xbm,
    'xpm': write_xpm,
}

def save(matrix, version, out, kind=None, **kw):
    """\
    Serializes the matrix in any of the supported formats.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: A filename or a writable file-like object with a
            ``name`` attribute. If a stream like :py:class:`io.ByteIO` or
            :py:class:`io.StringIO` object without a ``name`` attribute is
            provided, use the `kind` parameter to specify the serialization
            format.
    :param kind: If the desired output format cannot be extracted from
            the filename, this parameter can be used to indicate the
            serialization format (i.e. "svg" to enforce SVG output)
    :param kw: Any of the supported keywords by the specific serialization
            method.
    """
    is_stream = False
    if kind is None:
        try:
            fname = out.name
            is_stream = True
        except AttributeError:
            fname = out
        ext = fname[fname.rfind('.') + 1:].lower()
    else:
        ext = kind.lower()
    if not is_stream and ext == 'svgz':
        f = gzip.open(out, 'wb', compresslevel=kw.pop('compresslevel', 9))
        try:
            _VALID_SERIALISERS['svg'](matrix, version, f, **kw)
        finally:
            f.close()
    else:
        if kw.pop('debug', False) and ext == 'svg':
            ext = 'svg_debug'
        try:
            _VALID_SERIALISERS[ext](matrix, version, out, **kw)
        except KeyError:
            raise ValueError('Unknown file extension ".{0}"'.format(ext))
