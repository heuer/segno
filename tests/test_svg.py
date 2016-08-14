# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
SVG related tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import os
import re
import io
import tempfile
import xml.etree.ElementTree as etree
from nose.tools import eq_, ok_, raises
import segno

_SVG_NS = 'http://www.w3.org/2000/svg'


def _get_svg_el(root, name):
    return root.find('{%s}%s' % (_SVG_NS, name))


def _get_path(root):
    return _get_svg_el(root, 'path')


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
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out)
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    ok_('viewBox' not in root.attrib)
    ok_('height' in root.attrib)
    ok_('width' in root.attrib)
    css_class = root.attrib.get('class')
    ok_(css_class)
    eq_('segno', css_class)
    path_el = _get_path(root)
    ok_(path_el is not None)
    path_class = path_el.get('class')
    eq_('qrline', path_class)
    stroke = path_el.get('stroke')
    eq_(stroke, '#000')
    title_el = _get_title(root)
    ok_(title_el is None)
    desc_el = _get_desc(root)
    ok_(desc_el is None)


def test_write_svg_black():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, color='bLacK')
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    ok_('viewBox' not in root.attrib)
    ok_('height' in root.attrib)
    ok_('width' in root.attrib)
    css_class = root.attrib.get('class')
    ok_(css_class)
    eq_('segno', css_class)
    path_el = _get_path(root)
    ok_(path_el is not None)
    path_class = path_el.get('class')
    eq_('qrline', path_class)
    stroke = path_el.get('stroke')
    eq_(stroke, '#000')
    title_el = _get_title(root)
    ok_(title_el is None)
    desc_el = _get_desc(root)
    ok_(desc_el is None)


def test_write_svg_black2():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, color='#000000')
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    ok_('viewBox' not in root.attrib)
    ok_('height' in root.attrib)
    ok_('width' in root.attrib)
    css_class = root.attrib.get('class')
    ok_(css_class)
    eq_('segno', css_class)
    path_el = _get_path(root)
    ok_(path_el is not None)
    path_class = path_el.get('class')
    eq_('qrline', path_class)
    stroke = path_el.get('stroke')
    eq_(stroke, '#000')
    title_el = _get_title(root)
    ok_(title_el is None)
    desc_el = _get_desc(root)
    ok_(desc_el is None)


def test_write_svg_black3():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, color=(0, 0, 0))
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    ok_('viewBox' not in root.attrib)
    ok_('height' in root.attrib)
    ok_('width' in root.attrib)
    css_class = root.attrib.get('class')
    ok_(css_class)
    eq_('segno', css_class)
    path_el = _get_path(root)
    ok_(path_el is not None)
    path_class = path_el.get('class')
    eq_('qrline', path_class)
    stroke = path_el.get('stroke')
    eq_(stroke, '#000')
    title_el = _get_title(root)
    ok_(title_el is None)
    desc_el = _get_desc(root)
    ok_(desc_el is None)


def test_write_svg_background_omitted():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out)
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    # Background should be the first path in the doc
    path = _get_path(root)
    ok_(path is not  None)
    ok_(not path.attrib.get('fill'))


def test_write_svg_background_white():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, background='white')
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    # Background should be the first path in the doc
    path = _get_path(root)
    ok_(path is not  None)
    eq_('#fff', path.attrib.get('fill'))


def test_write_svg_background_white2():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, background='#fff')
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    # Background should be the first path in the doc
    path = _get_path(root)
    ok_(path is not  None)
    eq_('#fff', path.attrib.get('fill'))


def test_write_svg_background_white3():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, background='#ffffff')
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    # Background should be the first path in the doc
    path = _get_path(root)
    ok_(path is not  None)
    eq_('#fff', path.attrib.get('fill'))


