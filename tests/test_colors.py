#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the colors module.
"""
import pytest
from segno import writers as colors


def test_illegal():
    with pytest.raises(ValueError):
        colors._color_to_rgb('unknown')


def test_illegal2():
    with pytest.raises(ValueError):
        colors._color_to_rgb((1, 2, 3, 256))


def test_illegal3():
    with pytest.raises(ValueError):
        colors._color_to_rgb((300, 300, 300))


def test_illegal4():
    with pytest.raises(ValueError):
        colors._color_to_rgb((0, 0, 256))


def test_illegal5():
    with pytest.raises(ValueError):
        colors._color_to_rgb((256, 0, 0))


def test_rgba_vs_rgb_conflict():
    with pytest.raises(ValueError):
        colors._color_to_rgb('#949494E8')


@pytest.mark.parametrize('clr, expected', [((0, 0, 0, 0), False),
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
                                           ])
def test_color_is_black(clr, expected):
    assert expected == colors._color_is_black(clr)


@pytest.mark.parametrize('clr, expected', (((255, 255, 255, 0), False),
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
                                           ))
def test_color_is_white(clr, expected):
    assert expected == colors._color_is_white(clr)


@pytest.mark.parametrize('clr, expected', (('black', '#000'),
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
                                           ))
def test_color_to_webcolor(clr, expected):
    assert expected == colors._color_to_webcolor(clr)


@pytest.mark.parametrize('clr, expected', (('black', '#000'),
                                           ('#F00', '#ff0000'),
                                           ('#FF0000', '#ff0000'),
                                           ('red', '#ff0000'),
                                           ('#D2B48C', '#d2b48c'),
                                           ((0, 0, 0, 1.0), '#000'),
                                           ((255, 255, 255, 1.0), '#fff'),
                                           ))
def test_color_to_webcolor_dont_optimize(clr, expected):
    assert expected == colors._color_to_webcolor(clr, optimize=False)


def _make_valid_colornames_data():
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
        yield name, expected
        yield name.title(), expected
        yield name.upper(), expected
        yield name.lower(), expected


@pytest.mark.parametrize('name, expected', _make_valid_colornames_data())
def test_valid_colornames(name, expected):
    rgb = colors._color_to_rgb(name)
    assert 3 == len(rgb)
    assert expected == rgb


@pytest.mark.parametrize('color, expected', (('#fff', (255, 255, 255)),
                                             ('#0000ffcc', (0, 0, 255, .8)),
                                             ('#949494E8', (148, 148, 148, 0.91)),
                                             ))
def test_hex_to_rgba(color, expected):
    assert expected == colors._hex_to_rgb_or_rgba(color)


@pytest.mark.parametrize('color, expected', (('#fff', (255, 255, 255)),
                                             ('#0000ffcc', (0, 0, 255, 204)),
                                             ('#949494E8', (148, 148, 148, 232)),
                                             ))
def test_hex_to_rgba_alpha_int(color, expected):
    assert expected == colors._hex_to_rgb_or_rgba(color, alpha_float=False)


def _make_valid_hexcodes_rgb_data():
    data = (
        ('#000', (0, 0, 0)),
        ('#FF1493', (255, 20, 147)),
        ('#FA8072', (250, 128, 114)),
        ('00F', (0, 0, 255)),
        ('#800000', (128, 0, 0)),
        ('#812dd3', (129, 45, 211)),
    )
    for name, expected in data:
        yield name, expected
        yield name.title(), expected
        yield name.upper(), expected
        yield name.lower(), expected


@pytest.mark.parametrize('name, expected', _make_valid_hexcodes_rgb_data())
def test_valid_hexcodes_rgb(name, expected):
    rgb = colors._color_to_rgb(name)
    assert 3 == len(rgb)
    assert expected == rgb


def _make_valid_hexcodes_rgba_data():
    data = (
        ('#808000', (128, 128, 0, 1.0)),
        ('red', (255, 0, 0, 1.0)),
    )
    for name, expected in data:
        yield name, expected
        yield name.title(), expected
        yield name.upper(), expected
        yield name.lower(), expected


@pytest.mark.parametrize('name, expected', _make_valid_hexcodes_rgba_data())
def test_valid_hexcodes_rgba(name, expected):
    rgba = colors._color_to_rgba(name)
    assert 4 == len(rgba)
    assert expected == rgba


@pytest.mark.parametrize('t, expected', (
                                            ('#808000', (128, 128, 0, 1.0)),
                                            ('red', (255, 0, 0, 1.0)),
                                            ((255, 0, 0, .2), (255, 0, 0, .2)),
    ))
def test_tuple_to_rgba(t, expected):
    rgba = colors._color_to_rgba(t)
    assert expected == rgba


@pytest.mark.parametrize('t, expected', (
                                        ('#808000', (128, 128, 0, 255)),
                                        ('red', (255, 0, 0, 255)),
                                        ((0, 0, 255, .8), (0, 0, 255, 204)),
    ))
def test_tuple_to_rgba_int(t, expected):
    rgba = colors._color_to_rgba(t, alpha_float=False)
    assert expected == rgba


@pytest.mark.parametrize('color, expected', (
                                            ((0, 0, 0), (255, 255, 255)),
                                            ((255, 255, 255), (0, 0, 0)),
                                            ((123, 123, 123), (132, 132, 132)),
                                            ((60, 70, 80), (195, 185, 175)),
    ))
def test_invert_color(color, expected):
    assert expected == colors._invert_color(color)


if __name__ == '__main__':
    pytest.main([__file__])
