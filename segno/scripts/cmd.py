#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Command line script to generate QR Codes with Segno.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
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
                                     description='Segno QR Code and Micro QR Code generator')
    parser.add_argument('content', help='The content to encode')
    parser.add_argument('--version', '-v', help='(Micro) QR Code version: 1 .. 40 or "M1", "M2", "M3", "M4"',
                        required=False,)
    parser.add_argument('--error', '-e', help='Error correction level: "L": 7%%, "M": 15%% (default), "Q": 25%%, "H": 30%%, "-": no error correction (used for M1 symbols)',
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
    parser.add_argument('--scale', help='Scaling factor',
                        default=1,
                        type=_convert_scale)
    parser.add_argument('--border', help='Size of the border / quiet zone',
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
    png_group = parser.add_argument_group('PNG', 'PNG specific options')
    png_group.add_argument('--no-ad', help='Omits the "Software" comment in the PNG file',
                           dest='addad',
                           action='store_false')
    return parser


def parse(args):
    """\
    Parses the arguments and returns the result.
    """
    parser = make_parser()
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
    return parsed_args


def build_config(args):
    """\
    Builds a configuration and returns it. The config contains only keywords,
    which are supported by the serializer. Unsupported values are ignored.
    """
    config = dict()
    config.update(vars(args))
    # Remove args which are used to build the QR Code
    for name in ('content', 'mode', 'error', 'version', 'pattern', 'micro',
                 'output'):
        config.pop(name, None)
    # Done here since it seems not to be possible to detect if an argument
    # was supplied by the user or if it's the default argument.
    # If using type=lambda v: None if v in ('transparent', 'trans') else v
    # we cannot detect if "None" comes from "transparent" or the default value
    for clr in ('color', 'background'):
        val = config[clr]
        if val is None:
            del config[clr]
        elif val in ('transparent', 'trans'):
            config[clr] = None
    fname = args.output
    ext = fname[fname.rfind('.') + 1:].lower()
    if ext == 'svgz':  # There is no svgz serializer, use same config as svg
        ext = 'svg'
    supported_args = _EXT_TO_KW_MAPPING.get(ext, ())
    # Drop unsupported arguments from config rather than getting a
    # "unsupported keyword" exception
    for k in list(config):
        if k not in supported_args:
            del config[k]
    return config


def main(args=sys.argv[1:]):
    args = parse(args)
    qr = segno.make(args.content, mode=args.mode, error=args.error,
                    version=args.version, mask=args.pattern, micro=args.micro)
    if args.output is None:
        qr.terminal(border=args.border)
    else:
        qr.save(args.output, **build_config(args))


if __name__ == '__main__':  # pragma: no cover
    main()