def test_write_svg_color_rgb():
    # Test with default options
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, color=(76, 131, 205))
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<?xml'))
    root = _parse_xml(out)
    ok_('viewBox' not in root.attrib)
    ok_('height' in root.attrib)
    ok_('width' in root.attrib)
    css_class = root.attrib.get('class')
    ok_(css_class)
    eq_('segno', css_class)
    path_el = _get_path(root)
    ok_(path_el is not None)
    path_class = path_el.get('class')
    eq_('qrline', path_class)
    stroke = path_el.get('stroke')
    eq_(stroke, '#4c83cd')
    title_el = _get_title(root)
    ok_(title_el is None)
    desc_el = _get_desc(root)
    ok_(desc_el is None)


def test_write_svg_color_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, color='#0000ffcc')
    ok_(b'stroke-opacity' in out.getvalue())


def test_write_svg_color_rgba_svg2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, color='#0000ffcc', svgversion=2.0)
    ok_(b'stroke-opacity' not in out.getvalue())
    root = _parse_xml(out)
    path = _get_path(root)
    ok_(path.attrib['stroke'].startswith('rgba'))


def test_write_svg_background_rgba():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, background='#0000ffcc')
    ok_(b'fill-opacity' in out.getvalue())


def test_write_svg_background_rgba_svg2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, background='#0000ffcc', svgversion=2.0)
    ok_(b'fill-opacity' not in out.getvalue())
    root = _parse_xml(out)
    path = _get_path(root)
    ok_(path.attrib['fill'].startswith('rgba'))


def test_write_no_xmldecl():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, xmldecl=False)
    xml_str = out.getvalue()
    ok_(xml_str.startswith(b'<svg'))


def test_viewbox():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, omitsize=True)
    root = _parse_xml(out)
    ok_('viewBox' in root.attrib)
    ok_('height' not in root.attrib)
    ok_('width' not in root.attrib)


def test_svgid():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    ident = 'svgid'
    qr.svg(out, svgid=ident)
    root = _parse_xml(out)
    ok_('id' in root.attrib)
    eq_(ident, root.attrib['id'])


def test_svgid_default():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out)
    root = _parse_xml(out)
    ok_('id' not in root.attrib)


def test_svgversion():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    version = 1.0
    qr.svg(out, svgversion=version)
    root = _parse_xml(out)
    ok_('version' in root.attrib)
    eq_(str(version), root.attrib['version'])


def test_svgversion_default():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out)
    root = _parse_xml(out)
    ok_('version' not in root.attrib)


def test_no_svg_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, svgclass=None)
    root = _parse_xml(out)
    ok_('class' not in root.attrib)


def test_custom_svg_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, svgclass='test-class')
    root = _parse_xml(out)
    ok_('class' in root.attrib)
    eq_('test-class', root.attrib.get('class'))


def test_no_line_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, lineclass=None)
    root = _parse_xml(out)
    path_el = _get_path(root)
    ok_('class' not in path_el.attrib)


def test_custom_line_class():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, lineclass='test-class')
    root = _parse_xml(out)
    path_el = _get_path(root)
    ok_('class' in path_el.attrib)
    eq_('test-class', path_el.attrib.get('class'))


def test_omit_svgns():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, svgns=False)
    root = _parse_xml(out)
    path_el = _get_path(root)
    ok_(path_el is None)  # (since _get_path uses the SVG namespace)
    path_el = root.find('path')  # Query w/o namespace MUST find the path
    ok_(path_el is not None)


def test_title():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, title='Test')
    root = _parse_xml(out)
    title_el = _get_title(root)
    ok_(title_el is not None)
    eq_('Test', title_el.text)


def test_title2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, title='Määhhh')
    root = _parse_xml(out)
    title_el = _get_title(root)
    ok_(title_el is not None)
    eq_('Määhhh', title_el.text)


def test_title3():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, title='点')
    root = _parse_xml(out)
    title_el = _get_title(root)
    ok_(title_el is not None)
    eq_('点', title_el.text)


def test_title4():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    encoding = 'ISO-8859-1'
    qr.svg(out, title='áà', encoding=encoding)
    root = _parse_xml(out)
    title_el = _get_title(root)
    ok_(title_el is not None)
    eq_('áà', title_el.text)


