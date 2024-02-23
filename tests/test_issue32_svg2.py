#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #32.
<https://github.com/heuer/segno/issues/32>

SVG version 2.0 shouldn't have a version attribute.
"""
import io
import xml.etree.ElementTree as etree
import pytest
import segno

_SVG_NS = 'http://www.w3.org/2000/svg'


def _parse_xml(buff):
    """\
    Parses XML and returns the root element.
    """
    buff.seek(0)
    return etree.parse(buff).getroot()


def _get_svg_el(root, name):
    return root.find('{%s}%s' % (_SVG_NS, name))


def _get_path(root):
    return _get_svg_el(root, 'path')


def test_version_none():
    qr = segno.make('Test')
    out = io.BytesIO()
    qr.save(out, kind='svg', dark='#0000ffcc')
    root = _parse_xml(out)
    assert root.get('version') is None
    assert b'stroke-opacity' in out.getvalue()
    assert b'rgba(' not in out.getvalue()


def test_version_1_1():
    qr = segno.make('Test')
    out = io.BytesIO()
    qr.save(out, svgversion=1.1, kind='svg', dark='#0000ffcc')
    root = _parse_xml(out)
    assert '1.1' == root.get('version')
    assert b'stroke-opacity' in out.getvalue()
    assert b'rgba(' not in out.getvalue()


def test_version_2_0():
    qr = segno.make('Test')
    out = io.BytesIO()
    qr.save(out, svgversion=2.0, kind='svg', dark='#0000ffcc')
    root = _parse_xml(out)
    assert root.get('version') is None
    assert b'stroke-opacity' not in out.getvalue()
    assert b'rgba(' in out.getvalue()


if __name__ == '__main__':
    pytest.main([__file__])
