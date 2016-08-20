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
import argparse
import segno
from segno import writers
import sys


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


def parse(args):
    """\
    Parses the arguments and returns the result.
    """
    parser = argparse.ArgumentParser(description='Segno QR Code and Micro QR Code generator')
    parser.add_argument('content', nargs='?', default='')
    parser.add_argument('--version', '-v', help='(Micro) QR Code version: 1 .. 40 or "M1", "M2", "M3", "M4"',
                        required=False,)
    parser.add_argument('--error', '-e', help='Error correction level: "L": 7%%, "M": 15%% (default), "Q": 25%%, "H": 30%%, "-": no error correction (used for M1 symbols)',
                        required=False,
                        choices=('L', 'M', 'Q', 'H', '-'),
                        default=None,
                        type=lambda x: x.upper())
    parser.add_argument('--mask', '-m', help='Mask pattern to use',
                        required=False,
                        default=None,
                        type=int)
    parser.add_argument('--scale', help='Scaling factor',
                        default=1,
                        type=float)
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


def main(args=sys.argv[1:]):
    args = parse(args)
    qr = segno.make(args.content, error=args.error, version=args.version,
                    mask=args.mask, micro=args.micro)
    if args.output is None:
        qr.terminal(border=args.border)
    else:
        config = dict(scale=args.scale, border=args.border)
        if args.color is not None:
            config['color'] = args.color if args.color not in ('trans', 'transparent') else None
        if args.background is not None:
            config['background'] = args.background if args.background not in ('trans', 'transparent') else None
        if int(args.scale) == args.scale:
            config['scale'] = int(args.scale)
        fname = args.output
        ext = fname[fname.rfind('.') + 1:].lower()
        if ext == 'svgz':  # There is no svgz serializer, use same config as svg
            ext = 'svg'
        supported_args = _EXT_TO_KW_MAPPING.get(ext, ())
        # Drop unsupported arguments from config
        for k in list(config):
            if k not in supported_args:
                del config[k]
        qr.save(fname, **config)


if __name__ == '__main__':
    main()
