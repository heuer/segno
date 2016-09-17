# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the command line script.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import os
import tempfile
import gzip
import pytest
from segno.scripts import cmd


def test_defaults():
    args = cmd.parse([''])
    assert args.content == ''
    assert args.error is None
    assert args.mode is None
    assert args.pattern is None
    assert args.version is None
    assert args.scale == 1
    assert not args.micro
    assert args.output is None
    assert args.border is None
    assert args.color is None
    assert args.background is None
    assert args.boost_error
    # PNG
    assert args.addad
    # SVG
    assert args.xmldecl
    assert not args.no_classes
    assert args.encoding == 'utf-8'
    assert args.title is None
    assert args.desc is None
    assert args.svgns is True
    assert args.svgid is None
    assert args.svgclass is None
    assert args.lineclass is None
    assert args.omitsize is False
    assert args.unit is None
    assert args.svgversion is None
    assert args.nl is True


def test_segno_version():
    with pytest.raises(SystemExit) as e:
        cmd.parse(['', '--ver'])
        assert 0 == e.exception.code


def test_error():
    args = cmd.parse(['', '-e', 'm'])
    assert args.error == 'M'
    qr = cmd.make_code(args)
    assert 'H' == qr.error


def test_error2():
    args = cmd.parse(['', '-e', 'M'])
    assert args.error == 'M'
    qr = cmd.make_code(args)
    assert 'H' == qr.error


def test_error3():
    args = cmd.parse(['123', '-e', '-'])
    assert args.error is None
    qr = cmd.make_code(args)
    assert not qr.is_micro
    assert 1 == qr.version
    assert 'H' == qr.error


def test_error_allow_micro():
    args = cmd.parse(['123', '-e', '-', '--micro'])
    assert args.error is None
    qr = cmd.make_code(args)
    assert qr.is_micro
    assert 'M1' == qr.version
    assert qr.error is None


def test_error4():
    args = cmd.parse(['', '--error=q', '--no-error-boost'])
    assert args.error == 'Q'
    qr = cmd.make_code(args)
    assert 'Q' == qr.error


def test_version():
    args = cmd.parse(['', '-v', '1'])
    assert args.version == '1'
    qr = cmd.make_code(args)
    assert 1 == qr.version


def test_version2():
    args = cmd.parse(['', '--version', '40'])
    assert args.version == '40'
    qr = cmd.make_code(args)
    assert 40 == qr.version


def test_version_micro():
    args = cmd.parse(['0', '-v', 'M1'])
    assert args.version == 'M1'
    qr = cmd.make_code(args)
    assert 'M1' == qr.version


def test_mode():
    args = cmd.parse(['A', '-m', 'alphanumeric'])
    assert args.mode == 'alphanumeric'
    qr = cmd.make_code(args)
    assert 'alphanumeric' == qr.mode


def test_mode2():
    args = cmd.parse(['', '--mode=byte'])
    assert args.mode == 'byte'
    qr = cmd.make_code(args)
    assert 'byte' == qr.mode


def test_pattern():
    args = cmd.parse(['', '-p', '1'])
    assert args.pattern == 1
    qr = cmd.make_code(args)
    assert qr.mask == 1


def test_pattern2():
    args = cmd.parse(['', '--pattern', '5'])
    assert args.pattern == 5
    qr = cmd.make_code(args)
    assert qr.mask == 5


def test_micro_false():
    args = cmd.parse(['', '--no-micro'])
    assert not args.micro
    qr = cmd.make_code(args)
    assert not qr.is_micro


def test_micro_true():
    args = cmd.parse(['', '--micro'])
    assert args.micro
    qr = cmd.make_code(args)
    assert qr.is_micro


def test_boost_error_disable():
    args = cmd.parse(['', '--no-error-boost'])
    assert not args.boost_error


def test_border():
    args = cmd.parse(['', '--border', '0'])
    assert args.border == 0


def test_scale():
    args = cmd.parse(['', '--scale=1.6'])
    assert args.scale == 1.6


def test_scale2():
    args = cmd.parse(['', '--scale=2.0'])
    assert args.scale == 2
    assert isinstance(args.scale, int)


def test_color():
    args = cmd.parse(['', '--color', 'green'])
    assert args.color == 'green'


def test_color_transparent():
    args = cmd.parse(['', '--color=transparent', '-output=x.png'])
    assert args.color == 'transparent'
    assert cmd.build_config(args)['color'] is None


def test_color_transparent2():
    args = cmd.parse(['', '--color=trans', '-output=x.png'])
    assert args.color == 'trans'
    assert cmd.build_config(args)['color'] is None


def test_background():
    args = cmd.parse(['', '--background', 'red'])
    assert args.background == 'red'


def test_background_transparent():
    args = cmd.parse(['', '--background=transparent', '-output=x.png'])
    assert args.background == 'transparent'
    assert cmd.build_config(args)['background'] is None


def test_background_transparent2():
    args = cmd.parse(['', '--background=trans', '-output=x.png'])
    assert args.background == 'trans'
    assert cmd.build_config(args)['background'] is None


def test_output():
    data = (('svg', b'<?xml ', 'rb'),
            ('pdf', b'%PDF-', 'rb'),
            ('png', b'\211PNG\r\n\032\n', 'rb'),
            ('svgz', b'\x1f\x8b\x08', 'rb'),
            ('txt', '000000', 'rt'),
            ('eps', '%!PS-Adobe-3.0 EPSF-3.0', 'rt'),
            ('ans', '\033[7m       ', 'rt'),
    )

    def check(arg, ext, expected, mode):
        f = tempfile.NamedTemporaryFile('w', suffix='.{0}'.format(ext), delete=False)
        f.close()
        try:
            cmd.main(['test', arg, f.name])
            f = open(f.name, mode=mode)
            val = f.read(len(expected))
            f.close()
            assert expected == val
        finally:
            os.unlink(f.name)
    for arg in ('--output', '-o'):
        for ext, expected, mode in data:
            yield check, arg, ext, expected, mode


