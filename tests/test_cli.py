# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2017 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the command line script.
"""
from __future__ import absolute_import, unicode_literals
import os
import tempfile
import gzip
import shutil
import pytest
from segno import cli


def test_defaults():
    args = cli.parse([''])
    assert args.content == ['']
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
    assert not args.seq
    assert args.symbol_count is None
    # PNG
    assert args.addad
    assert not args.dpi
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
        cli.parse(['--ver', ''])
        assert 0 == e.exception.code


def test_segno_version_shortcut():
    with pytest.raises(SystemExit) as e:
        cli.parse(['-V', ''])
        assert 0 == e.exception.code


def test_noargs():
    with pytest.raises(SystemExit) as e:
        cli.parse([])
        assert 1 == e.exception.code


def test_error():
    args = cli.parse(['-e', 'm', ''])
    assert args.error == 'M'
    qr = cli.make_code(args)
    assert 'H' == qr.error


def test_error2():
    args = cli.parse(['-e', 'M', ''])
    assert args.error == 'M'
    qr = cli.make_code(args)
    assert 'H' == qr.error


def test_error3():
    args = cli.parse(['-e', '-', '123'])
    assert args.error is None
    qr = cli.make_code(args)
    assert not qr.is_micro
    assert 1 == qr.version
    assert 'H' == qr.error


def test_error_allow_micro():
    args = cli.parse(['-e', '-', '--micro', '123'])
    assert args.error is None
    qr = cli.make_code(args)
    assert qr.is_micro
    assert 'M1' == qr.version
    assert qr.error is None


def test_error4():
    args = cli.parse(['--error=q', '--no-error-boost', ''])
    assert args.error == 'Q'
    qr = cli.make_code(args)
    assert 'Q' == qr.error


def test_version():
    args = cli.parse(['-v', '1', ''])
    assert args.version == '1'
    qr = cli.make_code(args)
    assert 1 == qr.version


def test_version2():
    args = cli.parse(['--version', '40', ''])
    assert args.version == '40'
    qr = cli.make_code(args)
    assert 40 == qr.version


def test_version_micro():
    args = cli.parse(['-v', 'M1', '0'])
    assert args.version == 'M1'
    qr = cli.make_code(args)
    assert 'M1' == qr.version


def test_version_micro_m1():
    args = cli.parse(['-v', 'M1', '12345'])
    assert args.version == 'M1'
    qr = cli.make_code(args)
    assert 'M1' == qr.version


def test_version_micro_m1_automatic():
    args = cli.parse(['--micro', '12345'])
    qr = cli.make_code(args)
    assert 'M1' == qr.version


def test_version_micro_m2_automatic():
    args = cli.parse(['--micro', '123456'])
    qr = cli.make_code(args)
    assert 'M2' == qr.version


def test_mode():
    args = cli.parse(['-m', 'alphanumeric', 'A'])
    assert args.mode == 'alphanumeric'
    qr = cli.make_code(args)
    assert 'alphanumeric' == qr.mode


def test_mode2():
    args = cli.parse(['--mode=byte', ''])
    assert args.mode == 'byte'
    qr = cli.make_code(args)
    assert 'byte' == qr.mode


def test_pattern():
    args = cli.parse(['-p', '1', ''])
    assert args.pattern == 1
    qr = cli.make_code(args)
    assert qr.mask == 1


def test_pattern2():
    args = cli.parse(['--pattern', '5', ''])
    assert args.pattern == 5
    qr = cli.make_code(args)
    assert qr.mask == 5


def test_micro_false():
    args = cli.parse(['--no-micro', ''])
    assert not args.micro
    qr = cli.make_code(args)
    assert not qr.is_micro


def test_micro_true():
    args = cli.parse(['--micro', ''])
    assert args.micro
    qr = cli.make_code(args)
    assert qr.is_micro


def test_boost_error_disable():
    args = cli.parse(['--no-error-boost', ''])
    assert not args.boost_error


def test_border():
    args = cli.parse(['--border', '0', ''])
    assert args.border == 0


def test_border_shortcut():
    args = cli.parse(['-b', '10', ''])
    assert args.border == 10


def test_scale():
    args = cli.parse(['--scale=1.6', ''])
    assert args.scale == 1.6


def test_scale2():
    args = cli.parse(['--scale=2.0', ''])
    assert args.scale == 2
    assert isinstance(args.scale, int)


def test_scale_shortcut():
    args = cli.parse(['-s=1.6', ''])
    assert args.scale == 1.6


def test_sequence():
    args = cli.parse(['--seq', '-v=1', ''])
    assert args.seq
    assert '1' == args.version


def test_sequence_symbol_count():
    args = cli.parse(['--seq', '--symbol-count=4', ''])
    assert args.seq
    assert 4 == args.symbol_count


def test_sequence_symbol_count_shortcut():
    args = cli.parse(['--seq', '-sc=8', ''])
    assert args.seq
    assert 8 == args.symbol_count


def test_sequence_output():
    directory = tempfile.mkdtemp()
    assert 0 == len(os.listdir(directory))
    cli.main(['--seq', '-v=1', '-e=m', '-o=' + os.path.join(directory, 'test.svg'), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'])
    number_of_files = len(os.listdir(directory))
    shutil.rmtree(directory)
    assert 4 == number_of_files


def test_color():
    args = cli.parse(['--color', 'green', ''])
    assert args.color == 'green'


def test_color_transparent():
    args = cli.parse(['--color=transparent', '-output=x.png', ''])
    assert args.color == 'transparent'
    assert cli.build_config(args)['color'] is None


def test_color_transparent2():
    args = cli.parse(['--color=trans', '-output=x.png', ''])
    assert args.color == 'trans'
    assert cli.build_config(args)['color'] is None


def test_background():
    args = cli.parse(['--background', 'red', ''])
    assert args.background == 'red'


def test_background_transparent():
    args = cli.parse(['--background=transparent', '-output=x.png', ''])
    assert args.background == 'transparent'
    assert cli.build_config(args)['background'] is None


def test_background_transparent2():
    args = cli.parse(['--background=trans', '-output=x.png', ''])
    assert args.background == 'trans'
    assert cli.build_config(args)['background'] is None


@pytest.mark.parametrize('arg', ['-o', '--output'])
@pytest.mark.parametrize('ext, expected, mode', [('svg', b'<?xml ', 'rb'),
                                                 ('pdf', b'%PDF-', 'rb'),
                                                 ('png', b'\211PNG\r\n\032\n', 'rb'),
                                                 ('svgz', b'\x1f\x8b\x08', 'rb'),
                                                 ('txt', '000000', 'rt'),
                                                 ('eps', '%!PS-Adobe-3.0 EPSF-3.0', 'rt'),
                                                 ('ans', '\033[7m       ', 'rt'),
                                                 ('pam', b'P7', 'rb'),
                                                 ('pbm', b'P4\n', 'rb'),
                                                 ('xbm', '#define ', 'rt'),
                                                 ('xpm', '/* XPM */', 'rt'),
                                                 ('tex', '%% Creator: ', 'rt'),])
def test_output(arg, ext, expected, mode):
    f = tempfile.NamedTemporaryFile('w', suffix='.{0}'.format(ext), delete=False)
    f.close()
    try:
        cli.main(['test', arg, f.name])
        f = open(f.name, mode=mode)
        val = f.read(len(expected))
        f.close()
        assert expected == val
    finally:
        os.unlink(f.name)


def test_terminal(capsys):
    cli.main(['test'])
    out, err = capsys.readouterr()
    assert out


# -- PNG
def test_noad():
    args = cli.parse(['--no-ad', ''])
    assert not args.addad


def test_dpi():
    args = cli.parse(['--dpi=300', ''])
    assert 300 == args.dpi


# -- SVG
def test_xmldecl():
    args = cli.parse(['--output=x.svg', ''])
    assert args.xmldecl
    assert cli.build_config(args)['xmldecl'] is True


def test_omit_xmldecl():
    args = cli.parse(['--no-xmldecl', '--output=x.svg', ''])
    assert not args.xmldecl
    assert cli.build_config(args)['xmldecl'] is False


def test_not_omit_classes():
    args = cli.parse(['--output=x.svg', ''])
    assert not args.no_classes
    config = cli.build_config(args)
    assert 'svgclass' not in config
    assert 'lineclass' not in config


def test_omit_classes():
    args = cli.parse(['--no-classes', '--output=x.svg', ''])
    assert args.no_classes
    config = cli.build_config(args)
    assert config['svgclass'] is None
    assert config['lineclass'] is None


def test_encoding():
    args = cli.parse(['--output=x.svg', ''])
    assert args.encoding == 'utf-8'
    assert cli.build_config(args)['encoding'] == 'utf-8'


def test_encoding2():
    args = cli.parse(['--encoding=ascii', '--output=x.svg', ''])
    assert args.encoding == 'ascii'
    assert cli.build_config(args)['encoding'] == 'ascii'


def test_title():
    args = cli.parse(['--output=x.svg', ''])
    assert args.title is None
    assert cli.build_config(args)['title'] is None


def test_title2():
    args = cli.parse(['--title=Magnolia', '--output=x.svg', ''])
    assert args.title == 'Magnolia'
    assert cli.build_config(args)['title'] == 'Magnolia'


def test_desc():
    args = cli.parse(['--output=x.svg', ''])
    assert args.desc is None
    assert cli.build_config(args)['desc'] is None


def test_desc2():
    args = cli.parse(['--desc=Magnolia', '--output=x.svg', ''])
    assert args.desc == 'Magnolia'
    assert cli.build_config(args)['desc'] == 'Magnolia'


def test_nl():
    args = cli.parse(['--output=x.svg', ''])
    assert args.nl is True
    assert cli.build_config(args)['nl'] is True


def test_nl2():
    args = cli.parse(['--no-newline', '--output=x.svg', ''])
    assert not args.nl
    assert cli.build_config(args)['nl'] is False


def test_ns():
    args = cli.parse(['--output=x.svg', ''])
    assert args.svgns is True
    assert cli.build_config(args)['svgns'] is True


def test_ns2():
    args = cli.parse(['--no-namespace', '--output=x.svg', ''])
    assert not args.svgns
    assert cli.build_config(args)['svgns'] is False


def test_svgid():
    args = cli.parse(['--output=x.svg', ''])
    assert args.svgid is None
    assert 'svgid' not in cli.build_config(args)


def test_svgid2():
    args = cli.parse(['--svgid=magnolia', '--output=x.svg', ''])
    assert args.svgid == 'magnolia'
    assert cli.build_config(args)['svgid'] == 'magnolia'


def test_svgclass():
    args = cli.parse(['--output=x.svg', ''])
    assert args.svgclass is None
    assert 'svgclass' not in cli.build_config(args)


def test_svgclass2():
    args = cli.parse(['--svgclass=magnolia', '--output=x.svg', ''])
    assert args.svgclass == 'magnolia'
    assert cli.build_config(args)['svgclass'] == 'magnolia'


def test_svg_lineclass():
    args = cli.parse(['--output=x.svg', ''])
    assert args.lineclass is None
    assert 'lineclass' not in cli.build_config(args)


def test_svg_lineclass2():
    args = cli.parse(['--lineclass=magnolia', ''])
    assert args.lineclass == 'magnolia'
    assert cli.build_config(args)['lineclass'] == 'magnolia'


def test_omitsize():
    args = cli.parse(['--output=x.svg', ''])
    assert not args.omitsize
    assert cli.build_config(args)['omitsize'] is False


def test_omitsize2():
    args = cli.parse(['--no-size', ''])
    assert args.omitsize
    assert cli.build_config(args)['omitsize'] is True


def test_unit():
    args = cli.parse([''])
    assert args.unit is None
    assert cli.build_config(args)['unit'] is None


def test_unit2():
    args = cli.parse(['--unit=cm', ''])
    assert args.unit == 'cm'
    assert cli.build_config(args)['unit'] == 'cm'


def test_svgversion():
    args = cli.parse([''])
    assert args.svgversion is None
    assert cli.build_config(args)['svgversion'] is None


def test_svgversion2():
    args = cli.parse(['--svgversion=1', ''])
    assert args.svgversion == 1.0
    assert cli.build_config(args)['svgversion'] == 1.0


def test_svgversion3():
    args = cli.parse(['--svgversion=1.1', ''])
    assert args.svgversion == 1.1
    assert cli.build_config(args)['svgversion'] == 1.1


def test_png_svg_command():
    args = cli.parse(['--svgversion=1.1', ''])
    assert args.svgversion == 1.1
    assert 'svgversion' in cli.build_config(args)
    assert 'svgversion' not in cli.build_config(args, filename='x.png')


def test_output_svgz():
    f = tempfile.NamedTemporaryFile('w', suffix='.svgz', delete=False)
    f.close()
    cli.main(['--scale=10', '--color=red', '--output={0}'.format(f.name), 'test'])
    f = gzip.open(f.name)
    content = f.read()
    f.close()
    os.unlink(f.name)
    assert b'scale(10)' in content
    assert b'stroke="red"' in content


if __name__ == '__main__':
    pytest.main([__file__])
