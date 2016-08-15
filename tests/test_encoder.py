# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the encoder module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import os
import io
from nose.tools import eq_, ok_, raises, nottest
from segno import consts
from segno import encoder
from segno.encoder import Buffer


def bits(s):
    return bytearray([int(x, 2) for x in s if x != ' '])


def check_prepare_data(expected, data, mode, encoding):
    eq_(expected, tuple(encoder.prepare_data(data, mode, encoding)))


def read_matrix(name):
    """\
    Helper function to read a matrix from /ref_matrix. The file extension .txt
    is added automatically.

    :return: A tuple of bytearrays
    """
    matrix = []
    with io.open(os.path.join(os.path.dirname(__file__), 'ref_matrix/{0}.txt'.format(name)), 'rt') as f:
        for row in f:
            matrix.append(bytearray([int(i) for i in row if i != '\n']))
    return tuple(matrix)


def read_ref_matrix(name):
    """\
    Helper function to read a matrix from /ref. The file extension .txt
    is added automatically.

    :return: A tuple of bytearrays
    """
    matrix = []
    with io.open(os.path.join(os.path.dirname(__file__), 'ref/{0}.txt'.format(name)), 'rt') as f:
        for row in f:
            matrix.append(bytearray([int(i) for i in row if i != '\n']))
    return tuple(matrix)


def test_version_as_str():
    qr = encoder.encode('test', version='1', error=None, mode=None, mask=None, eci=None, micro=None, encoding=None)
    eq_(1, qr.version)


def test_prepare_data_numeric():
    test_data = (
        '1234567',
        '666',
    )
    for data in test_data:
        for mode in (None, consts.MODE_NUMERIC):
            expected = ((data.encode('ascii'), len(data), consts.MODE_NUMERIC, None),)
            yield check_prepare_data, expected, data, mode, None


def test_prepare_data_override_numeric():
    test_data = (
        '1234567',
        '666',
    )
    for data in test_data:
        for mode in (None, consts.MODE_NUMERIC, consts.MODE_ALPHANUMERIC,
                     consts.MODE_BYTE):
            encoding = None if mode != consts.MODE_BYTE else consts.DEFAULT_BYTE_ENCODING
            expected = ((data.encode('ascii'), len(data), mode or consts.MODE_NUMERIC, encoding),)
            yield check_prepare_data, expected, data, mode, None


def test_prepare_data_alphanumeric():
    test_data = (
        'HELLO WORLD',
        'ABCDEF',
        'HELLO    WORLD ',
        '-123',
    )
    for data in test_data:
        for mode in (None, consts.MODE_ALPHANUMERIC):
            expected = ((data.encode('ascii'), len(data), consts.MODE_ALPHANUMERIC, None),)
            yield check_prepare_data, expected, data, mode, None


def test_prepare_data_override_alphanumeric():
    test_data = (
        'HELLO WORLD',
        'ABCDEF',
        'HELLO    WORLD ',
    )
    for data in test_data:
        for mode in (None, consts.MODE_ALPHANUMERIC, consts.MODE_BYTE):
            encoding = None if mode != consts.MODE_BYTE else consts.DEFAULT_BYTE_ENCODING
            expected = ((data.encode('ascii'), len(data), mode or consts.MODE_ALPHANUMERIC, encoding),)
            yield check_prepare_data, expected, data, mode, None


def test_prepare_data_byte():
    test_data = (
        ('HeLLO WORLD', consts.DEFAULT_BYTE_ENCODING),
        ('HELLO\nWORLD', consts.DEFAULT_BYTE_ENCODING),
        ('☺', 'utf-8'),
        ('12345a', consts.DEFAULT_BYTE_ENCODING),
        ('abcdef', consts.DEFAULT_BYTE_ENCODING),
    )
    for data, encoding in test_data:
        for mode in (None, consts.MODE_BYTE):
            for param_encoding in (None, encoding):
                encoded_data = data.encode(encoding)
                expected = ((encoded_data, len(encoded_data), consts.MODE_BYTE, encoding),)
                yield check_prepare_data, expected, data, mode, param_encoding


def test_prepare_data_multiple():
    test_data = ['a', '1']
    segments = encoder.prepare_data(test_data, None, None)
    eq_(2, segments.data_length)
    eq_((b'a', 1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING), segments[0])
    eq_((b'1', 1, consts.MODE_NUMERIC, None), segments[1])


def test_prepare_data_multiple2():
    test_data = ['a']
    segments = encoder.prepare_data(test_data, None, None)
    eq_(1, segments.data_length)
    eq_((b'a', 1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING), segments[0])


def test_prepare_data_multiple_int():
    test_data = [1]
    segments = encoder.prepare_data(test_data, None, None)
    eq_(1, segments.data_length)
    eq_((b'1', 1, consts.MODE_NUMERIC, None), segments[0])


def test_prepare_data_multiple_override():
    test_data = [(1, consts.MODE_ALPHANUMERIC), 2]
    segments = encoder.prepare_data(test_data, None, None)
    eq_(2, segments.data_length)
    eq_((b'1', 1, consts.MODE_ALPHANUMERIC, None), segments[0])
    eq_((b'2', 1, consts.MODE_NUMERIC, None), segments[1])


def test_prepare_data_multiple_mode_none():
    test_data = [(1, None), ('A', None)]
    segments = encoder.prepare_data(test_data, None, None)
    eq_(2, segments.data_length)
    eq_((b'1', 1, consts.MODE_NUMERIC, None), segments[0])
    eq_((b'A', 1, consts.MODE_ALPHANUMERIC, None), segments[1])


def test_prepare_data_multiple_mode_none_ignore_encoding():
    test_data = [(1, None, consts.DEFAULT_BYTE_ENCODING), ('A', None, 'utf-8')]
    segments = encoder.prepare_data(test_data, None, None)
    eq_(2, segments.data_length)
    eq_((b'1', 1, consts.MODE_NUMERIC, None), segments[0])
    eq_((b'A', 1, consts.MODE_ALPHANUMERIC, None), segments[1])


