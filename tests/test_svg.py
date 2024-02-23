#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
SVG related tests.
"""
import os
import re
import io
import tempfile
import xml.etree.ElementTree as etree
import pytest
import segno

_SVG_NS = 'http://www.w3.org/2000/svg'
_CSS_CLASS = 'segno'
_PATH_CLASS = 'qrline'


def _get_svg_el(root, name):
    return root.find('{%s}%s' % (_SVG_NS, name))


def _get_group(root):
    return _get_svg_el(root, 'g')


def _get_first_path(root):
    g = _get_group(root)
    return _get_svg_el(root if g is None else g, 'path')


def _get_title(root):
    return _get_svg_el(root, 'title')


def _get_desc(root):
    return _get_svg_el(root, 'desc')


def _parse_xml(buff):
    """\
    Parses XML and returns the root element.
    """
    buff.seek(0)
    return etree.parse(buff).getroot()


def test_write_svg():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg')
    xml_str = out.getvalue()
    assert xml_str.startswith(b'<?xml')
    root = _parse_xml(out)
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
    out = io.BytesIO()
    qr.save(out, kind='svg', dark=dark)
    xml_str = out.getvalue()
    assert xml_str.startswith(b'<?xml')
    root = _parse_xml(out)
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
    out = io.BytesIO()
    qr.save(out, kind='svg')
    xml_str = out.getvalue()
    assert xml_str.startswith(b'<?xml')
    root = _parse_xml(out)
    # No background (and scaling) -> no group
    assert _get_group(root) is None
    # Background should be the first path in the doc
    path = _get_first_path(root)
    assert path is not None
    assert not path.attrib.get('fill')


@pytest.mark.parametrize('light', ['wHitE', '#fff', (255, 255, 255), '#ffffff'])
def test_write_svg_background_white(light):
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', light=light)
    xml_str = out.getvalue()
    assert xml_str.startswith(b'<?xml')
    root = _parse_xml(out)
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
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', light='yellow', scale=10)
    root = _parse_xml(out)
    g = _get_group(root)
    assert g is not None
    assert 'scale(10)' == g.attrib.get('transform')


def test_write_svg_color_rgb():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark=(76, 131, 205))
    xml_str = out.getvalue()
    assert xml_str.startswith(b'<?xml')
    root = _parse_xml(out)
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
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='#0000ffcc')
    assert b'stroke-opacity' in out.getvalue()


def test_write_svg_color_rgba_svg2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='#0000ffcc', svgversion=2.0)
    assert b'stroke-opacity' not in out.getvalue()
    root = _parse_xml(out)
    path = _get_first_path(root)
    assert path.attrib['stroke'].startswith('rgba')


def test_write_svg_background_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', light='#0000ffcc')
    assert b'fill-opacity' in out.getvalue()


def test_write_svg_background_rgba_svg2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', light='#0000ffcc', svgversion=2.0)
    assert b'fill-opacity' not in out.getvalue()
    root = _parse_xml(out)
    path = _get_first_path(root)
    assert path.attrib['fill'].startswith('rgba')


def test_write_no_xmldecl():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', xmldecl=False)
    xml_str = out.getvalue()
    assert xml_str.startswith(b'<svg')


def test_viewbox():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', omitsize=True)
    root = _parse_xml(out)
    assert 'viewBox' in root.attrib
    assert 'height' not in root.attrib
    assert 'width' not in root.attrib


def test_svgid():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    ident = 'svgid'
    qr.save(out, kind='svg', svgid=ident)
    root = _parse_xml(out)
    assert 'id' in root.attrib
    assert ident == root.attrib['id']


def test_svgid_default():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg')
    root = _parse_xml(out)
    assert 'id' not in root.attrib


def test_svgid_empty_string():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', svgid='')
    root = _parse_xml(out)
    assert 'id' not in root.attrib


def test_svgversion():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    version = 1.0
    qr.save(out, kind='svg', svgversion=version)
    root = _parse_xml(out)
    assert 'version' in root.attrib
    assert str(version) == root.attrib['version']


def test_svgversion_default():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg')
    root = _parse_xml(out)
    assert 'version' not in root.attrib


def test_no_svg_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', svgclass=None)
    root = _parse_xml(out)
    assert 'class' not in root.attrib


def test_no_svg_class_empty_str():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', svgclass='')
    root = _parse_xml(out)
    assert 'class' not in root.attrib


def test_custom_svg_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', svgclass='test-class')
    root = _parse_xml(out)
    assert 'class' in root.attrib
    assert 'test-class' == root.attrib.get('class')


def test_no_line_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', lineclass=None)
    root = _parse_xml(out)
    path_el = _get_first_path(root)
    assert 'class' not in path_el.attrib


def test_no_line_class_empty_str():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', lineclass='')
    root = _parse_xml(out)
    path_el = _get_first_path(root)
    assert 'class' not in path_el.attrib


def test_custom_line_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', lineclass='test-class')
    root = _parse_xml(out)
    path_el = _get_first_path(root)
    assert 'class' in path_el.attrib
    assert 'test-class' == path_el.attrib.get('class')


def test_omit_svgns():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', svgns=False)
    root = _parse_xml(out)
    path_el = _get_first_path(root)
    assert path_el is None  # (since _get_path uses the SVG namespace)
    path_el = root.find('path')  # Query w/o namespace MUST find the path
    assert path_el is not None


def test_title():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', title='Test')
    root = _parse_xml(out)
    title_el = _get_title(root)
    assert title_el is not None
    assert 'Test' == title_el.text


def test_title2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', title='Määhhh')
    root = _parse_xml(out)
    title_el = _get_title(root)
    assert title_el is not None
    assert 'Määhhh' == title_el.text


def test_title3():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', title='点')
    root = _parse_xml(out)
    title_el = _get_title(root)
    assert title_el is not None
    assert '点' == title_el.text


def test_title4():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    encoding = 'ISO-8859-1'
    qr.save(out, kind='svg', title='áà', encoding=encoding)
    root = _parse_xml(out)
    title_el = _get_title(root)
    assert title_el is not None
    assert 'áà' == title_el.text


def test_title_escape():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    title = '<title>&</title>'
    qr.save(out, kind='svg', title=title)
    assert b'<title>&lt;title&gt;&amp;&lt;/title&gt;</title>' in out.getvalue()
    root = _parse_xml(out)
    title_el = _get_title(root)
    assert title_el is not None
    assert title == title_el.text


def test_desc():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = 'Test'
    qr.save(out, kind='svg', desc=desc)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = 'Määhhhh'
    qr.save(out, kind='svg', desc=desc)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc3():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = '点'
    qr.save(out, kind='svg', desc=desc)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc4():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    encoding = 'ISO-8859-1'
    desc = 'áà'
    qr.save(out, kind='svg', desc='áà', encoding=encoding)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_desc_escape():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = '<desc>&</desc>'
    qr.save(out, kind='svg', desc=desc)
    assert b'<desc>&lt;desc&gt;&amp;&lt;/desc&gt;</desc>' in out.getvalue()
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    assert desc_el is not None
    assert desc == desc_el.text


def test_background():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    color = '#800080'
    qr.save(out, kind='svg', light=color)
    root = _parse_xml(out)
    # Background should be the first path in the doc
    rect = _get_first_path(root)
    assert rect is not None
    assert color == rect.attrib['fill']


def test_module_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    color = '#800080'
    qr.save(out, kind='svg', dark=color)
    root = _parse_xml(out)
    path = _get_first_path(root)
    assert path is not None
    assert color == path.attrib['stroke']


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', scale=2)
    root = _parse_xml(out)
    path = _get_first_path(root)
    assert path is not None
    assert 'scale(2)' in path.attrib['transform']


def test_scale_float():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 2.13
    qr.save(out, kind='svg', scale=scale)
    root = _parse_xml(out)
    path = _get_first_path(root)
    assert path is not None
    assert f'scale({scale})' in path.attrib['transform']


def test_unit_omitsize():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    with pytest.raises(ValueError):
        qr.save(out, kind='svg', unit='cm', omitsize=True)


def test_unit():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', unit='mm')
    width, height = qr.symbol_size()
    root = _parse_xml(out)
    assert 'width' in root.attrib
    assert '%dmm' % width == root.attrib['width']
    assert 'height' in root.attrib
    assert '%dmm' % height == root.attrib['height']
    assert 'viewBox' in root.attrib
    assert '0 0 %d %d' % (width, height) == root.attrib['viewBox']


def test_unit_none():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', unit=None)
    width, height = qr.symbol_size()
    root = _parse_xml(out)
    assert 'width' in root.attrib
    assert str(width) == root.attrib['width']
    assert 'height' in root.attrib
    assert str(height) == root.attrib['height']
    assert 'viewBox' not in root.attrib


def test_write_unicode_filename():
    qr = segno.make_qr('test')
    f = tempfile.NamedTemporaryFile('wt', suffix='.svg', delete=False)
    f.close()
    title = 'mürrische Mädchen'
    desc = '点'
    qr.save(f.name, title=title, desc=desc)
    f = open(f.name, mode='rb')
    root = _parse_xml(f)
    f.seek(0)
    val = f.read(6)
    f.close()
    os.unlink(f.name)
    assert b'<?xml ' == val
    assert title == _get_title(root).text
    assert desc == _get_desc(root).text


def test_encoding_none():
    qr = segno.make_qr('Help!')
    buff = io.BytesIO()
    qr.save(buff, 'svg', encoding=None)
    assert b'<?xml version="1.0"?>' in buff.getvalue()


def test_draw_transparent():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', finder_dark='green',
            dark_module='blue', alignment_light='yellow', quiet_zone='yellow',
            draw_transparent=False)
    root = _parse_xml(out)
    paths = root.findall('.//{%s}path' % _SVG_NS)
    assert 3 == len(paths)
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='green', finder_dark='green',
            dark_module='blue', alignment_light='yellow', quiet_zone='yellow',
            draw_transparent=True)
    root = _parse_xml(out)
    paths = root.findall('.//{%s}path' % _SVG_NS)
    assert 4 == len(paths)
    assert 1 == len([p for p in paths if p.attrib.get('stroke') is None])


def svg_as_matrix(buff, border):
    """\
    Returns the QR code path as list of [0,1] lists.
    """
    root = _parse_xml(buff)
    path = _get_first_path(root)
    h = root.attrib['height']
    w = root.attrib['width']
    if h != w:
        raise ValueError(f'Expected equal height/width, got height="{h}" width="{w}"')
    size = int(w) - 2 * border
    d = path.attrib['d']
    res = []
    res_row = None
    absolute_x = -border
    for op, x, y, length in re.findall(r'([Mm])(-?[0-9]+(?:\.[0-9]+)?) (-?[0-9]+(?:\.[0-9]+)?)h([0-9]+)', d):
        x = int(x)
        y = float(y)
        length = int(length)
        if y != 0.0:  # New row
            if res_row is not None:
                res_row.extend([0] * (size - len(res_row)))
            res_row = []
            res.append(res_row)
        if op == 'm':
            absolute_x += x
            if x < 0:
                res_row.extend([0] * absolute_x)
            else:
                res_row.extend([0] * x)
            absolute_x += length
        elif op == 'M':
            absolute_x = length
            if x != border:
                raise ValueError(f'Unexpected border width. Expected "{border}", got "{x}"')
        res_row.extend([1] * length)
    res_row.extend([0] * (size - len(res_row)))
    return res


if __name__ == '__main__':
    pytest.main([__file__])
