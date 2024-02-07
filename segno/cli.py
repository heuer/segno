#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
# type: ignore
"""\
Command line script to generate (Micro) QR codes with Segno.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.
"""
import os
import sys
import argparse
import segno
from segno import writers

# file extension to supported keywords mapping
_EXT_TO_KW_MAPPING = {}


def _get_args(func):
    func_code = func.__code__
    args = func_code.co_varnames[:func_code.co_argcount]
    return args[-len(func.__defaults__):]


for ext, func in writers._VALID_SERIALIZERS.items():
    kws = set(_get_args(func))
    try:
        kws.update(_get_args(func.__wrapped__))
    except AttributeError:
        pass
    _EXT_TO_KW_MAPPING[ext] = frozenset(kws)

del writers


def make_parser():
    """\
    Returns the command line parser.
    """

    def _convert_scale(val):
        val = float(val)
        return val if val != int(val) else int(val)

    parser = argparse.ArgumentParser(prog='segno',
                                     description='Segno QR Code and Micro QR Code generator version {0}'
                                     .format(segno.__version__))
    parser.add_argument('--version', '-v', help='(Micro) QR Code version: 1 .. 40 or "M1", "M2", "M3", "M4"',
                        required=False,)
    parser.add_argument('--error', '-e', help='Error correction level: "L": 7%% (default), "M": 15%%, "Q": 25%%, '
                                              '"H": 30%%, "-": no error correction (used for M1 symbols)',
                        choices=('L', 'M', 'Q', 'H', '-'),
                        default=None,
                        type=lambda x: x.upper())
    parser.add_argument('--mode', '-m', help='Mode. If unspecified (default), an optimal mode is chosen for the given '
                                             'input.',
                        choices=('numeric', 'alphanumeric', 'byte', 'kanji', 'hanzi'),
                        default=None,
                        type=lambda x: x.lower())
    parser.add_argument('--encoding', help='Sets the encoding of the input. '
                                           'If not set (default), a minimal encoding is chosen.',
                        default=None)
    parser.add_argument('--micro', help='Allow the creation of Micro QR Codes',
                        dest='micro', action='store_true')
    parser.add_argument('--no-micro', help='Disallow creation of Micro QR Codes (default)',
                        dest='micro', action='store_false')
    parser.add_argument('--pattern', '-p', help='Mask pattern to use. '
                                                'If unspecified (default), an optimal mask pattern is used. '
                                                'Valid values for QR Codes: 0 .. 7. '
                                                'Valid values for Micro QR Codes: 0 .. 3',
                        required=False,
                        default=None,
                        type=int)
    parser.add_argument('--no-error-boost', help='Disables the automatic error correction level incrementation. '
                                                 'By default, the maximal error correction level is used '
                                                 '(without changing the version).',
                        dest='boost_error', action='store_false')
    parser.add_argument('--seq', help='Creates a sequence of QR Codes (Structured Append mode). '
                                      'Version or symbol count must be provided',
                        dest='seq', action='store_true')
    parser.add_argument('--symbol-count', '-sc', help='Number of symbols to create',
                        default=None,
                        type=int)
    parser.add_argument('--border', '-b', help='Size of the border / quiet zone of the output. '
                                               'By default, the standard border (4 modules for QR Codes, '
                                               '2 modules for Micro QR Codes) will be used. '
                                               'A value of 0 omits the border',
                        default=None,
                        type=int)
    parser.add_argument('--scale', '-s', help='Scaling factor. By default, a scaling factor of 1 is used. '
                                              'That may lead into too small images. '
                                              'Some output formats, i.e. SVG, accept a decimal value.',
                        default=1,
                        type=_convert_scale)
    parser.add_argument('--output', '-o', help='Output file. If not specified, the QR Code is printed to the terminal',
                        required=False)

    color_group = parser.add_argument_group('Module Colors', 'Arguments to specify the module colors. '
                                                             'Multiple colors are supported for SVG and PNG. '
                                                             'The module color support varies between the '
                                                             'serialization formats. '
                                                             'Most serializers support at least "--dark" and "--light". '  # noqa: E501
                                                             'Unsupported arguments are ignored.')
    color_group.add_argument('--dark', help='Color of the dark modules. '
                                            'The color may be specified as web color name, i.e. "red" or '
                                            'as hexadecimal value, i.e. "#0033cc". '
                                            'Some serializers, i.e. SVG and PNG, support alpha channels '
                                            '(8-digit hexadecimal value) and some support "transparent" / "trans" as '
                                            'color value for alpha transparency. '
                                            'The standard color is black.')
    color_group.add_argument('--light', help='Color of the light modules. '
                                             'See "dark" for a description of possible values. '
                                             'The standard light color is white.')
    color_group.add_argument('--finder-dark', help='Sets the color of the dark finder modules')
    color_group.add_argument('--finder-light', help='Sets the color of the light finder modules')
    color_group.add_argument('--separator', help='Sets the color of the separator modules')
    color_group.add_argument('--data-dark', help='Sets the color of the dark data modules')
    color_group.add_argument('--data-light', help='Sets the color of the light data modules')
    color_group.add_argument('--timing-dark', help='Sets the color of the dark timing modules')
    color_group.add_argument('--timing-light', help='Sets the color of the light timing modules')
    color_group.add_argument('--align-dark', help='Sets the color of the dark alignment modules',
                             dest='alignment_dark', )
    color_group.add_argument('--align-light', help='Sets the color of the light alignment modules',
                             dest='alignment_light', )
    color_group.add_argument('--quiet-zone', help='Sets the color of the quiet zone (border)')
    color_group.add_argument('--dark-module', help='Sets the color of the dark module')
    color_group.add_argument('--format-dark', help='Sets the color of the dark format information modules')
    color_group.add_argument('--format-light', help='Sets the color of the light format information modules')
    color_group.add_argument('--version-dark', help='Sets the color of the dark version information modules')
    color_group.add_argument('--version-light', help='Sets the color of the light version information modules')

    # SVG
    svg_group = parser.add_argument_group('SVG', 'SVG specific options')
    svg_group.add_argument('--no-classes', help='Omits the (default) SVG classes',
                           action='store_true')
    svg_group.add_argument('--no-xmldecl', help='Omits the XML declaration header',
                           dest='xmldecl',
                           action='store_false')
    svg_group.add_argument('--no-namespace', help='Indicates that the SVG document should have no SVG namespace '
                                                  'declaration',
                           dest='svgns',
                           action='store_false')
    svg_group.add_argument('--no-newline', help='Indicates that the SVG document should have no trailing newline',
                           dest='nl',
                           action='store_false')
    svg_group.add_argument('--title', help='Specifies the title of the SVG document')
    svg_group.add_argument('--desc', help='Specifies the description of the SVG document')
    svg_group.add_argument('--svgid', help='Indicates the ID of the <svg/> element')
    svg_group.add_argument('--svgclass', help='Indicates the CSS class of the <svg/> element. '
                                              'An empty string omits the attribute.')
    svg_group.add_argument('--lineclass', help='Indicates the CSS class of the <path/> elements. '
                                               'An empty string omits the attribute.')
    svg_group.add_argument('--no-size', help='Indicates that the SVG document should not have "width" and "height" '
                                             'attributes',
                           dest='omitsize',
                           action='store_true')
    svg_group.add_argument('--unit', help='Indicates SVG coordinate system unit')
    svg_group.add_argument('--svgversion', help='Indicates the SVG version',
                           type=float)
    svg_group.add_argument('--svgencoding', help='Specifies the encoding of the document',
                           default='utf-8')
    svg_group.add_argument('--draw-transparent', help='Indicates that transparent paths should be drawn',
                           action='store_true')
    # PNG
    png_group = parser.add_argument_group('PNG', 'PNG specific options')
    png_group.add_argument('--dpi', help='Sets the DPI value of the PNG file',
                           type=int)
    # Terminal
    terminal_group = parser.add_argument_group('Terminal', 'Terminal specific options')
    terminal_group.add_argument('--compact', help='Indicates that the QR code should be printed in a more compact manner',   # noqa: E501
                                action='store_true')
    # Show Segno's version --version and -v are taken by QR Code version
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
    Builds a configuration and returns it.

    The config contains only keywords which are supported by the serializer.
    Unsupported values are removed.

    :param dict config: The configuration / dict returned by the :py:func:`parse` function.
    :param filename: Optional filename. If not ``None`` (default), the `filename`
                     must provide a supported extension to identify the serializer.
    :return: A (maybe) modified configuration.
    """
    # Done here since it seems not to be possible to detect if an argument
    # was supplied by the user or if it's the default argument.
    # If using type=lambda v: None if v in ('transparent', 'trans') else v
    # we cannot detect if "None" comes from "transparent" or the default value
    for clr in ('dark', 'light', 'finder_dark', 'finder_light',
                'format_dark', 'format_light', 'alignment_dark', 'alignment_light',
                'timing_dark', 'timing_light', 'data_dark', 'data_light',
                'version_dark', 'version_light',
                'quiet_zone', 'dark_module', 'separator'):
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
    # encoding is used to provide the encoding to *create* a QR code
    config['encoding'] = config.pop('svgencoding', 'utf-8')
    if filename is not None:
        ext = filename[filename.rfind('.') + 1:].lower()
        if ext == 'svgz':  # There is no svgz serializer, use same config as svg
            ext = 'svg'
        supported_args = _EXT_TO_KW_MAPPING.get(ext, ())
        # Drop unsupported arguments from config rather than getting a
        # "unsupported keyword" exception
        config = {k: config[k] for k in config if k in supported_args}
    return config


def make_code(config):
    """\
    Creates the (Micro) QR Code (Sequence).

    Configuration parameters used for creating the Micro QR Code, QR Code
    or QR Code Sequence are removed from the configuration.

    :param config: Configuration, see :py:func:`build_config`
    :return: :py:class:`segno.QRCode` or :py:class:`segno.QRCodeSequence`.
    """
    make = segno.make
    kw = dict(mode=config.pop('mode'), error=config.pop('error'),
              version=config.pop('version'), mask=config.pop('pattern'),
              encoding=config.pop('encoding'),
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
    except ValueError as ex:
        sys.stderr.writelines([str(ex), os.linesep])
        return sys.exit(1)
    output = config.pop('output')
    if output is None:
        qr.terminal(border=config['border'], compact=config.get('compact', False))
    else:
        qr.save(output, **build_config(config, filename=output))
    return 0


class _AttrDict(dict):
    """\
    Internal helper class.
    """
    def __init__(self, *args, **kwargs):
        super(_AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


if __name__ == '__main__':
    main()
