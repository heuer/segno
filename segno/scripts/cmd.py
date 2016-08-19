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


def parse(args):
    """\
    Creates the parser.

    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Segno QR Code and Micro QR Code generator')
    parser.add_argument('content', nargs='?', default='')
    parser.add_argument('--version', '-v', help='(Micro) QR Code version',
                        required=False,)
    parser.add_argument('--error', '-e', help='Error correction level: "L": 7%, "M": 15% (default), "Q": 25%, "H": 30%, "-": no error correction (used for M1 symbols)',
                        required=False,
                        choices=('L', 'M', 'Q', 'H', '-'),
                        default=None,
                        type=lambda x: x.upper())
    parser.add_argument('--mask', '-m', help='Mask',
                        required=False,
                        default=None,
                        type=int)
    parser.add_argument('--scale', help='Scaling factor',
                        default=1,
                        type=float)
    parser.add_argument('--border', '-b', help='Border / quiet zone',
                        default=None,
                        type=int)
    parser.add_argument('--micro', dest='micro', action='store_true')
    parser.add_argument('--no-micro', dest='micro', action='store_false')
    parser.add_argument('--output', '-o', help='Output file',
                        required=False,
                        )
    parsed_args = parser.parse_args(args)
    if parsed_args.content == '':
        parsed_args.content = None
    if parsed_args.error == '-':
        parsed_args.error = None
    return parsed_args


def main(args):
    args = parse(args)
    qr = segno.make(args.content,
                    error=(args.error if args.error != '-' else None),
                    version=args.version, mask=args.mask, micro=args.micro)
    if args.output is None:
        qr.terminal()
    else:
        qr.save(args.output)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
