#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
SVG related tests for multicolor support.
"""
import io
import xml.etree.ElementTree as etree
import pytest
import segno
from segno import writers as colors

_SVG_NS = 'http://www.w3.org/2000/svg'


def _get_svg_el(root, name):
    return root.find('{%s}%s' % (_SVG_NS, name))


def _get_group(root):
    return _get_svg_el(root, 'g')


def _parse_xml(buff):
    """\
    Parses XML and returns the root element.
    """
    buff.seek(0)
    return etree.parse(buff).getroot()


def test_merge_colors():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', finder_dark='green',
            dark_module='green')
    green = colors._color_to_webcolor('green')
    assert green in out.getvalue().decode('utf-8')
    root = _parse_xml(out)
    paths = root.findall('.//{%s}path' % _SVG_NS)
    assert 1 == len(paths)


def test_merge_colors2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', finder_dark='green',
            dark_module='blue', alignment_light='yellow',
            quiet_zone='yellow')
    green = colors._color_to_webcolor('green')
    yellow = colors._color_to_webcolor('yellow')
    blue = colors._color_to_webcolor('blue')
    res = out.getvalue().decode('utf-8')
    assert green in res
    assert yellow in res
    assert blue in res
    root = _parse_xml(out)
    paths = root.findall('.//{%s}path' % _SVG_NS)
    assert 3 == len(paths)
    assert not any(p.attrib.get('transform') for p in paths)


def test_nogroup():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', finder_dark='green',
            dark_module='blue', alignment_light='yellow', quiet_zone='yellow',
            scale=1.0)
    root = _parse_xml(out)
    paths = root.findall('.//{%s}path' % _SVG_NS)
    assert 3 == len(paths)
    assert all(p.attrib.get('transform') is None for p in paths)
    group = _get_group(root)
    assert not group


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', finder_dark='green',
            dark_module='blue', alignment_light='yellow', quiet_zone='yellow',
            scale=1.5)
    root = _parse_xml(out)
    paths = root.findall('.//{%s}path' % _SVG_NS)
    assert 3 == len(paths)
    assert all(p.attrib.get('transform') is None for p in paths)
    group = _get_group(root)
    assert group is not None
    assert 'scale(1.5)' == group.attrib.get('transform')


if __name__ == '__main__':
    pytest.main([__file__])
