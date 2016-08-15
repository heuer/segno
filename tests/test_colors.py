# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the colors module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
from nose.tools import eq_, raises, nottest
from segno import colors


@raises(ValueError)
def test_illegal():
    colors.color_to_rgb('unknown')


@raises(ValueError)
def test_illegal2():
    colors.color_to_rgb((1, 2, 3, 256))


@raises(ValueError)
def test_illegal3():
    colors.color_to_rgb((300, 300, 300))


@raises(ValueError)
def test_illegal4():
    colors.color_to_rgb((0, 0, 256))


@raises(ValueError)
def test_illegal5():
    colors.color_to_rgb((256, 0, 0))


def test_color_is_black():
    data = (((0, 0, 0, 0), False),
            ((0, 0, 0, 1), True),
            ((0, 0, 0, 1.0), True),
            ((0, 0, 0, 255), True),
            ((0, 0, 0, 0.25), False),
            ('#000', True),
            ('#000000', True),
            ('Black', True),
            ('black', True),
            ('BLACK', True),
            ('blacK', True),
            )

    def check(expected, clr):
        return eq_(expected, colors.color_is_black(clr))

    for clr, expected in data:
        yield check, expected, clr


def test_color_is_white():
    data = (((255, 255, 255, 0), False),
            ((255, 255, 255, 1), True),
            ((255, 255, 255, 255), True),
            ((255, 255, 255, 1.0), True),
            ((255, 255, 255, .0), False),
            ((255, 255, 255, .25), False),
            ('#FFF', True),
            ('#fFF', True),
            ('#ffF', True),
            ('#fff', True),
            ('#ffffff', True),
            ('White', True),
            ('white', True),
            ('WHITE', True),
            ('whitE', True),
            )

    def check(expected, clr):
        return eq_(expected, colors.color_is_white(clr))

    for clr, expected in data:
        yield check, expected, clr


def test_color_to_webcolor():
    data = (('black', '#000'),
            ('WHite', '#fff'),
            ('#000000', '#000'),
            ('#ffFFff', '#fff'),
            ('#EEeeEE', '#eee'),
            ('#F00', 'red'),
            ('#FF0000', 'red'),
            ('red', 'red'),
            ('#d2b48c', 'tan'),
            ('tan', 'tan'),
            ((0, 0, 0, 1.0), '#000'),
            ((255, 255, 255, 1.0), '#fff'),
            ((255, 0, 0, 0.25), 'rgba(255,0,0,0.25)'),
            ('#0000ffcc', 'rgba(0,0,255,0.8)'),
            ('#949494E8', 'rgba(148,148,148,0.91)'),
    )

    def check(expected, clr):
        return eq_(expected, colors.color_to_webcolor(clr))

    for clr, expected in data:
        yield check, expected, clr


def test_color_to_webcolor_dont_optimize():
    data = (('black', '#000'),
            ('#F00', '#ff0000'),
            ('#FF0000', '#ff0000'),
            ('red', '#ff0000'),
            ('#D2B48C', '#d2b48c'),
            ((0, 0, 0, 1.0), '#000'),
            ((255, 255, 255, 1.0), '#fff'),
    )

    def check(expected, clr):
        return eq_(expected, colors.color_to_webcolor(clr, optimize=False))

    for clr, expected in data:
        yield check, expected, clr


def test_valid_colornames():
    def check(name, expected):
        rgb = colors.color_to_rgb(name)
        eq_(3, len(rgb))
        eq_(expected, rgb)
    data = (
        ('red', (255, 0, 0)),
        ('green', (0, 128, 0)),
        ('blue', (0, 0, 255)),
        ('Fuchsia', (255, 0, 255)),
        ('CoRnFloWeRblUe', (100, 149, 237)),
        ('hOtPink', (255, 105, 180)),
        ('darkSlateGrey', (47, 79, 79)),
    )
    for name, expected in data:
        yield check, name, expected
        yield check, name.title(), expected
        yield check, name.upper(), expected
        yield check, name.lower(), expected


def test_hex_to_rgba():
    data = (('#fff', (255, 255, 255)),
            ('#0000ffcc', (0, 0, 255, .8)),
            ('#949494E8', (148, 148, 148, 0.91)),
    )

    def check(expected, color):
        eq_(expected, colors._hex_to_rgb_or_rgba(color))

    for color, expected in data:
        yield check, expected, color


def test_hex_to_rgba_alpha_int():
    data = (('#fff', (255, 255, 255)),
            ('#0000ffcc', (0, 0, 255, 204)),
            ('#949494E8', (148, 148, 148, 232)),
    )

    def check(expected, color):
        eq_(expected, colors._hex_to_rgb_or_rgba(color, alpha_float=False))

    for color, expected in data:
        yield check, expected, color


def test_valid_hexcodes_rgb():
    def check(name, expected):
        rgb = colors.color_to_rgb(name)
        eq_(3, len(rgb))
        eq_(expected, rgb)
    data = (
        ('#000', (0, 0, 0)),
        ('#FF1493', (255, 20, 147)),
        ('#FA8072', (250, 128, 114)),
        ('00F', (0, 0, 255)),
        ('#800000', (128, 0, 0)),
        ('#812dd3', (129, 45, 211)),
    )
    for name, expected in data:
        yield check, name, expected
        yield check, name.title(), expected
        yield check, name.upper(), expected
        yield check, name.lower(), expected


def test_valid_hexcodes_rgba():
    def check(name, expected):
        rgba = colors.color_to_rgba(name)
        eq_(4, len(rgba))
        eq_(expected, rgba)
    data = (
        ('#808000', (128, 128, 0, 1.0)),
        ('red', (255, 0, 0, 1.0)),
    )
    for name, expected in data:
        yield check, name, expected
        yield check, name.title(), expected
        yield check, name.upper(), expected
        yield check, name.lower(), expected


def test_tuple_to_rgba():
    def check(t, expected):
        rgba = colors.color_to_rgba(t)
        eq_(expected, rgba)

    data = (
        ('#808000', (128, 128, 0, 1.0)),
        ('red', (255, 0, 0, 1.0)),
        ((255, 0, 0, .2), (255, 0, 0, .2)),
    )

    for t, expected in data:
        yield check, t, expected


def test_tuple_to_rgba_int():
    def check(t, expected):
        rgba = colors.color_to_rgba(t, alpha_float=False)
        eq_(expected, rgba)

    data = (
        ('#808000', (128, 128, 0, 255)),
        ('red', (255, 0, 0, 255)),
        ((0, 0, 255, .8), (0, 0, 255, 204)),
    )

    for t, expected in data:
        yield check, t, expected


def test_invert_color():
    def check(color, expected_color):
        eq_(expected_color, colors.invert_color(color))
    data = (
        ((0, 0, 0), (255, 255, 255)),
        ((255, 255, 255), (0, 0, 0)),
        ((123, 123, 123), (132, 132, 132)),
        ((60, 70, 80), (195, 185, 175)),
    )
    for color, expected_color in data:
        yield check, color, expected_color


if __name__ == '__main__':
    import nose
    nose.core.runmodule()