def test_prepare_data_multiple_mode_none_encoding():
    test_data = [('Ä', None, consts.DEFAULT_BYTE_ENCODING), ('Ä', None, 'utf-8'),
                 ('Ä', None, None)]
    segments = encoder.prepare_data(test_data, None, None)
    eq_(4, segments.data_length)  # 1 byte latin1 + 2 bytes UTF-8 + 1 byte latin1
    eq_(('Ä'.encode(consts.DEFAULT_BYTE_ENCODING), 1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING), segments[0])
    eq_(('Ä'.encode('utf-8'), 2, consts.MODE_BYTE, 'utf-8'), segments[1])
    eq_(segments[0], segments[2])  # Encoding detection should produce the same result as 1st tuple


def test_prepare_data_multiple_tuple():
    test_data = ('a', '1')
    segments = encoder.prepare_data(test_data, None, None)
    eq_(2, segments.data_length)
    eq_((b'a', 1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING), segments[0])
    eq_((b'1', 1, consts.MODE_NUMERIC, None), segments[1])


def test_write_segment_eci_standard_value():
    # See ISO/IEC 18004:2006(E) -- 6.4.2.1 ECI Designator - EXAMPLE (page 24)
    encoding = 'ISO-8859-7'
    #TODO: ?
    # NOTE: ISO/IEC 18004:2006(E) uses "ΑΒΓΔΕ" but text says:
    # (character values A1HEX, A2HEX, A3HEX, A4HEX, A5HEX) and result seems
    # to use the A...HEX values as well
    s = '\u2018\u2019\u00A3\u20AC\u20AF'.encode(encoding)
    seg = encoder.Segment(s, len(s), consts.MODE_BYTE, encoding)
    buff = Buffer()
    v, vrange = None, consts.VERSION_RANGE_01_09
    encoder.write_segment(buff, seg, v, vrange, True)
    expected = bits('0111 00001001 0100 00000101 10100001 10100010 10100011 10100100 10100101')
    result = buff.getbits()
    eq_(len(expected), len(result))
    eq_(expected, result)


def test_write_segment_numeric_standard_value_example1():
    # See ISO/IEC 18004:2006(E) -- 6.4.3 Numeric mode - EXAMPLE 1 (page 25)
    def check(eci):
        s = b'01234567'
        seg = encoder.Segment(s, len(s), consts.MODE_NUMERIC, None)
        buff = Buffer()
        v, vrange = None, consts.VERSION_RANGE_01_09
        encoder.write_segment(buff, seg, v, vrange, eci=eci)
        eq_(bits('00010000001000000000110001010110011000011'), buff.getbits())
    for eci in (True, False):
        yield check, eci


def test_write_segment_numeric_standard_value_example2():
    # See ISO/IEC 18004:2006(E) -- 6.4.3 Numeric mode - EXAMPLE 2 (page 25)
    def check(eci):
        s = b'0123456789012345'
        seg = encoder.Segment(s, len(s), consts.MODE_NUMERIC, None)
        buff = Buffer()
        v, vrange = consts.VERSION_M3, consts.VERSION_M3
        encoder.write_segment(buff, seg, v, vrange, eci=eci)
        eq_(bits('0010000000000110001010110011010100110111000010100111010100101'),
            buff.getbits())
    for eci in (True, False):
        yield check, eci


def test_write_segment_numeric_standard_value_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    def check(eci):
        s = b'01234567'
        seg = encoder.Segment(s, len(s), consts.MODE_NUMERIC, None)
        buff = Buffer()
        v, vrange = consts.VERSION_M2, consts.VERSION_M2
        encoder.write_segment(buff, seg, v, vrange, eci=eci)
        eq_(bits('01000000000110001010110011000011'), buff.getbits())
    for eci in (True, False):
        yield check, eci


def test_write_segment_alphanumeric_standard_value_example():
    # See ISO/IEC 18004:2006(E) -- 6.4.3 Numeric mode - EXAMPLE (page 26)
    def check(eci):
        s = b'AC-42'
        seg = encoder.Segment(s, len(s), consts.MODE_ALPHANUMERIC, None)
        buff = Buffer()
        v, vrange = None, consts.VERSION_RANGE_01_09
        encoder.write_segment(buff, seg, v, vrange, eci=eci)
        eq_(bits('00100000001010011100111011100111001000010'), buff.getbits())
    for eci in (True, False):
        yield check, eci


def test_write_segment_alphanumeric_thonky():
    # <http://www.thonky.com/qr-code-tutorial/data-encoding/#step-3-encode-using-the-selected-mode>
    def check(eci):
        s = b'HELLO WORLD'
        seg = encoder.Segment(s, len(s), consts.MODE_ALPHANUMERIC, None)
        buff = Buffer()
        v, vrange = None, consts.VERSION_RANGE_01_09
        encoder.write_segment(buff, seg, v, vrange, eci)
        eq_(bits('00100000010110110000101101111000110100010111001011011100010011010100001101'),
            buff.getbits())
    for eci in (True, False):
        yield check, eci


def test_write_segment_bytes_thonky():
    # <http://www.thonky.com/qr-code-tutorial/byte-mode-encoding/>
    def check(eci):
        s = b'Hello, world!'
        seg = encoder.Segment(s, len(s), consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING)
        buff = Buffer()
        v, vrange = None, consts.VERSION_RANGE_01_09
        encoder.write_segment(buff, seg, v, vrange, eci=eci)
        eq_(bits('010000001101'
                 '01001000'
                 '01100101'
                 '01101100'
                 '01101100'
                 '01101111'
                 '00101100'
                 '00100000'
                 '01110111'
                 '01101111'
                 '01110010'
                 '01101100'
                 '01100100'
                 '00100001'), buff.getbits())
    for eci in (True, False):
        yield check, eci


