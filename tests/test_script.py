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
from segno.scripts import cmd


def test_defaults():
    args = cmd.parse(())
    assert args.content == ''
    assert args.error is None
    assert args.mask is None
    assert args.version is None
    assert args.scale == 1
    assert not args.micro
    assert args.output is None
    assert args.border is None
    assert args.color is None
    assert args.background is None


def test_error():
    args = cmd.parse(['-e', 'm'])
    assert args.error == 'M'


def test_error2():
    args = cmd.parse(['-e', 'M'])
    assert args.error == 'M'


def test_error3():
    args = cmd.parse(['-e', '-'])
    assert args.error is None


def test_error4():
    args = cmd.parse(['--error', 'q'])
    assert args.error == 'Q'


def test_version():
    args = cmd.parse(['-v', '1'])
    assert args.version == '1'


def test_version2():
    args = cmd.parse(['--version', '40'])
    assert args.version == '40'


def test_version_micro():
    args = cmd.parse(['-v', 'M1'])
    assert args.version == 'M1'


def test_mask():
    args = cmd.parse(['-m', '1'])
    assert args.mask == 1


def test_mask2():
    args = cmd.parse(['--mask', '5'])
    assert args.mask == 5


def test_micro_false():
    args = cmd.parse(['--no-micro'])
    assert not args.micro


def test_micro_true():
    args = cmd.parse(['--micro'])
    assert args.micro


def test_border():
    args = cmd.parse(['--border', '0'])
    assert args.border == 0


def test_scale():
    args = cmd.parse(['--scale', '1.6'])
    assert args.scale == 1.6


def test_color():
    args = cmd.parse(['--color', 'green'])
    assert args.color == 'green'


def test_background():
    args = cmd.parse(['--background', 'red'])
    assert args.background == 'red'


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


if __name__ == '__main__':
    import pytest
    pytest.main(['-x', __file__])
