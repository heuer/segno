#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
SVG embeddable into HTML tests.
"""
import xml.etree.ElementTree as etree
import pytest
import segno

_CSS_CLASS = 'segno'
_PATH_CLASS = 'qrline'


def _get_svg_el(root, name):
    return root.find('%s' % name)


def _get_group(root):
    return _get_svg_el(root, 'g')


def _get_first_path(root):
    g = _get_group(root)
    return _get_svg_el(root if g is None else g, 'path')


def _get_title(root):
    return _get_svg_el(root, 'title')


def _get_desc(root):
    return _get_svg_el(root, 'desc')


def _parse_xml(s):
    """\
    Parses XML and returns the root element.
    """
    return etree.fromstring(s)


def test_write_svg():
    qr = segno.make_qr('test')
    svg = qr.svg_inline()
    assert svg.startswith('<svg')
    root = _parse_xml(svg)
    # No background (and scaling) -> no group
    assert _get_group(root) is None
    assert 'viewBox' not in root.attrib
    assert 'height' in root.attrib
    assert 'width' in root.attrib
    css_class = root.attrib.get('class')
    assert css_class
    assert _CSS_CLASS == css_class
    path_el = _get_first_path(root)
    assert path_el is not None
    path_class = path_el.get('class')
    assert _PATH_CLASS == path_class
    stroke = path_el.get('stroke')
    assert stroke == '#000'
    title_el = _get_title(root)
    assert title_el is None
    desc_el = _get_desc(root)
    assert desc_el is None


@pytest.mark.parametrize('dark', ['bLack', '#000000', (0, 0, 0)])
def test_write_svg_black(dark):
    qr = segno.make_qr('test')
    svg = qr.svg_inline(dark=dark)
    assert svg.startswith('<svg')
    root = _parse_xml(svg)
    # No background (and scaling) -> no group
    assert _get_group(root) is None
    assert 'viewBox' not in root.attrib
    assert 'height' in root.attrib
    assert 'width' in root.attrib
    css_class = root.attrib.get('class')
    assert css_class
    assert _CSS_CLASS == css_class
    path_el = _get_first_path(root)
    assert path_el is not None
    path_class = path_el.get('class')
    assert _PATH_CLASS == path_class
    stroke = path_el.get('stroke')
    assert stroke == '#000'
    title_el = _get_title(root)
    assert title_el is None
    desc_el = _get_desc(root)
    assert desc_el is None


def test_write_svg_background_omitted():
    qr = segno.make_qr('test')
    svg = qr.svg_inline()
    assert svg.startswith('<svg')
    root = _parse_xml(svg)
    # No background (and scaling) -> no group
    assert _get_group(root) is None
    # Background should be the first path in the doc
    path = _get_first_path(root)
    assert path is not None
    assert not path.attrib.get('fill')


@pytest.mark.parametrize('light', ['wHitE', '#fff', (255, 255, 255), '#ffffff'])
def test_write_svg_background_white(light):
    qr = segno.make_qr('test')
    svg = qr.svg_inline(light=light)
    assert svg.startswith('<svg')
    root = _parse_xml(svg)
    # No scaling -> no group
    assert _get_group(root) is None
    # Background should be the first path in the doc
    path = _get_first_path(root)
    assert path is not None
    assert '#fff' == path.attrib.get('fill')
    assert path.attrib.get('class') is None
    d = path.attrib.get('d')
    assert d
    expected = 'M0 0h{1}v{0}h-{1}z'.format(*qr.symbol_size())
    assert expected == d
    g = _get_group(root)
    assert g is None


def test_scale_background():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(dark='green', light='yellow', scale=10)
    root = _parse_xml(svg)
    g = _get_group(root)
    assert g is not None
    assert 'scale(10)' == g.attrib.get('transform')


def test_write_svg_color_rgb():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(dark=(76, 131, 205))
    assert svg.startswith('<svg')
    root = _parse_xml(svg)
    assert 'viewBox' not in root.attrib
    assert 'height' in root.attrib
    assert 'width' in root.attrib
    css_class = root.attrib.get('class')
    assert css_class
    assert _CSS_CLASS == css_class
    path_el = _get_first_path(root)
    assert path_el is not None
    path_class = path_el.get('class')
    assert _PATH_CLASS == path_class
    stroke = path_el.get('stroke')
    assert stroke == '#4c83cd'
    title_el = _get_title(root)
    assert title_el is None
    desc_el = _get_desc(root)
    assert desc_el is None


def test_write_svg_color_rgba():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(dark='#0000ffcc')
    assert 'stroke-opacity' in svg


def test_write_svg_color_rgba_svg2():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(dark='#0000ffcc', svgversion=2.0)
    assert 'stroke-opacity' not in svg
    root = _parse_xml(svg)
    path = _get_first_path(root)
    assert path.attrib['stroke'].startswith('rgba')


def test_write_svg_background_rgba():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(light='#0000ffcc')
    assert 'fill-opacity' in svg


def test_write_svg_background_rgba_svg2():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(light='#0000ffcc', svgversion=2.0)
    assert 'fill-opacity' not in svg
    root = _parse_xml(svg)
    path = _get_first_path(root)
    assert path.attrib['fill'].startswith('rgba')


def test_write_no_xmldecl():
    qr = segno.make_qr('test')
    with pytest.raises(TypeError):
        qr.svg_inline(xmldecl=False)


def test_viewbox():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(omitsize=True)
    root = _parse_xml(svg)
    assert 'viewBox' in root.attrib
    assert 'height' not in root.attrib
    assert 'width' not in root.attrib


def test_svgid():
    qr = segno.make_qr('test')
    ident = 'svgid'
    svg = qr.svg_inline(svgid=ident)
    root = _parse_xml(svg)
    assert 'id' in root.attrib
    assert ident == root.attrib['id']


def test_svgid_default():
    qr = segno.make_qr('test')
    svg = qr.svg_inline()
    root = _parse_xml(svg)
    assert 'id' not in root.attrib


def test_svgid_empty_string():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(svgid='')
    root = _parse_xml(svg)
    assert 'id' not in root.attrib


def test_svgversion():
    qr = segno.make_qr('test')
    version = 1.0
    svg = qr.svg_inline(svgversion=version)
    root = _parse_xml(svg)
    assert 'version' in root.attrib
    assert str(version) == root.attrib['version']


def test_svgversion_default():
    qr = segno.make_qr('test')
    svg = qr.svg_inline()
    root = _parse_xml(svg)
    assert 'version' not in root.attrib


def test_no_svg_class():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(svgclass=None)
    root = _parse_xml(svg)
    assert 'class' not in root.attrib


def test_no_svg_class_empty_str():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(svgclass='')
    root = _parse_xml(svg)
    assert 'class' not in root.attrib


def test_custom_svg_class():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(svgclass='test-class')
    root = _parse_xml(svg)
    assert 'class' in root.attrib
    assert 'test-class' == root.attrib.get('class')


def test_no_line_class():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(lineclass=None)
    root = _parse_xml(svg)
    path_el = _get_first_path(root)
    assert 'class' not in path_el.attrib


def test_no_line_class_empty_str():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(lineclass='')
    root = _parse_xml(svg)
    path_el = _get_first_path(root)
    assert 'class' not in path_el.attrib


def test_custom_line_class():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(lineclass='test-class')
    root = _parse_xml(svg)
    path_el = _get_first_path(root)
    assert 'class' in path_el.attrib
    assert 'test-class' == path_el.attrib.get('class')


def test_title():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(title='Test')
    root = _parse_xml(svg)
    title_el = _get_title(root)
    assert title_el is not None
    assert 'Test' == title_el.text


def test_title2():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(title='Määhhh')
    root = _parse_xml(svg)
    title_el = _get_title(root)
    assert title_el is not None
    assert 'Määhhh' == title_el.text


def test_title3():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(title='点')
    root = _parse_xml(svg)
    title_el = _get_title(root)
    assert title_el is not None
    assert '点' == title_el.text


def test_title4():
    qr = segno.make_qr('test')
    encoding = 'ISO-8859-1'
    svg = qr.svg_inline(title='áà', encoding=encoding)
    root = _parse_xml(svg)
    title_el = _get_title(root)
    assert title_el is not None
    assert 'áà' == title_el.text


def test_title_escape():
    qr = segno.make_qr('test')
    title = '<title>&</title>'
    svg = qr.svg_inline(title=title)
    assert '<title>&lt;title&gt;&amp;&lt;/title&gt;</title>' in svg
    root = _parse_xml(svg)
    title_el = _get_title(root)
    assert title_el is not None
    assert title == title_el.text


def test_desc():
    qr = segno.make_qr('test')
    desc = 'Test'
    svg = qr.svg_inline(desc=desc)
    root = _parse_xml(svg)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc2():
    qr = segno.make_qr('test')
    desc = 'Määhhhh'
    svg = qr.svg_inline(desc=desc)
    root = _parse_xml(svg)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc3():
    qr = segno.make_qr('test')
    desc = '点'
    svg = qr.svg_inline(desc=desc)
    root = _parse_xml(svg)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc4():
    qr = segno.make_qr('test')
    encoding = 'ISO-8859-1'
    desc = 'áà'
    svg = qr.svg_inline(desc='áà', encoding=encoding)
    root = _parse_xml(svg)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc_escape():
    qr = segno.make_qr('test')
    desc = '<desc>&</desc>'
    svg = qr.svg_inline(desc=desc)
    assert '<desc>&lt;desc&gt;&amp;&lt;/desc&gt;</desc>' in svg
    root = _parse_xml(svg)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_background():
    qr = segno.make_qr('test')
    color = '#800080'
    svg = qr.svg_inline(light=color)
    root = _parse_xml(svg)
    # Background should be the first path in the doc
    rect = _get_first_path(root)
    assert rect is not None
    assert color == rect.attrib['fill']


def test_module_color():
    qr = segno.make_qr('test')
    color = '#800080'
    svg = qr.svg_inline(dark=color)
    root = _parse_xml(svg)
    path = _get_first_path(root)
    assert path is not None
    assert color == path.attrib['stroke']


def test_scale():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(scale=2)
    root = _parse_xml(svg)
    path = _get_first_path(root)
    assert path is not None
    assert 'scale(2)' in path.attrib['transform']


def test_scale_float():
    qr = segno.make_qr('test')
    scale = 2.13
    svg = qr.svg_inline(scale=scale)
    root = _parse_xml(svg)
    path = _get_first_path(root)
    assert path is not None
    assert f'scale({scale})' in path.attrib['transform']


def test_unit_omitsize():
    qr = segno.make_qr('test')
    with pytest.raises(ValueError):
        qr.svg_inline(unit='cm', omitsize=True)


def test_unit():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(unit='mm')
    width, height = qr.symbol_size()
    root = _parse_xml(svg)
    assert 'width' in root.attrib
    assert '%dmm' % width == root.attrib['width']
    assert 'height' in root.attrib
    assert '%dmm' % height == root.attrib['height']
    assert 'viewBox' in root.attrib
    assert '0 0 %d %d' % (width, height) == root.attrib['viewBox']


def test_unit_none():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(unit=None)
    width, height = qr.symbol_size()
    root = _parse_xml(svg)
    assert 'width' in root.attrib
    assert str(width) == root.attrib['width']
    assert 'height' in root.attrib
    assert str(height) == root.attrib['height']
    assert 'viewBox' not in root.attrib


def test_draw_transparent():
    qr = segno.make_qr('test')
    svg = qr.svg_inline(dark='green', finder_dark='green', dark_module='blue',
                        alignment_light='yellow', quiet_zone='yellow',
                        draw_transparent=False)
    root = _parse_xml(svg)
    paths = root.findall('.//path')
    assert 3 == len(paths)
    svg = qr.svg_inline(dark='green', finder_dark='green', dark_module='blue',
                        alignment_light='yellow', quiet_zone='yellow',
                        draw_transparent=True)
    root = _parse_xml(svg)
    paths = root.findall('.//path')
    assert 4 == len(paths)
    assert 1 == len([p for p in paths if p.attrib.get('stroke') is None])


if __name__ == '__main__':
    pytest.main([__file__])