def test_write_terminator_thonky():
    # <http://www.thonky.com/qr-code-tutorial/data-encoding/#add-a-terminator-of-0s-if-necessary>
    data = bits('00100000010110110000101101111000110100010111001011011100010011010100001101')
    buff = Buffer(data)
    version = 1
    v = None
    capacity = consts.SYMBOL_CAPACITY[version][consts.ERROR_LEVEL_Q][0]
    encoder.write_terminator(buff, capacity, v, len(data))
    eq_(data + bits('0000'), buff.getbits())


def test_write_terminator_standard_value_i2():
    # See ISO/IEC 18004:2006(E) -- I.2 Encoding a QR Code symbol (page 94)
    data = bits('000100000010000000001100010101100110000110000')
    buff = Buffer(data)
    version = 1
    v = None
    capacity = consts.SYMBOL_CAPACITY[version][consts.ERROR_LEVEL_M][0]
    encoder.write_terminator(buff, capacity, v, len(data))
    eq_(data + bits('0000'), buff.getbits())


def test_write_terminator_standard_value_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    data = bits('01000000000110001010110011000011')
    buff = Buffer(data)
    version = consts.VERSION_M2
    capacity = consts.SYMBOL_CAPACITY[version][consts.ERROR_LEVEL_L][0]
    encoder.write_terminator(buff, capacity, version, len(data))
    eq_(data + bits('00000'), buff.getbits())


def test_write_padding_bits_iso_i2():
    # See ISO/IEC 18004:2006(E) -- I.2 Encoding a QR Code symbol (page 94)
    data = bits('0001 0000001000 0000001100 0101011001 1000011 0000')
    buff = Buffer(data)
    encoder.write_padding_bits(buff, len(buff))
    eq_(bits('00010000 00100000 00001100 01010110 01100001 10000000'), buff.getbits())


def test_write_padding_bits_iso_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    data = bits('0 1000 0000001100 0101011001 1000011 00000')
    buff = Buffer(data)
    encoder.write_padding_bits(buff, len(buff))
    eq_(bits('01000000 00011000 10101100 11000011 00000000'), buff.getbits())


def test_write_padding_bits_thonky():
    # <http://www.thonky.com/qr-code-tutorial/data-encoding>
    data = bits('00100000 01011011 00001011 01111000 11010001 01110010 11011100 01001101 01000011 010000')
    buff = Buffer(data)
    encoder.write_padding_bits(buff, len(buff))
    eq_(bits('00100000 01011011 00001011 01111000 11010001 01110010 11011100 01001101 01000011 01000000'), buff.getbits())


def test_write_pad_codewords_standard_value_i2():
    # See ISO/IEC 18004:2006(E) -- I.2 Encoding a QR Code symbol (page 94)
    data = bits('00010000 00100000 00001100 01010110 01100001 10000000')
    buff = Buffer(data)
    version = 1
    error = consts.ERROR_LEVEL_M
    capacity = consts.SYMBOL_CAPACITY[version][error][0]
    encoder.write_pad_codewords(buff, version, capacity, len(buff))
    eq_(data + bits('11101100000100011110110000010001111011000001000111101100000100011110110000010001'), buff.getbits())


def test_write_pad_codewords_standard_value_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    data = bits('0100000000011000101011001100001100000000')
    buff = Buffer(data)
    version = consts.VERSION_M2
    error = consts.ERROR_LEVEL_L
    capacity = consts.SYMBOL_CAPACITY[version][error][0]
    encoder.write_pad_codewords(buff, version, capacity, len(buff))
    eq_(data, buff.getbits())


def test_is_alphanumeric():
    def check(data):
        ok_(encoder.is_alphanumeric(data))
    valid = (b'ABCDEF', b'A', b'A1', b'1A', b'HTTP://WWW.EXAMPLE.ORG',
             b'666', b' ', b'HELLO WORLD', b'AC-42',
             consts.ALPHANUMERIC_CHARS)
    for data in valid:
        yield check, data


def test_is_not_alphanumeric():
    def check(data):
        ok_(not encoder.is_alphanumeric(data))
    invalid = (b'a', b'0123b', b'_', b'http://www.example.org/',  b'',
               'ü'.encode('utf-8'), 'Ü'.encode('utf-8'),
               'ä'.encode(consts.DEFAULT_BYTE_ENCODING), b'HELLO\nWORLD', b'Ab')
    for data in invalid:
        yield check, data


def test_is_kanji():
    def check(data):
        ok_(encoder.is_kanji(data.encode('shift_jis')))
    valid = ('点', '漢字', '外来語', 'あめかんむり', 'ひへん', 'くさかんむり')
    for data in valid:
        yield check, data


def test_is_not_kanji():
    def check(data):
        ok_(not encoder.is_kanji(data.encode('shift_jis')))
    invalid = ('abcdef', '1234', '1234a', 'ABCDEF')
    for data in invalid:
        yield check, data


def test_find_mode():
    def check(data, expected):
        eq_(expected, encoder.find_mode(data))
    data = (
        (b'123', consts.MODE_NUMERIC),
        (b'-123', consts.MODE_ALPHANUMERIC),
        (b'123a', consts.MODE_BYTE),
        (b'123A', consts.MODE_ALPHANUMERIC),
        (b'HELLO WORLD', consts.MODE_ALPHANUMERIC),
        (b'HELLO \n WORLD', consts.MODE_BYTE),
        (b'HTTP://WWW.EXAMPLE.ORG/', consts.MODE_ALPHANUMERIC),
        (b'http://www.example.org/', consts.MODE_BYTE),
        (b'#', consts.MODE_BYTE),
        (b'', consts.MODE_BYTE),
        (b'a', consts.MODE_BYTE),
        ('点'.encode('shift_jis'), consts.MODE_KANJI),
        ('茗'.encode('shift_jis'), consts.MODE_KANJI),
        ('漢字'.encode('shift_jis'), consts.MODE_KANJI),
        ('外来語'.encode('shift_jis'), consts.MODE_KANJI),
        ('外来語'.encode('utf-8'), consts.MODE_BYTE),
    )
    for d, mode in data:
        yield check, d, mode