# -- PNG
def test_noad():
    args = cmd.parse(['', '--no-ad'])
    assert not args.addad


# -- SVG
def test_xmldecl():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.xmldecl
    assert cmd.build_config(args)['xmldecl'] is True


def test_omit_xmldecl():
    args = cmd.parse(['', '--no-xmldecl', '--output=x.svg'])
    assert not args.xmldecl
    assert cmd.build_config(args)['xmldecl'] is False


def test_not_omit_classes():
    args = cmd.parse(['', '--output=x.svg'])
    assert not args.no_classes
    config = cmd.build_config(args)
    assert 'svgclass' not in config
    assert 'lineclass' not in config


def test_omit_classes():
    args = cmd.parse(['', '--no-classes', '--output=x.svg'])
    assert args.no_classes
    config = cmd.build_config(args)
    assert config['svgclass'] is None
    assert config['lineclass'] is None


def test_encoding():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.encoding == 'utf-8'
    assert cmd.build_config(args)['encoding'] == 'utf-8'


def test_encoding2():
    args = cmd.parse(['', '--encoding=ascii', '--output=x.svg'])
    assert args.encoding == 'ascii'
    assert cmd.build_config(args)['encoding'] == 'ascii'


def test_title():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.title is None
    assert cmd.build_config(args)['title'] is None


def test_title2():
    args = cmd.parse(['', '--title=Magnolia', '--output=x.svg'])
    assert args.title == 'Magnolia'
    assert cmd.build_config(args)['title'] == 'Magnolia'


def test_desc():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.desc is None
    assert cmd.build_config(args)['desc'] is None


def test_desc2():
    args = cmd.parse(['', '--desc=Magnolia', '--output=x.svg'])
    assert args.desc == 'Magnolia'
    assert cmd.build_config(args)['desc'] == 'Magnolia'


def test_nl():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.nl is True
    assert cmd.build_config(args)['nl'] is True


def test_nl2():
    args = cmd.parse(['', '--no-newline', '--output=x.svg'])
    assert not args.nl
    assert cmd.build_config(args)['nl'] is False


def test_ns():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.svgns is True
    assert cmd.build_config(args)['svgns'] is True


def test_ns2():
    args = cmd.parse(['', '--no-namespace', '--output=x.svg'])
    assert not args.svgns
    assert cmd.build_config(args)['svgns'] is False


def test_svgid():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.svgid is None
    assert 'svgid' not in cmd.build_config(args)


def test_svgid2():
    args = cmd.parse(['', '--svgid=magnolia', '--output=x.svg'])
    assert args.svgid == 'magnolia'
    assert cmd.build_config(args)['svgid'] == 'magnolia'


def test_svgclass():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.svgclass is None
    assert 'svgclass' not in cmd.build_config(args)


def test_svgclass2():
    args = cmd.parse(['', '--svgclass=magnolia', '--output=x.svg'])
    assert args.svgclass == 'magnolia'
    assert cmd.build_config(args)['svgclass'] == 'magnolia'


def test_svg_lineclass():
    args = cmd.parse(['', '--output=x.svg'])
    assert args.lineclass is None
    assert 'lineclass' not in cmd.build_config(args)


def test_svg_lineclass2():
    args = cmd.parse(['', '--lineclass=magnolia'])
    assert args.lineclass == 'magnolia'
    assert cmd.build_config(args)['lineclass'] == 'magnolia'


def test_omitsize():
    args = cmd.parse(['', '--output=x.svg'])
    assert not args.omitsize
    assert cmd.build_config(args)['omitsize'] is False


def test_omitsize2():
    args = cmd.parse(['', '--no-size'])
    assert args.omitsize
    assert cmd.build_config(args)['omitsize'] is True


def test_unit():
    args = cmd.parse([''])
    assert args.unit is None
    assert cmd.build_config(args)['unit'] is None


def test_unit2():
    args = cmd.parse(['', '--unit=cm'])
    assert args.unit == 'cm'
    assert cmd.build_config(args)['unit'] == 'cm'


def test_svgversion():
    args = cmd.parse([''])
    assert args.svgversion is None
    assert cmd.build_config(args)['svgversion'] is None


def test_svgversion2():
    args = cmd.parse(['', '--svgversion=1'])
    assert args.svgversion == 1.0
    assert cmd.build_config(args)['svgversion'] == 1.0


def test_svgversion3():
    args = cmd.parse(['', '--svgversion=1.1'])
    assert args.svgversion == 1.1
    assert cmd.build_config(args)['svgversion'] == 1.1


def test_png_svg_command():
    args = cmd.parse(['', '--svgversion=1.1'])
    assert args.svgversion == 1.1
    assert 'svgversion' in cmd.build_config(args)
    assert 'svgversion' not in cmd.build_config(args, filename='x.png')


def test_output_svgz():
    f = tempfile.NamedTemporaryFile('w', suffix='.svgz', delete=False)
    f.close()
    cmd.main(['test', '--scale=10', '--color=red', '--output={0}'.format(f.name)])
    f = gzip.open(f.name)
    content = f.read()
    f.close()
    os.unlink(f.name)
    assert b'scale(10)' in content
    assert b'stroke="red"' in content



if __name__ == '__main__':
    pytest.main([__file__])
