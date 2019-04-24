# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Color utility functions.
"""
from __future__ import absolute_import, unicode_literals


def color_to_rgb_or_rgba(color, alpha_float=True):
    """\
    Returns the provided color as ``(R, G, B)`` or ``(R, G, B, A)`` tuple.

    If the alpha value is opaque, an RGB tuple is returned, otherwise an RGBA
    tuple.

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB(A) tuple (i.e. ``(R, G, B)`` or
            ``(R, G, B, A)``)
    :param bool alpha_float: Indicates if the alpha value should be returned as
            float value. If ``False``, the alpha value is an integer value in
            the range of ``0 .. 254``.
    :rtype: tuple
    """
    rgba = color_to_rgba(color, alpha_float=alpha_float)
    if rgba[3] in (1.0, 255):
        return rgba[:3]
    return rgba


def color_to_webcolor(color, allow_css3_colors=True, optimize=True):
    """\
    Returns either a hexadecimal code or a color name.

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB(A) tuple (i.e. ``(R, G, B)`` or
            ``(R, G, B, A)``)
    :param bool allow_css3_colors: Indicates if a CSS3 color value like
            rgba(R G, B, A) is an acceptable result.
    :param bool optimize: Inidcates if the shortest possible color value should
            be returned (default: ``True``).
    :rtype: str
    :return: The provided color as web color: ``#RGB``, ``#RRGGBB``,
            ``rgba(R, G, B, A)``, or web color name.
    """
    if color_is_black(color):
        return '#000'
    elif color_is_white(color):
        return '#fff'
    clr = color_to_rgb_or_rgba(color)
    alpha_channel = None
    if len(clr) == 4:
        if allow_css3_colors:
            return 'rgba({0},{1},{2},{3})'.format(*clr)
        alpha_channel = clr[3]
        clr = clr[:3]
    hx = '#{0:02x}{1:02x}{2:02x}'.format(*clr)
    if optimize:
        if hx == '#d2b48c':
            hx = 'tan'  # shorter
        elif hx == '#ff0000':
            hx = 'red'  # shorter
        elif hx[1] == hx[2] and hx[3] == hx[4] and hx[5] == hx[6]:
            hx = '#{0}{1}{2}'.format(hx[1], hx[3], hx[5])
    return hx if alpha_channel is None else (hx, alpha_channel)


def color_to_rgb_hex(color):
    """\
    Returns the provided color in hexadecimal representation.

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB(A) tuple (i.e. ``(R, G, B)`` or
            ``(R, G, B, A)``)
    :returns: ``#RRGGBB``.
    """
    return '#{0:02x}{1:02x}{2:02x}'.format(*color_to_rgb(color))


def color_is_black(color):
    """\
    Returns if the provided color represents "black".

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB(A) tuple (i.e. ``(R, G, B)`` or
            ``(R, G, B, A)``)
    :return: ``True`` if color is represents black, otherwise ``False``.
    """
    try:
        color = color.lower()
    except AttributeError:
        pass
    return color in ('#000', '#000000', 'black', (0, 0, 0), (0, 0, 0, 255),
                     (0, 0, 0, 1.0))


def color_is_white(color):
    """\
    Returns if the provided color represents "black".

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB(A) tuple (i.e. ``(R, G, B)`` or
            ``(R, G, B, A)``)
    :return: ``True`` if color is represents white, otherwise ``False``.
    """
    try:
        color = color.lower()
    except AttributeError:
        pass
    return color in ('#fff', '#ffffff', 'white', (255, 255, 255),
                     (255, 255, 255, 255), (255, 255, 255, 1.0))


def color_to_rgb(color):
    """\
    Converts web color names like "red" or hexadecimal values like "#36c",
    "#FFFFFF" and RGB tuples like ``(255, 255 255)`` into a (R, G, B) tuple.

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB tuple (i.e. ``(R, G, B)``))
    :return: ``(R, G, B)`` tuple.
    """
    rgb = color_to_rgb_or_rgba(color)
    if len(rgb) != 3:
        raise ValueError('The alpha channel {0} in color "{1}" cannot be '
                         'converted to RGB'.format(rgb[3], color))
    return rgb


def color_to_rgba(color, alpha_float=True):
    """\
    Returns a (R, G, B, A) tuple.

    :param color: A web color name (i.e. ``darkblue``) or a hexadecimal value
            (``#RGB`` or ``#RRGGBB``) or a RGB(A) tuple (i.e. ``(R, G, B)`` or
            ``(R, G, B, A)``)
    :param bool alpha_float: Indicates if the alpha value should be returned as
            float value. If ``False``, the alpha value is an integer value in
            the range of ``0 .. 254``.
    :return: ``(R, G, B, A)`` tuple.
    """
    res = []
    alpha_channel = (1.0,) if alpha_float else (255,)
    if isinstance(color, tuple):
        col_length = len(color)
        is_valid = False
        if 3 <= col_length <= 4:
            for i, part in enumerate(color[:3]):
                is_valid = 0 <= part <= 255
                res.append(part)
                if not is_valid or i == 2:
                    break
            if is_valid:
                if col_length == 4:
                    res.append(_alpha_value(color[3], alpha_float))
                else:
                    res.append(alpha_channel[0])
        if is_valid:
            return tuple(res)
        raise ValueError('Unsupported color "{0}"'.format(color))
    try:
        return _NAME2RGB[color.lower()] + alpha_channel
    except KeyError:
        try:
            clr = _hex_to_rgb_or_rgba(color, alpha_float=alpha_float)
            if len(clr) == 4:
                return clr
            else:
                return clr + alpha_channel
        except ValueError:
            raise ValueError('Unsupported color "{0}". Neither a known web '
                             'color name nor a color in hexadecimal format.'
                             .format(color))


def _hex_to_rgb_or_rgba(color, alpha_float=True):
    """\
    Helper function to convert a color provided in hexadecimal format (``#RGB``
    or ``#RRGGBB``) to a RGB(A) tuple.

    :param str color: Hexadecimal color name.
    :param bool alpha_float: Indicates if the alpha value should be returned as
            float value. If ``False``, the alpha value is an integer value in
            the range of ``0 .. 254``.
    :return: Tuple of integer values representing a RGB(A) color.
    :rtype: tuple
    :raises: :py:exc:`ValueError` in case the provided string could not
                converted into a RGB(A) tuple
    """
    if color[0] == '#':
        color = color[1:]
    if 2 < len(color) < 5:
        # Expand RGB -> RRGGBB and RGBA -> RRGGBBAA
        color = ''.join([color[i] * 2 for i in range(len(color))])
    color_len = len(color)
    if color_len not in (6, 8):
        raise ValueError('Input #{0} is not in #RRGGBB nor in #RRGGBBAA format'.format(color))
    res = tuple([int(color[i:i+2], 16) for i in range(0, color_len, 2)])
    if alpha_float and color_len == 8:
        res = res[:3] + (_alpha_value(res[3], alpha_float),)
    return res


_ALPHA_COMMONS = {255: 1.0, 128: .5, 64: .25, 32: .125, 16: .625, 0: 0.0}

def _alpha_value(color, alpha_float):
    if alpha_float:
        if not isinstance(color, float):
            if 0 <= color <= 255:
                return _ALPHA_COMMONS.get(color, float('%.02f' % (color / 255.0)))
        else:
            if 0 <= color <= 1.0:
                return color
    else:
        if not isinstance(color, float):
            if 0 <= color <= 255:
                return color
        else:
            if 0 <= color <= 1.0:
                return color * 255.0
    raise ValueError('Invalid alpha channel value: {0}'.format(color))


def invert_color(rgb_or_rgba):
    """\
    Returns the inverse color for the provided color.

    This function does not check if the color is a valid RGB / RGBA color.

    :param rgb: (R, G, B) or (R, G, B, A) tuple.
    """
    return tuple([255 - c for c in rgb_or_rgba])


# <http://www.w3.org/TR/css3-color/#svg-color>
_NAME2RGB = {
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aqua': (0, 255, 255),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'black': (0, 0, 0),
    'blanchedalmond': (255, 235, 205),
    'blue': (0, 0, 255),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'cyan': (0, 255, 255),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkgrey': (169, 169, 169),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'fuchsia': (255, 0, 255),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'gray': (128, 128, 128),
    'green': (0, 128, 0),
    'greenyellow': (173, 255, 47),
    'grey': (128, 128, 128),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightgrey': (211, 211, 211),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'lime': (0, 255, 0),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'magenta': (255, 0, 255),
    'maroon': (128, 0, 0),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'navy': (0, 0, 128),
    'oldlace': (253, 245, 230),
    'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35),
    'orange': (255, 165, 0),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'purple': (128, 0, 128),
    'red': (255, 0, 0),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'silver': (192, 192, 192),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'teal': (0, 128, 128),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'white': (255, 255, 255),
    'whitesmoke': (245, 245, 245),
    'yellow': (255, 255, 0),
    'yellowgreen': (154, 205, 50),
}