def test_get_matrix_size():
    def check(version, expected):
        try:
            v = consts.MICRO_VERSION_MAPPING[version]
        except KeyError:
            v = version
        eq_(expected, encoder.calc_matrix_size(v))
    data = (
        # Version, matrix size
        ('M1', 11),
        ('M2', 13),
        ('M3', 15),
        ('M4', 17),
        (1, 21),
        (27, 125),
        (40, 177),
    )
    for version, size in data:
        yield check, version, size


def test_is_mode_supported():
    def check(mode, version, expected):
        try:
            v = consts.MICRO_VERSION_MAPPING[version]
        except KeyError:
            v = version
        eq_(expected, encoder.is_mode_supported(mode, v))
    # See ISO/IEC 18004:2006(E) - Table 2 (page 22)
    data = (
        (consts.MODE_NUMERIC, 'M1', True),
        (consts.MODE_NUMERIC, 'M2', True),
        (consts.MODE_NUMERIC, 'M3', True),
        (consts.MODE_NUMERIC, 'M4', True),
        (consts.MODE_ALPHANUMERIC, 'M1', False),
        (consts.MODE_ALPHANUMERIC, 'M2', True),
        (consts.MODE_ALPHANUMERIC, 'M3', True),
        (consts.MODE_ALPHANUMERIC, 'M4', True),
        (consts.MODE_ECI, 'M1', False),
        (consts.MODE_ECI, 'M2', False),
        (consts.MODE_ECI, 'M3', False),
        (consts.MODE_ECI, 'M4', False),
        (consts.MODE_BYTE, 'M1', False),
        (consts.MODE_BYTE, 'M2', False),
        (consts.MODE_BYTE, 'M3', True),
        (consts.MODE_BYTE, 'M4', True),
        (consts.MODE_KANJI, 'M3', True),
        (consts.MODE_KANJI, 'M4', True),
    )
    for v in range(1, 41):
        for mode in (consts.MODE_NUMERIC, consts.MODE_ALPHANUMERIC,
                     consts.MODE_BYTE, consts.MODE_ECI, consts.MODE_KANJI):
            yield check, mode, v, True
    for mode, version, expected in data:
        yield check, mode, version, expected


def test_is_mode_supported_invalid_mode():
    @raises(encoder.ModeError)
    def check(mode, version):
        encoder.is_mode_supported(mode, version)
    data = (
        (-1, 1),
        (-2, consts.VERSION_M2),
        (10, 1),
        (10, consts.VERSION_M1),
        (9, 39),
    )
    for mode, version in data:
        yield check, mode, version


def test_normalize_mode_illegal():
    @raises(encoder.ModeError)
    def check(mode):
        encoder.normalize_mode(mode)
    data = ('kanij', 'binary', 'blub', '')
    for mode in data:
        yield check, mode


def test_normalize_mask():
    micro = range(4)
    usual = range(8)

    def check(version, mask):
        eq_(mask, encoder.normalize_mask(mask, version < 1))

    for mask in usual:
        for version in range(1, 41):
            yield check, version, mask

    for mask in micro:
        for version in range(consts.VERSION_M1, 1):
            yield check, version, mask


def test_normalize_mask_none():
    ok_(encoder.normalize_mask(None, is_micro=True) is None)
    ok_(encoder.normalize_mask(None, is_micro=False) is None)


def test_normalize_mask_illegal():
    @raises(encoder.MaskError)
    def check(version, mask):
        encoder.normalize_mask(mask, version < 1)

    for version, mask in ((consts.VERSION_M1, 8), (1, 9), (1, -1)):
        yield check, version, mask


@raises(encoder.ModeError)
def test_mode_name_illegal():
    encoder.get_mode_name(7)


@raises(encoder.ErrorLevelError)
def test_error_name_illegal():
    encoder.get_error_name(7)


@raises(encoder.VersionError)
def test_version_name_illegal():
    encoder.get_version_name(41)


@raises(encoder.VersionError)
def test_version_range_illegal():
    encoder.version_range(41)


def test_normalize_errorlevel():
    eq_(consts.ERROR_LEVEL_H, encoder.normalize_errorlevel('h'))
    eq_(consts.ERROR_LEVEL_Q, encoder.normalize_errorlevel('Q'))
    eq_(None, encoder.normalize_errorlevel(None, accept_none=True))
    eq_(consts.ERROR_LEVEL_M, encoder.normalize_errorlevel(consts.ERROR_LEVEL_M))


@raises(encoder.ErrorLevelError)
def test_normalize_errorlevel_illegal():
    encoder.normalize_errorlevel('g')


@raises(encoder.ErrorLevelError)
def test_normalize_errorlevel_illegal2():
    encoder.normalize_errorlevel(None)


def test_find_version():
    def check(data, error, micro, expected_version):
        segments = encoder.prepare_data(data, None, None)
        eq_(expected_version, encoder.find_version(segments, error, micro))

    test_data = (
        # data, error, micro, expected version
        ('12345', None, True, consts.VERSION_M1),
        ('12345', consts.ERROR_LEVEL_M, True, consts.VERSION_M2),
        # Error level Q isn't suppoted by M1 - M3
        ('12345', consts.ERROR_LEVEL_Q, True, consts.VERSION_M4),
        # Error level H isn't supported by Micro QR Codes
        ('12345', consts.ERROR_LEVEL_H, None, 1),
        ('12345', None, False, 1),
        (12345, None, True, consts.VERSION_M1),
        (-12345, None, True, consts.VERSION_M3),  # Negative number
        (12345, None, False, 1),
        ('123456', None, True, consts.VERSION_M2),
        ('123456', None, False, 1),
        (123456, None, True, consts.VERSION_M2),
        (123456, None, False, 1),
        ('ABCDE', None, True, consts.VERSION_M2),  # Alphanumeric isn't supported by M1
        ('ABCDEF', consts.ERROR_LEVEL_L, True, consts.VERSION_M2),
        ('ABCDEF', consts.ERROR_LEVEL_M, True, consts.VERSION_M3),  # Too much data for error level M and version M2
        ('ABCDEF', consts.ERROR_LEVEL_L, False, 1),
        ('ABCDEF', consts.ERROR_LEVEL_M, False, 1),
        ('Märchenbuch', None, True, consts.VERSION_M4),
        ('Märchenbücher', None, False, 1),
        ('Märchenbücherei', None, None, 2),
    )
    for data, error, micro, expected_version in test_data:
        yield check, data, error, micro, expected_version