def test_title_escape():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    title = '<title>&</title>'
    qr.svg(out, title=title)
    ok_(b'<title>&lt;title&gt;&amp;&lt;/title&gt;</title>' in out.getvalue())
    root = _parse_xml(out)
    title_el = _get_title(root)
    ok_(title_el is not None)
    eq_(title, title_el.text)


def test_desc():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = 'Test'
    qr.svg(out, desc=desc)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    ok_(desc_el is not None)
    eq_(desc, desc_el.text)


def test_desc2():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = 'Määhhhh'
    qr.svg(out, desc=desc)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    ok_(desc_el is not None)
    eq_(desc, desc_el.text)


def test_desc3():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = '点'
    qr.svg(out, desc=desc)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    ok_(desc_el is not None)
    eq_(desc, desc_el.text)


def test_desc4():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    encoding = 'ISO-8859-1'
    desc = 'áà'
    qr.svg(out, desc='áà', encoding=encoding)
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    ok_(desc_el is not None)
    eq_(desc, desc_el.text)


def test_desc_escape():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    desc = '<desc>&</desc>'
    qr.svg(out, desc=desc)
    ok_(b'<desc>&lt;desc&gt;&amp;&lt;/desc&gt;</desc>' in out.getvalue())
    root = _parse_xml(out)
    desc_el = _get_desc(root)
    ok_(desc_el is not None)
    eq_(desc, desc_el.text)


def test_background():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    color = '#800080'
    qr.svg(out, background=color)
    root = _parse_xml(out)
    # Background should be the first path in the doc
    rect = _get_path(root)
    ok_(rect is not None)
    eq_(color, rect.attrib['fill'])


def test_module_color():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    color = '#800080'
    qr.svg(out, color=color)
    root = _parse_xml(out)
    path = _get_path(root)
    ok_(path is not None)
    eq_(color, path.attrib['stroke'])


def test_scale():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, scale=2)
    root = _parse_xml(out)
    path = _get_path(root)
    ok_(path is not None)
    ok_('scale(2)' in path.attrib['transform'])


def test_scale_float():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    scale = 2.13
    qr.svg(out, scale=scale)
    root = _parse_xml(out)
    path = _get_path(root)
    ok_(path is not None)
    ok_('scale({0})'.format(scale) in path.attrib['transform'])


@raises(ValueError)
def test_unit_omitsize():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, unit='cm', omitsize=True)


def test_unit():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.svg(out, unit='mm')
    width, height = qr.symbol_size()
    root = _parse_xml(out)
    ok_('width' in root.attrib)
    eq_('%dmm' % width, root.attrib['width'])
    ok_('height' in root.attrib)
    eq_('%dmm' % height, root.attrib['height'])
    ok_('viewBox' in root.attrib)
    eq_('0 0 %d %d' % (width, height), root.attrib['viewBox'])


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
    eq_(b'<?xml ', val)
    eq_(title, _get_title(root).text)
    eq_(desc, _get_desc(root).text)


def svg_as_matrix(buff, border):
    """\
    Returns the QR code path as list of [0,1] lists.
    """
    root = _parse_xml(buff)
    path = _get_path(root)
    h = root.attrib['height']
    w = root.attrib['width']
    if h != w:
        raise ValueError('Expected equal height/width, got height="{}" width="{}"'.format(h, w))
    size = int(w) - 2 * border
    d = path.attrib['d']
    res = []
    res_row = None
    absolute_x = -border
    for op, x, y, l in re.findall(r'([Mm])(\-?[0-9]+(?:\.[0-9]+)?) (\-?[0-9]+(?:\.[0-9]+)?)h([0-9]+)', d):
        x = int(x)
        y = float(y)
        l = int(l)
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
            absolute_x += l
        elif op == 'M':
            absolute_x = l
            if x != border:
                raise ValueError('Unexpected border width. Expected "{}", got "{}"'.format(border, x))
        res_row.extend([1] * l)
    res_row.extend([0] * (size - len(res_row)))
    return res


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
