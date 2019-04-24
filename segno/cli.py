#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Command line script to generate QR Codes with Segno.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.
"""
from __future__ import absolute_import, unicode_literals
import os
import sys
import argparse
import segno
from segno import writers


# file extension to supported keywords mapping
_EXT_TO_KW_MAPPING = {}

for ext, func in writers._VALID_SERIALISERS.items():
    if len(ext) > 3:
        continue
    # Python 2 vs Python 3
    func_code = getattr(func, 'func_code', None) or func.__code__
    defaults = getattr(func, 'func_defaults', None) or func.__defaults__
    args = func_code.co_varnames[:func_code.co_argcount]
    _EXT_TO_KW_MAPPING[ext] = args[-len(defaults):]

del writers


def make_parser():
    """\
    Returns the command line parser.
    """

    def _convert_scale(val):
        val = float(val)
        return val if val != int(val) else int(val)

    parser = argparse.ArgumentParser(prog='segno',
                                     description='Segno QR Code and Micro QR Code generator version {0}'.format(segno.__version__))
    parser.add_argument('--version', '-v', help='(Micro) QR Code version: 1 .. 40 or "M1", "M2", "M3", "M4"',
                        required=False,)
    parser.add_argument('--error', '-e', help='Error correction level: "L": 7%% (default), "M": 15%%, "Q": 25%%, "H": 30%%, "-": no error correction (used for M1 symbols)',
                        choices=('L', 'M', 'Q', 'H', '-'),
                        default=None,
                        type=lambda x: x.upper())
    parser.add_argument('--mode', '-m', help='Mode',
                        choices=('numeric', 'alphanumeric', 'byte', 'kanji'),
                        default=None,
                        type=lambda x: x.lower())
    parser.add_argument('--pattern', '-p', help='Mask pattern to use',
                        required=False,
                        default=None,
                        type=int)
    parser.add_argument('--scale', '-s', help='Scaling factor',
                        default=1,
                        type=_convert_scale)
    parser.add_argument('--border', '-b', help='Size of the border / quiet zone',
                        default=None,
                        type=int)
    parser.add_argument('--micro', help='Allow the creation of Micro QR Codes',
                        dest='micro', action='store_true')
    parser.add_argument('--no-micro', help='Disallow creation of Micro QR Codes (default)',
                        dest='micro', action='store_false')
    parser.add_argument('--color', help='Color of the dark modules. Use "transparent" to set the color to None (not supported by all serializers)')
    parser.add_argument('--background', help='Color of the light modules. Use "transparent" to set the background to None (not supported by all serializers)')
    parser.add_argument('--output', '-o', help='Output file. If not specified, the QR Code is printed to the terminal',
                        required=False,
                        )
    parser.add_argument('--no-error-boost', help='Disables the automatic error incrementation if a higher error correction level is possible',
                        dest='boost_error', action='store_false')
    parser.add_argument('--seq', help='Creates a sequence of QR Codes (Structured Append mode). Version or symbol count must be provided',
                        dest='seq', action='store_true')
    parser.add_argument('--symbol-count', '-sc', help='Number of symbols to create',
                        default=None,
                        type=int)
    # SVG
    svg_group = parser.add_argument_group('SVG', 'SVG specific options')
    svg_group.add_argument('--no-classes', help='Omits the (default) SVG classes',
                           action='store_true')
    svg_group.add_argument('--no-xmldecl', help='Omits the XML declaration header',
                           dest='xmldecl',
                           action='store_false')
    svg_group.add_argument('--no-namespace', help='Indicates that the SVG document should have no SVG namespace declaration',
                           dest='svgns',
                           action='store_false')
    svg_group.add_argument('--no-newline', help='Indicates that the SVG document should have no trailing newline',
                           dest='nl',
                           action='store_false')
    svg_group.add_argument('--title', help='Specifies the title of the SVG document')
    svg_group.add_argument('--desc', help='Specifies the description of the SVG document')
    svg_group.add_argument('--svgid', help='Indicates the ID of the <svg/> element')
    svg_group.add_argument('--svgclass', help='Indicates the CSS class of the <svg/> element')
    svg_group.add_argument('--lineclass', help='Indicates the CSS class of the <path/> element (the dark modules)')
    svg_group.add_argument('--no-size', help='Indicates that the SVG document should not have "width" and "height" attributes',
                           dest='omitsize',
                           action='store_true')
    svg_group.add_argument('--unit', help='Indicates SVG coordinate system unit')
    svg_group.add_argument('--svgversion', help='Indicates the SVG version',
                           type=float)
    svg_group.add_argument('--encoding', help='Specifies the encoding of the document',
                           default='utf-8')
    # PNG
    png_group = parser.add_argument_group('PNG', 'PNG specific options')
    png_group.add_argument('--dpi', help='Sets the DPI value of the PNG file',
                           type=int)
    png_group.add_argument('--no-ad', help='Omits the "Software" comment in the PNG file',
                           dest='addad',
                           action='store_false')
    parser.add_mutually_exclusive_group().add_argument('--ver', '-V', help="Shows Segno's version",
                                                       action='version',
                                                       version='Segno {0}'.format(segno.__version__))
    parser.add_argument('content', nargs='+', help='The content to encode')
    return parser


def parse(args):
    """\
    Parses the arguments and returns the result.
    """
    parser = make_parser()
    if not len(args):
        parser.print_help()
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    if parsed_args.error == '-':
        parsed_args.error = None
    # 'micro' is False by default. If version is set to a Micro QR Code version,
    # encoder.encode raises a VersionError.
    # Small problem: --version=M4 --no-micro is allowed
    version = parsed_args.version
    if version is not None:
        version = str(version).upper()
    if not parsed_args.micro and version in ('M1', 'M2', 'M3', 'M4'):
        parsed_args.micro = None
    return _AttrDict(vars(parsed_args))


def build_config(config, filename=None):
    """\
    Builds a configuration and returns it. The config contains only keywords,
    which are supported by the serializer. Unsupported values are ignored.
    """
    # Done here since it seems not to be possible to detect if an argument
    # was supplied by the user or if it's the default argument.
    # If using type=lambda v: None if v in ('transparent', 'trans') else v
    # we cannot detect if "None" comes from "transparent" or the default value
    for clr in ('color', 'background'):
        val = config.pop(clr, None)
        if val in ('transparent', 'trans'):
            config[clr] = None
        elif val:
            config[clr] = val
    # SVG
    for name in ('svgid', 'svgclass', 'lineclass'):
        if config.get(name, None) is None:
            config.pop(name, None)
    if config.pop('no_classes', False):
        config['svgclass'] = None
        config['lineclass'] = None
    if filename is not None:
        ext = filename[filename.rfind('.') + 1:].lower()
        if ext == 'svgz':  # There is no svgz serializer, use same config as svg
            ext = 'svg'
        supported_args = _EXT_TO_KW_MAPPING.get(ext, ())
        # Drop unsupported arguments from config rather than getting a
        # "unsupported keyword" exception
        for k in list(config):
            if k not in supported_args:
                del config[k]
    return config


def make_code(config):
    make = segno.make
    kw = dict(mode=config.pop('mode'), error=config.pop('error'),
              version=config.pop('version'), mask=config.pop('pattern'),
              boost_error=config.pop('boost_error'))
    if config.pop('seq'):
        make = segno.make_sequence
        kw['symbol_count'] = config.pop('symbol_count')
    else:
        kw['micro'] = config.pop('micro')
    return make(' '.join(config.pop('content')), **kw)


def main(args=sys.argv[1:]):
    config = parse(args)
    try:
        qr = make_code(config)
    except segno.QRCodeError as ex:
        sys.stderr.writelines([str(ex), os.linesep])
        return sys.exit(1)
    output = config.pop('output')
    if output is None:
        qr.terminal(border=config['border'])
    else:
        qr.save(output, **build_config(config, filename=output))
    return 0


class _AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(_AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


if __name__ == '__main__':  # pragma: no cover
    main()