def test_thonky_add_format_info():
    # <http://www.thonky.com/qr-code-tutorial/format-version-information#put-the-format-string-into-the-qr-code>
    version = 1
    matrix = encoder.make_matrix(version, reserve_regions=False)
    encoder.add_finder_patterns(matrix, is_micro=False)
    encoder.add_format_info(matrix, version, consts.ERROR_LEVEL_L, 4)
    ref_matrix = read_matrix('thonky_format')
    eq_(ref_matrix, matrix)


def test_thonky_add_version_info():
    # <http://www.thonky.com/qr-code-tutorial/format-version-information>
    version = 7
    matrix = encoder.make_matrix(version, reserve_regions=False)
    encoder.add_finder_patterns(matrix, is_micro=False)
    encoder.add_alignment_patterns(matrix, version)
    encoder.add_version_info(matrix, version)
    matrix[-8][8] = 0x1  # dark module
    ref_matrix = read_matrix('thonky_version')
    eq_(ref_matrix, matrix)


def test_eval_micro():
    # ISO/IEC 18004:2006(E) page 54
    # 6.8.2.2 Evaluation of Micro QR Code symbols
    matrix = read_matrix('iso_6.8.2.2')
    res = encoder.evaluate_micro_mask(matrix, len(matrix))
    eq_(104, res)


def make_thonky_score_matrix():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking-1')
    return matrix, len(matrix)


def test_score_n1():
    matrix, matrix_size = make_thonky_score_matrix()
    score = encoder.score_n1(matrix, matrix_size)
    eq_(180, score)


def test_score_n2():
    matrix, matrix_size = make_thonky_score_matrix()
    score = encoder.score_n2(matrix, matrix_size)
    eq_(90, score)


def test_score_n3():
    matrix, matrix_size = make_thonky_score_matrix()
    score = encoder.score_n3(matrix, matrix_size)
    # Thonky: 80
    eq_(760, score)


def test_score_n4():
    matrix = read_matrix('thonky_datamasking-2')
    score = encoder.score_n4(matrix, len(matrix))
    eq_(0, score)


def test_thonky_pattern_0():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-0')
    matrix_size = len(matrix)
    eq_(180, encoder.score_n1(matrix, matrix_size))
    eq_(90, encoder.score_n2(matrix, matrix_size))
    # Thonky: 80
    eq_(760, encoder.score_n3(matrix, matrix_size))
    eq_(0, encoder.score_n4(matrix, matrix_size))
    # See score 3
    eq_(350 - 80 + 760, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_1():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-1')
    matrix_size = len(matrix)
    eq_(172, encoder.score_n1(matrix, matrix_size))
    eq_(129, encoder.score_n2(matrix, matrix_size))
    # Thonky: 120
    eq_(760, encoder.score_n3(matrix, matrix_size))
    eq_(0, encoder.score_n4(matrix, matrix_size))
    # See score 3
    eq_(421 - 120 + 760, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_2():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-2')
    matrix_size = len(matrix)
    eq_(206, encoder.score_n1(matrix, matrix_size))
    eq_(141, encoder.score_n2(matrix, matrix_size))
    # Thonky: 160
    eq_(800, encoder.score_n3(matrix, matrix_size))
    eq_(0, encoder.score_n4(matrix, matrix_size))
    eq_(507 - 160 + 800, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_3():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-3')
    matrix_size = len(matrix)
    eq_(180, encoder.score_n1(matrix, matrix_size))
    eq_(141, encoder.score_n2(matrix, matrix_size))
    # Thonky: 120
    eq_(760, encoder.score_n3(matrix, matrix_size))
    # Thonky: 2, but that's impossible: Either 0 or a multiple of 10 (N4 = 10)
    eq_(0, encoder.score_n4(matrix, matrix_size))
    eq_(443 - 2 - 120 + 760, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_4():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-4')
    matrix_size = len(matrix)
    eq_(195, encoder.score_n1(matrix, matrix_size))
    eq_(138, encoder.score_n2(matrix, matrix_size))
    # Thonky: 200
    eq_(800, encoder.score_n3(matrix, matrix_size))
    eq_(0, encoder.score_n4(matrix, matrix_size))
    # See score 3
    eq_(533 - 200 + 800, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_5():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-5')
    matrix_size = len(matrix)
    eq_(189, encoder.score_n1(matrix, matrix_size))
    eq_(156, encoder.score_n2(matrix, matrix_size))
    # Thonky: 200
    eq_(800, encoder.score_n3(matrix, matrix_size))
    # Thonky: 2, but that's impossible: Either 0 or a multiple of 10 (N4 = 10)
    eq_(0, encoder.score_n4(matrix, matrix_size))
    # See score 3 and 4
    eq_(547 - 2 - 200 + 800, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_6():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-6')
    matrix_size = len(matrix)
    eq_(171, encoder.score_n1(matrix, matrix_size))
    eq_(102, encoder.score_n2(matrix, matrix_size))
    # Thonky: 80
    eq_(840, encoder.score_n3(matrix, matrix_size))
    # Thonky: 4, but that's impossible: Either 0 or a multiple of 10 (N4 = 10)
    eq_(0, encoder.score_n4(matrix, matrix_size))
    # See score 3 and 4
    eq_(357 - 4 - 80 + 840, encoder.evaluate_mask(matrix, matrix_size))


def test_thonky_pattern_7():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix = read_matrix('thonky_datamasking_mask-7')
    matrix_size = len(matrix)
    eq_(197, encoder.score_n1(matrix, matrix_size))
    eq_(123, encoder.score_n2(matrix, matrix_size))
    # Thonky: 200
    eq_(720, encoder.score_n3(matrix, matrix_size))
    eq_(0, encoder.score_n4(matrix, matrix_size))
    # See score 3
    eq_(520 - 200 + 720, encoder.evaluate_mask(matrix, matrix_size))


def test_score_n1_iso():
    # For example, impose 5 penalty points on the block of “dark:dark:dark:dark:dark:dark:dark”
    # module pattern, where a series of seven consecutive modules is counted as one block
    matrix = tuple(bytearray([1] * 7) for i in range(7))
    score = encoder.score_n1(matrix, len(matrix))
    eq_(5 * 7 * 2, score)


def test_score_n2_iso():
    # Take a block consisting of 3 x 3 dark
    # modules for an example. Considering that up to four 2 x 2 dark modules can
    # be included in this block, the penalty applied to this block shall be
    # calculated as 4 (blocks) x 3 (points) = 12 points.
    matrix = (bytearray([1,1,1]), bytearray([1,1,1]), bytearray([1,1,1]))
    score = encoder.score_n2(matrix, len(matrix))
    eq_(12, score)

    matrix = (bytearray([0,0,0]), bytearray([0,0,0]), bytearray([0,0,0]))
    score = encoder.score_n2(matrix, len(matrix))
    eq_(12, score)


def test_score_n4_iso():
    # Add 10 points to a deviation of 5% increment or decrement in the
    # proportion ratio of dark module from the referential 50% (or 0 point)
    # level. For example, assign 0 points as a penalty if the ratio of dark
    # module is between 45% and 55%, or 10 points if the ratio of dark module
    # is between 40% and 60%

    def make_matrix():
        row = [0x0] * 10
        return tuple([bytearray(row) for i in range(10)])

    def fill_matrix(matrix, percent):
        cnt = 0
        finished = False
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                matrix[i][j] = 0x1
                cnt+=1
                finished = cnt == percent
                if finished:
                    break
            if finished:
                break

    def check(score, percent):
        matrix = make_matrix()
        fill_matrix(matrix, percent)
        eq_(score, encoder.score_n4(matrix, len(matrix)))

    for p in range(41, 46):
        yield check, 10, p

    for p in range(55, 60):
        yield check, 10, p

    for p in range(46, 55):
        yield check, 0, p

    yield check, 3 * 10, 35


def test_binary_sequence_to_integers():
    # <http://www.thonky.com/qr-code-tutorial/error-correction-coding>
    # HELLO WORLD as a 1-M code
    data = bits('00100000 01011011 00001011 01111000 11010001 01110010 11011100 01001101 01000011 01000000 11101100 00010001 11101100 00010001 11101100 00010001')
    expected = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    eq_(len(data)/8, len(Buffer(data).toints()))
    eq_(expected, Buffer(data).toints())


def test_split_into_blocks():
    # <http://www.thonky.com/qr-code-tutorial/error-correction-coding>
    # HELLO WORLD as a 5-Q code
    s = '01000011 01010101 01000110 10000110 01010111 00100110 01010101 11000010 01110111 00110010 00000110 00010010 00000110 01100111 00100110 11110110 11110110 01000010 00000111 01110110 10000110 11110010 00000111 00100110 01010110 00010110 11000110 11000111 10010010 00000110 10110110 11100110 11110111 01110111 00110010 00000111 01110110 10000110 01010111 00100110 01010010 00000110 10000110 10010111 00110010 00000111 01000110 11110111 01110110 01010110 11000010 00000110 10010111 00110010 11100000 11101100 00010001 11101100 00010001 11101100 00010001 11101100'
    data = bits(s)
    codewords = Buffer(data).toints()
    eq_(62, len(codewords))
    ec_infos = consts.ECC[5][consts.ERROR_LEVEL_Q]
    ok_(ec_infos)
    eq_(2, len(ec_infos))
    blocks = encoder.make_data_blocks(ec_infos, codewords)
    eq_(4, len(blocks))
    eq_(15, len(blocks[0]))
    eq_(codewords[:15], blocks[0])
    eq_(15, len(blocks[1]))
    eq_(16, len(blocks[2]))
    eq_(16, len(blocks[3]))


def test_make_error_block0():
    # <http://www.thonky.com/qr-code-tutorial/error-correction-coding>
    # 1-M
    data_block = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    error_block = bytearray([196, 35, 39, 119, 235, 215, 231, 226, 93, 23])
    ec_infos = consts.ECC[1][consts.ERROR_LEVEL_M]
    eq_(1, len(ec_infos))
    ec_info = ec_infos[0]
    eq_(1, ec_info.num_blocks)
    eq_(10, ec_info.num_total - ec_info.num_data)
    res = encoder.make_error_block(ec_info, data_block)
    eq_(len(error_block), len(res))
    eq_(error_block, res)


def test_make_error_block1():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    data_block = [67, 85, 70, 134, 87, 38, 85, 194, 119, 50, 6, 18, 6, 103, 38]
    error_block = bytearray([213, 199, 11, 45, 115, 247, 241, 223, 229, 248, 154, 117, 154, 111, 86, 161, 111, 39])
    ec_info = consts.ECC[5][consts.ERROR_LEVEL_Q][0]
    eq_(error_block, encoder.make_error_block(ec_info, data_block))


def test_make_error_block2():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    data_block = [246, 246, 66, 7, 118, 134, 242, 7, 38, 86, 22, 198, 199, 146, 6]
    error_block = bytearray([87, 204, 96, 60, 202, 182, 124, 157, 200, 134, 27, 129, 209, 17, 163, 163, 120, 133])
    ec_info = consts.ECC[5][consts.ERROR_LEVEL_Q][0]
    eq_(error_block, encoder.make_error_block(ec_info, data_block))


def test_make_error_block3():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    data_block = [182, 230, 247, 119, 50, 7, 118, 134, 87, 38, 82, 6, 134, 151, 50, 7]
    error_block = bytearray([148, 116, 177, 212, 76, 133, 75, 242, 238, 76, 195, 230, 189, 10, 108, 240, 192, 141])
    ec_info = consts.ECC[5][consts.ERROR_LEVEL_Q][1]
    eq_(error_block, encoder.make_error_block(ec_info, data_block))


def test_make_error_block4():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    data_block = [70, 247, 118, 86, 194, 6, 151, 50, 16, 236, 17, 236, 17, 236, 17, 236]
    error_block = bytearray([235, 159, 5, 173, 24, 147, 59, 33, 106, 40, 255, 172, 82, 2, 131, 32, 178, 236])
    ec_info = consts.ECC[5][consts.ERROR_LEVEL_Q][1]
    eq_(error_block, encoder.make_error_block(ec_info, data_block))


def test_make_error_block_iso_i2():
    # ISO/IEC 18004:2006(E) - I.2 Encoding a QR Code symbol -- page 94
    # Input: 01234567
    # Symbol: 1-M
    s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001'
    data_block = Buffer(bits(s)).toints()
    error_s = '10100101 00100100 11010100 11000001 11101101 00110110 11000111 10000111 00101100 01010101'
    error_block = Buffer(bits(error_s)).toints()
    ec_info = consts.ECC[1][consts.ERROR_LEVEL_M][0]
    eq_(ec_info.num_total - ec_info.num_data, len(error_block))
    eq_(bytearray(error_block), encoder.make_error_block(ec_info, data_block))


def test_make_error_block_iso_i3():
    # ISO/IEC 18004:2006(E) - I.3 Encoding a Micro QR Code symbol  -- page 96
    # Input: 01234567
    # Symbol: M2-L
    s = '01000000 00011000 10101100 11000011 00000000'
    data_block = Buffer(bits(s)).toints()
    error_s = '10000110 00001101 00100010 10101110 00110000'
    error_block = Buffer(bits(error_s)).toints()
    ec_info = consts.ECC[consts.VERSION_M2][consts.ERROR_LEVEL_L][0]
    eq_(ec_info.num_total - ec_info.num_data, len(error_block))
    eq_(bytearray(error_block), encoder.make_error_block(ec_info, data_block))


def test_make_final_message_iso_i2():
    # ISO/IEC 18004:2015(E) - I.2 Encoding a QR Code symbol  -- page 94
    # Input: 01234567
    # Symbol: 1-M
    s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001'
    codewords = Buffer(bits(s)).toints()
    expected_s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 10100101 00100100 11010100 11000001 11101101 00110110 11000111 10000111 00101100 01010101'
    expected = bits(expected_s)
    eq_(expected, encoder.make_final_message(1, consts.ERROR_LEVEL_M, codewords).getbits())


def test_make_final_message_iso_i3():
    # ISO/IEC 18004:2015(E) - I.3 Encoding a Micro QR Code symbol  -- page 96
    # Input: 01234567
    # Symbol: M2-L
    s = '01000000 00011000 10101100 11000011 00000000'
    codewords = Buffer(bits(s)).toints()
    expected_s = '01000000 00011000 10101100 11000011 00000000 10000110 00001101 00100010 10101110 00110000'
    expected = bits(expected_s)
    eq_(expected, encoder.make_final_message(consts.VERSION_M2, consts.ERROR_LEVEL_L, codewords).getbits())


def test_make_final_message_thonky():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    codewords = [67,85,70,134,87,38,85,194,119,50,6,18,6,103,38,
                 246,246,66,7,118,134,242,7,38,86,22,198,199,146,6,
                 182,230,247,119,50,7,118,134,87,38,82,6,134,151,50,7,
                 70,247,118,86,194,6,151,50,16,236,17,236,17,236,17,236]
    s = '01000011111101101011011001000110010101011111011011100110111101110100011001000010111101110111011010000110000001110111011101010110010101110111011000110010110000100010011010000110000001110000011001010101111100100111011010010111110000100000011110000110001100100111011100100110010101110001000000110010010101100010011011101100000001100001011001010010000100010001001011000110000001101110110000000110110001111000011000010001011001111001001010010111111011000010011000000110001100100001000100000111111011001101010101010111100101001110101111000111110011000111010010011111000010110110000010110001000001010010110100111100110101001010110101110011110010100100110000011000111101111011011010000101100100111111000101111100010010110011101111011111100111011111001000100001111001011100100011101110011010101111100010000110010011000010100010011010000110111100001111111111011101011000000111100110101011001001101011010001101111010101001001101111000100010000101000000010010101101010001101101100100000111010000110100011111100000010000001101111011110001100000010110010001001111000010110001101111011000000000'
    expected = bits(s)
    res = encoder.make_final_message(5, consts.ERROR_LEVEL_Q, codewords)
    eq_(len(expected), len(res))
    eq_(expected, res.getbits())


def test_encode_iso_fig1():
    # ISO/IEC 18004:2015(E) - page 7
    # 'QR Code Symbol' as 1-M symbol
    qr = encoder.encode('QR Code Symbol', error='M', mask=None, micro=False)
    eq_(consts.ERROR_LEVEL_M, qr.error)
    eq_(1, qr.version)
    eq_(5, qr.mask, 'Wrong mask, got: {0}'.format(qr.mask))
    ref_matrix = read_matrix('iso-fig-1')
    eq_(ref_matrix, qr.matrix)


def test_encode_iso_i2():
    # ISO/IEC 18004:2015(E) - page 94
    # 01234567 as 1-M symbol
    #TODO: Without the mask param Segno chooses mask 3 which seems to be correct
    # Mask 2 is IMO an error in the standard
    qr = encoder.encode('01234567', error='m', version=1, mask=2, micro=False)
    eq_(consts.ERROR_LEVEL_M, qr.error)
    eq_(1, qr.version)
    eq_(2, qr.mask, 'Wrong mask, got: {0}'.format(qr.mask))
    qr = encoder.encode('01234567', error='m', mask=2, micro=False)
    eq_(consts.ERROR_LEVEL_M, qr.error)
    eq_(1, qr.version)
    eq_(2, qr.mask, 'Wrong mask, got: {0}'.format(qr.mask))
    ref_matrix = read_matrix('iso-i2')
    eq_(ref_matrix, qr.matrix)


def test_encode_iso_i3():
    # ISO/IEC 18004:2015(E) - page 96
    # 01234567 as M2-L symbol
    qr = encoder.encode('01234567', error='l', version='m2', mask=1, micro=True)
    eq_(consts.ERROR_LEVEL_L, qr.error)
    eq_(consts.VERSION_M2, qr.version)
    eq_(1, qr.mask, 'Wrong mask, got: {0}'.format(qr.mask))
    qr = encoder.encode('01234567', error='l', version=None, mask=1, micro=True)
    eq_(consts.ERROR_LEVEL_L, qr.error)
    eq_(consts.VERSION_M2, qr.version)
    eq_(1, qr.mask, 'Wrong mask, got: {0}'.format(qr.mask))
    ref_matrix = read_matrix('iso-i3')
    eq_(ref_matrix, qr.matrix)


def test_codeword_placement_iso_i2():
    # ISO/IEC 18004:2015(E) - page 96
    # 01234567 as M2-L symbol
    s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001'
    codewords = Buffer(bits(s)).toints()
    version = 1
    buff = encoder.make_final_message(version, consts.ERROR_LEVEL_M, codewords)
    expected_s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 10100101 00100100 11010100 11000001 11101101 00110110 11000111 10000111 00101100 01010101'
    expected = bits(expected_s)
    eq_(expected, buff.getbits())
    matrix = encoder.make_matrix(version)
    encoder.add_finder_patterns(matrix, is_micro=False)
    encoder.add_codewords(matrix, buff, is_micro=False)
    ref_matrix = read_matrix('iso-i2_code_placement')
    eq_(ref_matrix, matrix)


def test_codeword_placement_iso_i3():
    # ISO/IEC 18004:2015(E) - page 96
    # 01234567 as M2-L symbol
    s = '01000000 00011000 10101100 11000011 00000000'
    codewords = Buffer(bits(s)).toints()
    version = consts.VERSION_M2
    buff = encoder.make_final_message(version, consts.ERROR_LEVEL_L, codewords)
    expected_s = '01000000 00011000 10101100 11000011 00000000 10000110 00001101 00100010 10101110 00110000'
    expected = bits(expected_s)
    eq_(expected, buff.getbits())
    matrix = encoder.make_matrix(version)
    encoder.add_finder_patterns(matrix, is_micro=True)
    encoder.add_codewords(matrix, buff, is_micro=True)
    ref_matrix = read_matrix('iso-i3_code_placement')
    eq_(ref_matrix, matrix)


def _make_figure22_matrix():
    version = consts.VERSION_M4
    matrix = encoder.make_matrix(version)
    for row in matrix:
        for i in range(len(row)):
           if row[i] == 0x2:
                row[i] = 0x0
    encoder.add_finder_patterns(matrix, True)
    return matrix


def test_figure22_mask0():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 0
    version = consts.VERSION_M4
    matrix = _make_figure22_matrix()
    matrix, mask = encoder.find_best_mask(matrix, version, 'm', True,
                                          proposed_mask=0)
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix = read_matrix('fig-22-mask-0')
    eq_(len(ref_matrix), len(matrix))
    eq_(ref_matrix, matrix)


def test_figure22_mask1():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 1
    version = consts.VERSION_M4
    matrix = _make_figure22_matrix()
    matrix, mask = encoder.find_best_mask(matrix, version, 'm', True,
                                          proposed_mask=1)
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix = read_matrix('fig-22-mask-1')
    eq_(len(ref_matrix), len(matrix))
    eq_(ref_matrix, matrix)


def test_figure22_mask2():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 2
    version = consts.VERSION_M4
    matrix = _make_figure22_matrix()
    matrix, mask = encoder.find_best_mask(matrix, version, 'm', True,
                                          proposed_mask=2)
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix = read_matrix('fig-22-mask-2')
    eq_(len(ref_matrix), len(matrix))
    eq_(ref_matrix, matrix)


def test_figure22_mask3():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 3
    version = consts.VERSION_M4
    matrix = _make_figure22_matrix()
    matrix, mask = encoder.find_best_mask(matrix, version, 'm', True,
                                          proposed_mask=3)
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix = read_matrix('fig-22-mask-3')
    eq_(len(ref_matrix), len(matrix))
    eq_(ref_matrix, matrix)


def test_fig23_best_mask():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 23
    matrix = read_matrix('fig-23-unmasked')
    masked_matrix, mask = encoder.find_best_mask(matrix, 1, error=None, is_micro=False)
    eq_(0, mask)
    ref_matrix = read_matrix('fig-23-mask-0')
    eq_(ref_matrix, masked_matrix)


def test_format_info_figure26():
    # 7.9.2 Micro QR Code symbols (page 57)
    version = consts.VERSION_M1
    mask = 3
    matrix = tuple([bytearray([0x0] * 11) for i in range(11)])
    encoder.add_timing_pattern(matrix, is_micro=True)
    encoder.add_finder_patterns(matrix, is_micro=True)
    encoder.add_format_info(matrix, version=version, error=None, mask_pattern=mask)
    ref_matrix = read_matrix('fig-26')
    eq_(len(ref_matrix), len(matrix))
    eq_(ref_matrix, matrix)



if __name__ == '__main__':
    import nose
    nose.core.runmodule()
