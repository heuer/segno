#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the encoder module.
"""
import pytest
from segno import consts
from segno import encoder
from segno.encoder import Buffer
try:
    from .tutils import read_matrix
# Attempted relative import in non-package
except (ValueError, SystemError, ImportError):
    from tutils import read_matrix


def bits(s):
    return bytearray([int(x, 2) for x in s if x != ' '])


def check_prepare_data(expected, data, mode, encoding):
    assert expected[1:] == tuple(encoder.prepare_data(data, mode, encoding))[1:]


def test_version_as_str():
    qr = encoder.encode('test', version='1', error=None, mode=None, mask=None,
                        eci=None, micro=None, encoding=None)
    assert 1 == qr.version


@pytest.mark.parametrize('data', ['1234567', '666'])
@pytest.mark.parametrize('mode', [None, consts.MODE_NUMERIC])
def test_prepare_data_numeric(data, mode):
    expected = ((data.encode('ascii'), len(data), consts.MODE_NUMERIC, None),)
    check_prepare_data(expected, data, mode, None)


@pytest.mark.parametrize('data', ['1234567', '666'])
@pytest.mark.parametrize('mode', [None, consts.MODE_NUMERIC,
                                  consts.MODE_ALPHANUMERIC, consts.MODE_BYTE])
def test_prepare_data_override_numeric(data, mode):
    encoding = None if mode != consts.MODE_BYTE else consts.DEFAULT_BYTE_ENCODING
    expected = ((data.encode('ascii'), len(data), mode or consts.MODE_NUMERIC, encoding),)
    check_prepare_data(expected, data, mode, None)


@pytest.mark.parametrize('data', (
        'HELLO WORLD',
        'ABCDEF',
        'HELLO    WORLD ',
        '-123',
    ))
@pytest.mark.parametrize('mode', [None, consts.MODE_ALPHANUMERIC])
def test_prepare_data_alphanumeric(data, mode):
    expected = ((data.encode('ascii'), len(data), consts.MODE_ALPHANUMERIC, None),)
    check_prepare_data(expected, data, mode, None)


@pytest.mark.parametrize('data', (
        'HELLO WORLD',
        'ABCDEF',
        'HELLO    WORLD ',
    ))
@pytest.mark.parametrize('mode', (None, consts.MODE_ALPHANUMERIC, consts.MODE_BYTE))
def test_prepare_data_override_alphanumeric(data, mode):
    encoding = None if mode != consts.MODE_BYTE else consts.DEFAULT_BYTE_ENCODING
    expected = ((data.encode('ascii'), len(data), mode or consts.MODE_ALPHANUMERIC, encoding),)
    check_prepare_data(expected, data, mode, None)


def _make_test_prepare_data_byte_data():
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
                yield expected, data, mode, param_encoding


@pytest.mark.parametrize('expected, data, mode, param_encoding',
                         _make_test_prepare_data_byte_data())
def test_prepare_data_byte(expected, data, mode, param_encoding):
    check_prepare_data(expected, data, mode, param_encoding)


def test_prepare_data_multiple():
    test_data = ['a', '1']
    segments = encoder.prepare_data(test_data, None, None)
    assert 2 == len(segments)
    assert 12 == segments.bit_length
    assert (1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING) == segments[0][1:]
    assert (1, consts.MODE_NUMERIC, None) == segments[1][1:]


def test_prepare_data_multiple2():
    test_data = ['a']
    segments = encoder.prepare_data(test_data, None, None)
    assert 1 == len(segments)
    assert 8 == segments.bit_length
    assert (1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING) == segments[0][1:]


def test_prepare_data_multiple_int():
    test_data = [1]
    segments = encoder.prepare_data(test_data, None, None)
    assert 1 == len(segments)
    assert 4 == segments.bit_length
    assert (1, consts.MODE_NUMERIC, None) == segments[0][1:]


def test_prepare_data_multiple_override():
    test_data = [(1, consts.MODE_ALPHANUMERIC), 2]
    segments = encoder.prepare_data(test_data, None, None)
    assert 2 == len(segments)
    assert 10 == segments.bit_length
    assert (1, consts.MODE_ALPHANUMERIC, None) == segments[0][1:]
    assert (1, consts.MODE_NUMERIC, None) == segments[1][1:]


def test_prepare_data_multiple_mode_none():
    test_data = [(1, None), ('A', None)]
    segments = encoder.prepare_data(test_data, None, None)
    assert 2 == len(segments)
    assert 10 == segments.bit_length
    assert (1, consts.MODE_NUMERIC, None) == segments[0][1:]
    assert (1, consts.MODE_ALPHANUMERIC, None) == segments[1][1:]


def test_prepare_data_multiple_mode_none_ignore_encoding():
    test_data = [(1, None, consts.DEFAULT_BYTE_ENCODING), ('A', None, 'utf-8')]
    segments = encoder.prepare_data(test_data, None, None)
    assert 2 == len(segments)
    assert 10 == segments.bit_length
    assert (1, consts.MODE_NUMERIC, None) == segments[0][1:]
    assert (1, consts.MODE_ALPHANUMERIC, None) == segments[1][1:]


def test_prepare_data_multiple_mode_none_encoding():
    test_data = [('Ä', None, consts.DEFAULT_BYTE_ENCODING), ('Ä', None, 'utf-8'),
                 ('Ä', None, None)]
    segments = encoder.prepare_data(test_data, None, None)
    assert 3 == len(segments)
    assert 32 == segments.bit_length
    seg1, seg2, seg3 = segments
    mode, encoding = consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING
    assert (len('Ä'.encode(consts.DEFAULT_BYTE_ENCODING)), mode, encoding) == seg1[1:]
    encoding = 'utf-8'
    assert (len('Ä'.encode()), mode, encoding) == seg2[1:]
    assert seg1 == seg3  # Encoding detection should produce the same result as 1st tuple


def test_prepare_data_multiple_tuple():
    test_data = ('a', '1')
    segments = encoder.prepare_data(test_data, None, None)
    assert 2 == len(segments)
    assert 12 == segments.bit_length
    assert (1, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING) == segments[0][1:]
    assert (1, consts.MODE_NUMERIC, None) == segments[1][1:]


def test_write_segment_eci_standard_value():
    # See ISO/IEC 18004:2006(E) -- 6.4.2.1 ECI Designator - EXAMPLE (page 24)
    encoding = 'ISO-8859-7'
    # TODO: ?
    # NOTE: ISO/IEC 18004:2006(E) uses "ΑΒΓΔΕ" but text says:
    # (character values A1HEX, A2HEX, A3HEX, A4HEX, A5HEX) and result seems
    # to use the A...HEX values as well
    s = '\u2018\u2019\u00A3\u20AC\u20AF'.encode(encoding)
    seg = encoder.make_segment(s, consts.MODE_BYTE, encoding)
    buff = Buffer()
    v, vrange = None, consts.VERSION_RANGE_01_09
    encoder.write_segment(buff, seg, v, vrange, True)
    expected = bits('0111 00001001 0100 00000101 10100001 10100010 10100011 10100100 10100101')
    result = buff.getbits()
    assert len(expected) == len(result)
    assert expected == result


@pytest.mark.parametrize('eci', [True, False])
def test_write_segment_numeric_standard_value_example1(eci):
    # See ISO/IEC 18004:2006(E) -- 6.4.3 Numeric mode - EXAMPLE 1 (page 25)
    s = b'01234567'
    seg = encoder.make_segment(s, consts.MODE_NUMERIC)
    buff = Buffer()
    v, vrange = None, consts.VERSION_RANGE_01_09
    encoder.write_segment(buff, seg, v, vrange, eci=eci)
    assert bits('00010000001000000000110001010110011000011') == buff.getbits()


@pytest.mark.parametrize('eci', [True, False])
def test_write_segment_numeric_standard_value_example2(eci):
    # See ISO/IEC 18004:2006(E) -- 6.4.3 Numeric mode - EXAMPLE 2 (page 25)
    s = b'0123456789012345'
    seg = encoder.make_segment(s, consts.MODE_NUMERIC)
    buff = Buffer()
    v, vrange = consts.VERSION_M3, consts.VERSION_M3
    encoder.write_segment(buff, seg, v, vrange, eci=eci)
    assert bits('0010000000000110001010110011010100110111000010100111010100101') == buff.getbits()


@pytest.mark.parametrize('eci', [True, False])
def test_write_segment_numeric_standard_value_i3(eci):
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    s = b'01234567'
    seg = encoder.make_segment(s, consts.MODE_NUMERIC)
    buff = Buffer()
    v, vrange = consts.VERSION_M2, consts.VERSION_M2
    encoder.write_segment(buff, seg, v, vrange, eci=eci)
    assert bits('01000000000110001010110011000011') == buff.getbits()


@pytest.mark.parametrize('eci', [True, False])
def test_write_segment_alphanumeric_standard_value_example(eci):
    # See ISO/IEC 18004:2006(E) -- 6.4.3 Numeric mode - EXAMPLE (page 26)
    s = b'AC-42'
    seg = encoder.make_segment(s, consts.MODE_ALPHANUMERIC)
    buff = Buffer()
    v, vrange = None, consts.VERSION_RANGE_01_09
    encoder.write_segment(buff, seg, v, vrange, eci=eci)
    assert bits('00100000001010011100111011100111001000010') == buff.getbits()


@pytest.mark.parametrize('eci', [True, False])
def test_write_segment_alphanumeric_thonky(eci):
    # <http://www.thonky.com/qr-code-tutorial/data-encoding/#step-3-encode-using-the-selected-mode>
    s = b'HELLO WORLD'
    seg = encoder.make_segment(s, consts.MODE_ALPHANUMERIC, None)
    buff = Buffer()
    v, vrange = None, consts.VERSION_RANGE_01_09
    encoder.write_segment(buff, seg, v, vrange, eci)
    assert bits('00100000010110110000101101111000110100010111001011011100010011010100001101') == buff.getbits()


@pytest.mark.parametrize('eci', [True, False])
def test_write_segment_bytes_thonky(eci):
    # <http://www.thonky.com/qr-code-tutorial/byte-mode-encoding/>
    s = b'Hello, world!'
    seg = encoder.make_segment(s, consts.MODE_BYTE, consts.DEFAULT_BYTE_ENCODING)
    buff = Buffer()
    v, vrange = None, consts.VERSION_RANGE_01_09
    encoder.write_segment(buff, seg, v, vrange, eci=eci)
    assert bits('010000001101'
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
                '00100001') == buff.getbits()


def test_write_terminator_thonky():
    # <http://www.thonky.com/qr-code-tutorial/data-encoding/#add-a-terminator-of-0s-if-necessary>
    data = bits('00100000010110110000101101111000110100010111001011011100010011010100001101')
    buff = Buffer(data)
    version = 1
    v = None
    capacity = consts.SYMBOL_CAPACITY[version][consts.ERROR_LEVEL_Q]
    encoder.write_terminator(buff, capacity, v, len(data))
    assert data + bits('0000') == buff.getbits()


def test_write_terminator_standard_value_i2():
    # See ISO/IEC 18004:2006(E) -- I.2 Encoding a QR Code symbol (page 94)
    data = bits('000100000010000000001100010101100110000110000')
    buff = Buffer(data)
    version = 1
    v = None
    capacity = consts.SYMBOL_CAPACITY[version][consts.ERROR_LEVEL_M]
    encoder.write_terminator(buff, capacity, v, len(data))
    assert data + bits('0000') == buff.getbits()


def test_write_terminator_standard_value_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    data = bits('01000000000110001010110011000011')
    buff = Buffer(data)
    version = consts.VERSION_M2
    capacity = consts.SYMBOL_CAPACITY[version][consts.ERROR_LEVEL_L]
    encoder.write_terminator(buff, capacity, version, len(data))
    assert data + bits('00000') == buff.getbits()


def test_write_padding_bits_iso_i2():
    # See ISO/IEC 18004:2006(E) -- I.2 Encoding a QR Code symbol (page 94)
    data = bits('0001 0000001000 0000001100 0101011001 1000011 0000')
    buff = Buffer(data)
    version = 1
    encoder.write_padding_bits(buff, version, len(buff))
    assert bits('00010000 00100000 00001100 01010110 01100001 10000000') == buff.getbits()


def test_write_padding_bits_iso_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    data = bits('0 1000 0000001100 0101011001 1000011 00000')
    buff = Buffer(data)
    version = consts.VERSION_M2
    encoder.write_padding_bits(buff, version, len(buff))
    assert bits('01000000 00011000 10101100 11000011 00000000') == buff.getbits()


def test_write_padding_bits_thonky():
    # <http://www.thonky.com/qr-code-tutorial/data-encoding>
    data = bits('00100000 01011011 00001011 01111000 11010001 01110010 11011100 '
                '01001101 01000011 010000')
    buff = Buffer(data)
    version = 1
    encoder.write_padding_bits(buff, version, len(buff))
    assert bits('00100000 01011011 00001011 01111000 11010001 01110010 11011100 '
                '01001101 01000011 01000000') == buff.getbits()


def test_write_pad_codewords_standard_value_i2():
    # See ISO/IEC 18004:2006(E) -- I.2 Encoding a QR Code symbol (page 94)
    data = bits('00010000 00100000 00001100 01010110 01100001 10000000')
    buff = Buffer(data)
    version = 1
    error = consts.ERROR_LEVEL_M
    capacity = consts.SYMBOL_CAPACITY[version][error]
    encoder.write_pad_codewords(buff, version, capacity, len(buff))
    assert data + bits('1110110000010001111011000001000111101100000100011110110'
                       '0000100011110110000010001') == buff.getbits()


def test_write_pad_codewords_standard_value_i3():
    # See ISO/IEC 18004:2006(E) -- I.3 Encoding a Micro QR Code symbol (page 96)
    data = bits('0100000000011000101011001100001100000000')
    buff = Buffer(data)
    version = consts.VERSION_M2
    error = consts.ERROR_LEVEL_L
    capacity = consts.SYMBOL_CAPACITY[version][error]
    encoder.write_pad_codewords(buff, version, capacity, len(buff))
    assert data == buff.getbits()


@pytest.mark.parametrize('data', [b'ABCDEF', b'A', b'A1', b'1A', b'HTTP://WWW.EXAMPLE.ORG',
                                  b'666', b' ', b'HELLO WORLD', b'AC-42',
                                  consts.ALPHANUMERIC_CHARS])
def test_is_alphanumeric(data):
    assert encoder.is_alphanumeric(data)


@pytest.mark.parametrize('data', [b'a', b'0123b', b'_', b'http://www.example.org/',  b'',
                                  'ü'.encode(), 'Ü'.encode(),
                                  'ä'.encode(consts.DEFAULT_BYTE_ENCODING), b'HELLO\nWORLD', b'Ab'])
def test_is_not_alphanumeric(data):
    assert not encoder.is_alphanumeric(data)


@pytest.mark.parametrize('data', ['点', '漢字', '外来語', 'あめかんむり', 'ひへん', 'くさかんむり'])
def test_is_kanji(data):
    assert encoder.is_kanji(data.encode('shift_jis'))


@pytest.mark.parametrize('data', ['abcdef', '1234', '1234a', 'ABCDEF'])
def test_is_not_kanji(data):
    assert not encoder.is_kanji(data.encode('shift_jis'))


_test_find_mode_test_data = (
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
        ('外来語'.encode(), consts.MODE_BYTE),
    )


@pytest.mark.parametrize('data, expected', _test_find_mode_test_data)
def test_find_mode(data, expected):
    assert expected == encoder.find_mode(data)


@pytest.mark.parametrize('version, expected',  # Version, matrix size
                                               [('M1', 11),
                                                ('M2', 13),
                                                ('M3', 15),
                                                ('M4', 17),
                                                (1, 21),
                                                (27, 125),
                                                (40, 177)])
def test_get_matrix_size(version, expected):
    try:
        v = consts.MICRO_VERSION_MAPPING[version]
    except KeyError:
        v = version
    assert expected == encoder.calc_matrix_size(v)


# See ISO/IEC 18004:2006(E) - Table 2 (page 22)
_test_is_mode_supported_micro_data = (
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


@pytest.mark.parametrize('mode, version, expected', _test_is_mode_supported_micro_data)
def test_is_mode_supported_micro(mode, version, expected):
    v = consts.MICRO_VERSION_MAPPING[version]
    assert expected == encoder.is_mode_supported(mode, v)


@pytest.mark.parametrize('version', tuple(range(1, 41)))
@pytest.mark.parametrize('mode', (consts.MODE_NUMERIC, consts.MODE_ALPHANUMERIC,
                                  consts.MODE_BYTE, consts.MODE_ECI, consts.MODE_KANJI))
def test_is_mode_supported_micro2(version, mode):
    assert encoder.is_mode_supported(mode, version)


@pytest.mark.parametrize('mode, version', [(-1, 1), (-2, consts.VERSION_M2),
                                           (10, 1), (10, consts.VERSION_M1),
                                           (9, 39)])
def test_is_mode_supported_invalid_mode(mode, version):
    with pytest.raises(ValueError) as ex:
        encoder.is_mode_supported(mode, version)
    assert 'mode' in str(ex.value)


@pytest.mark.parametrize('mode', ('kanij', 'binary', 'blub', ''))
def test_normalize_mode_illegal(mode):
    with pytest.raises(ValueError) as ex:
        encoder.normalize_mode(mode)
    assert 'mode' in str(ex.value)


@pytest.mark.parametrize('mask', tuple(range(8)))
def test_normalize_mask(mask):
    assert mask == encoder.normalize_mask(mask, is_micro=False)


@pytest.mark.parametrize('mask', tuple(range(4)))
def test_normalize_mask_micro(mask):
    assert mask == encoder.normalize_mask(mask, is_micro=True)


def test_normalize_mask_none():
    assert encoder.normalize_mask(None, is_micro=True) is None
    assert encoder.normalize_mask(None, is_micro=False) is None


@pytest.mark.parametrize('version, mask', [(consts.VERSION_M1, 8), (1, 9), (1, -1)])
def test_normalize_mask_illegal(version, mask):
    with pytest.raises(ValueError):
        encoder.normalize_mask(mask, version < 1)


def test_mode_name_illegal():
    with pytest.raises(ValueError):
        encoder.get_mode_name(7)


def test_error_name_illegal():
    with pytest.raises(ValueError):
        encoder.get_error_name(7)


def test_version_name_illegal():
    with pytest.raises(ValueError):
        encoder.get_version_name(41)


def test_version_range_illegal():
    with pytest.raises(ValueError):
        encoder.version_range(41)


def test_normalize_errorlevel():
    assert consts.ERROR_LEVEL_H == encoder.normalize_errorlevel('h')
    assert consts.ERROR_LEVEL_Q == encoder.normalize_errorlevel('Q')
    assert encoder.normalize_errorlevel(None, accept_none=True) is None
    assert consts.ERROR_LEVEL_M == encoder.normalize_errorlevel(consts.ERROR_LEVEL_M)


def test_normalize_errorlevel_illegal():
    with pytest.raises(ValueError):
        encoder.normalize_errorlevel('g')


def test_normalize_errorlevel_illegal2():
    with pytest.raises(ValueError) as ex:
        encoder.normalize_errorlevel(None)
    assert 'error' in str(ex.value)


_test_find_version_test_data = (
    # data, error, micro, expected version
    ('12345', None, True, consts.VERSION_M1),
    ('12345', consts.ERROR_LEVEL_L, True, consts.VERSION_M2),
    # Error level Q isn't suppoted by M1 - M3
    ('12345', consts.ERROR_LEVEL_Q, True, consts.VERSION_M4),
    # Error level H isn't supported by Micro QR Codes
    ('12345', consts.ERROR_LEVEL_H, None, 1),
    ('12345', None, False, 1),
    (12345, None, True, consts.VERSION_M1),
    (-12345, None, True, consts.VERSION_M2),  # Negative number
    (-12345, consts.ERROR_LEVEL_M, True, consts.VERSION_M3),  # Negative number
    (12345, None, False, 1),
    ('123456', None, True, consts.VERSION_M2),
    ('123456', None, False, 1),
    (123456, None, True, consts.VERSION_M2),
    (123456, None, False, 1),
    ('ABCDE', None, True, consts.VERSION_M2),  # Alphanumeric isn't supported by M1
    ('ABCDEF', consts.ERROR_LEVEL_L, True, consts.VERSION_M2),
    ('ABCDEF', consts.ERROR_LEVEL_M, True, consts.VERSION_M3),  # Too much data for error level M and version M2
    ('ABCDEF', consts.ERROR_LEVEL_L, False, 1),
    ('ABCDEF', consts.ERROR_LEVEL_L, False, 1),
    ('Märchenbuch', None, True, consts.VERSION_M4),
    ('Märchenbücher', None, False, 1),
    ('Märchenbücherei', None, None, consts.VERSION_M4),
    ('Märchenbücherei', consts.ERROR_LEVEL_M, None, 2),
)


@pytest.mark.parametrize('data, error, micro, expected_version', _test_find_version_test_data)
def test_find_version(data, error, micro, expected_version):
    segments = encoder.prepare_data(data, None, None)
    assert expected_version == encoder.find_version(segments, error, eci=False, micro=micro)


def test_thonky_add_format_info():
    # <http://www.thonky.com/qr-code-tutorial/format-version-information#put-the-format-string-into-the-qr-code>
    version = 1
    width, height = 21, 21  # Version 1
    matrix = encoder.make_matrix(width, height, reserve_regions=False)
    encoder.add_finder_patterns(matrix, width, height)
    encoder.add_format_info(matrix, version, consts.ERROR_LEVEL_L, 4)
    ref_matrix, ref_matrix_width, ref_matrix_height = read_matrix('thonky_format')
    assert ref_matrix_width, ref_matrix_height == (width, height)
    assert ref_matrix == matrix


def test_thonky_add_version_info():
    # <http://www.thonky.com/qr-code-tutorial/format-version-information>
    version = 7
    width, height = 45, 45  # Version 7
    matrix = encoder.make_matrix(width, height, reserve_regions=False)
    encoder.add_finder_patterns(matrix, width, height)
    encoder.add_alignment_patterns(matrix, width, height)
    encoder.add_version_info(matrix, version)
    matrix[-8][8] = 0x1  # dark module
    ref_matrix, ref_matrix_width, ref_matrix_height = read_matrix('thonky_version')
    assert ref_matrix_width, ref_matrix_height == (width, height)
    assert ref_matrix == matrix


def test_eval_micro():
    # ISO/IEC 18004:2006(E) page 54
    # 6.8.2.2 Evaluation of Micro QR Code symbols
    matrix, width, height = read_matrix('iso_6.8.2.2')
    res = encoder.evaluate_micro_mask(matrix, width, height)
    assert 104 == res


def make_thonky_score_matrix():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    return read_matrix('thonky_datamasking-1')


def test_score_n1():
    matrix, width, height = make_thonky_score_matrix()
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[0]
    assert 180 == score


def test_score_n2():
    matrix, width, height = make_thonky_score_matrix()
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[1]
    assert 90 == score


def test_score_n3():
    matrix, width, height = make_thonky_score_matrix()
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[2]
    # Thonky: 80
    assert 760 == score


def test_score_n4():
    matrix, width, height = read_matrix('thonky_datamasking-2')
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[3]
    assert 0 == score


def test_thonky_pattern_0():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-0')
    scores = encoder.mask_scores(matrix, width, height)
    assert 180 == scores[0]
    assert 90 == scores[1]
    # Thonky: 80
    assert 760 == scores[2]
    assert 0 == scores[3]
    # See score 3
    assert 350 - 80 + 760 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_1():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-1')
    scores = encoder.mask_scores(matrix, width, height)
    assert 172 == scores[0]
    assert 129 == scores[1]
    # Thonky: 120
    assert 760 == scores[2]
    assert 0 == scores[3]
    # See score 3
    assert 421 - 120 + 760 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_2():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-2')
    scores = encoder.mask_scores(matrix, width, height)
    assert 206 == scores[0]
    assert 141 == scores[1]
    # Thonky: 160
    assert 800 == scores[2]
    assert 0 == scores[3]
    assert 507 - 160 + 800 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_3():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-3')
    scores = encoder.mask_scores(matrix, width, height)
    assert 180 == scores[0]
    assert 141 == scores[1]
    # Thonky: 120
    assert 760 == scores[2]
    # Thonky: 2, but that's impossible: Either 0 or a multiple of 10 (N4 = 10)
    assert 0 == scores[3]
    assert 443 - 2 - 120 + 760 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_4():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-4')
    scores = encoder.mask_scores(matrix, width, height)
    assert 195 == scores[0]
    assert 138 == scores[1]
    # Thonky: 200
    assert 800 == scores[2]
    assert 0 == scores[3]
    # See score 3
    assert 533 - 200 + 800 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_5():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-5')
    scores = encoder.mask_scores(matrix, width, height)
    assert 189 == scores[0]
    assert 156 == scores[1]
    # Thonky: 200
    assert 800 == scores[2]
    # Thonky: 2, but that's impossible: Either 0 or a multiple of 10 (N4 = 10)
    assert 0 == scores[3]
    # See score 3 and 4
    assert 547 - 2 - 200 + 800 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_6():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-6')
    scores = encoder.mask_scores(matrix, width, height)
    assert 171 == scores[0]
    assert 102 == scores[1]
    # Thonky: 80
    assert 840 == scores[2]
    # Thonky: 4, but that's impossible: Either 0 or a multiple of 10 (N4 = 10)
    assert 0 == scores[3]
    # See score 3 and 4
    assert 357 - 4 - 80 + 840 == encoder.evaluate_mask(matrix, width, height)


def test_thonky_pattern_7():
    # http://www.thonky.com/qr-code-tutorial/data-masking
    matrix, width, height = read_matrix('thonky_datamasking_mask-7')
    scores = encoder.mask_scores(matrix, width, height)
    assert 197 == scores[0]
    assert 123 == scores[1]
    # Thonky: 200
    assert 720 == scores[2]
    assert 0 == scores[3]
    # See score 3
    assert 520 - 200 + 720 == encoder.evaluate_mask(matrix, width, height)


def test_score_n1_iso():
    # For example, impose 5 penalty points on the block of “dark:dark:dark:dark:dark:dark:dark”
    # module pattern, where a series of seven consecutive modules is counted as one block
    matrix = tuple(bytearray([1] * 7) for i in range(7))
    width, height = [len(matrix)] * 2
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[0]
    assert 5 * 7 * 2 == score


def test_score_n2_iso():
    # Take a block consisting of 3 x 3 dark
    # modules for an example. Considering that up to four 2 x 2 dark modules can
    # be included in this block, the penalty applied to this block shall be
    # calculated as 4 (blocks) x 3 (points) = 12 points.
    matrix = (bytearray([1, 1, 1]), bytearray([1, 1, 1]), bytearray([1, 1, 1]))
    width, height = [len(matrix)] * 2
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[1]
    assert 12 == score

    matrix = (bytearray([0, 0, 0]), bytearray([0, 0, 0]), bytearray([0, 0, 0]))
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[1]
    assert 12 == score


def _make_score_n4_data():
    for p in range(41, 46):
        yield 10, p

    for p in range(55, 60):
        yield 10, p

    for p in range(46, 55):
        yield 0, p

    yield 3 * 10, 35


@pytest.mark.parametrize('score, percent', _make_score_n4_data())
def test_score_n4_iso(score, percent):
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
                cnt += 1
                finished = cnt == percent
                if finished:
                    break
            if finished:
                break

    matrix = make_matrix()
    fill_matrix(matrix, percent)
    width, height = [len(matrix)] * 2
    scores = encoder.mask_scores(matrix, width, height)
    score = scores[3]
    assert score == score


def test_binary_sequence_to_integers():
    # <http://www.thonky.com/qr-code-tutorial/error-correction-coding>
    # HELLO WORLD as a 1-M code
    data = bits('00100000 01011011 00001011 01111000 11010001 01110010 11011100 '
                '01001101 01000011 01000000 11101100 00010001 11101100 00010001 '
                '11101100 00010001')
    expected = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    res_int = list(Buffer(data).toints())
    assert len(data) // 8 == len(res_int)
    assert expected == res_int


def test_split_into_blocks():
    # <http://www.thonky.com/qr-code-tutorial/error-correction-coding>
    # HELLO WORLD as a 5-Q code
    s = '01000011 01010101 01000110 10000110 01010111 00100110 01010101 ' \
        '11000010 01110111 00110010 00000110 00010010 00000110 01100111 ' \
        '00100110 11110110 11110110 01000010 00000111 01110110 10000110 ' \
        '11110010 00000111 00100110 01010110 00010110 11000110 11000111 ' \
        '10010010 00000110 10110110 11100110 11110111 01110111 00110010 ' \
        '00000111 01110110 10000110 01010111 00100110 01010010 00000110 ' \
        '10000110 10010111 00110010 00000111 01000110 11110111 01110110 ' \
        '01010110 11000010 00000110 10010111 00110010 11100000 11101100 ' \
        '00010001 11101100 00010001 11101100 00010001 11101100'
    data = bits(s)
    buff = Buffer(data)
    codewords = list(buff.toints())
    assert 62 == len(codewords)
    ec_infos = consts.ECC[5][consts.ERROR_LEVEL_Q]
    assert ec_infos
    assert 2 == len(ec_infos)
    blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert 4 == len(blocks)
    assert 15 == len(blocks[0])
    assert bytearray(codewords[:15]) == blocks[0]
    assert 15 == len(blocks[1])
    assert 16 == len(blocks[2])
    assert 16 == len(blocks[3])


def test_make_error_block0():
    # <http://www.thonky.com/qr-code-tutorial/error-correction-coding>
    # 1-M
    codeword = '00100000 01011011 00001011 01111000 11010001 01110010 11011100 ' \
               '01001101 01000011 01000000 11101100 00010001 11101100 00010001 ' \
               '11101100 00010001'
    codeword_ints = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    buff = Buffer(bits(codeword))
    assert codeword_ints == list(buff.toints())
    error_block = bytearray([196, 35, 39, 119, 235, 215, 231, 226, 93, 23])
    ec_infos = consts.ECC[1][consts.ERROR_LEVEL_M]
    assert 1 == len(ec_infos)
    ec_info = ec_infos[0]
    assert 1 == ec_info.num_blocks
    assert 10 == ec_info.num_total - ec_info.num_data
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert len(error_block) == len(error_blocks[0])
    assert error_block == error_blocks[0]


def test_make_error_block1():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    codeword = '01000011 01010101 01000110 10000110 01010111 00100110 01010101 ' \
               '11000010 01110111 00110010 00000110 00010010 00000110 01100111 ' \
               '00100110'
    codeword_ints = [67, 85, 70, 134, 87, 38, 85, 194, 119, 50, 6, 18, 6, 103, 38]
    buff = Buffer(bits(codeword))
    assert codeword_ints == list(buff.toints())
    error_block = bytearray([213, 199, 11, 45, 115, 247, 241, 223, 229, 248, 154, 117, 154, 111, 86, 161, 111, 39])
    ec_infos = consts.ECC[5][consts.ERROR_LEVEL_Q]
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert error_block == error_blocks[0]


def test_make_error_block2():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    codeword = '11110110 11110110 01000010 00000111 01110110 10000110 11110010 ' \
               '00000111 00100110 01010110 00010110 11000110 11000111 10010010 ' \
               '00000110'
    codeword_ints = [246, 246, 66, 7, 118, 134, 242, 7, 38, 86, 22, 198, 199,
                     146, 6]
    buff = Buffer(bits(codeword))
    assert codeword_ints == list(buff.toints())
    error_block = bytearray([87, 204, 96, 60, 202, 182, 124, 157, 200, 134, 27,
                             129, 209, 17, 163, 163, 120, 133])
    ec_infos = consts.ECC[5][consts.ERROR_LEVEL_Q]
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert error_block == error_blocks[0]


def test_make_error_block3():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    codeword = '10110110 11100110 11110111 01110111 00110010 00000111 01110110 ' \
               '10000110 01010111 00100110 01010010 00000110 10000110 10010111 ' \
               '00110010 00000111'
    codeword_ints = [182, 230, 247, 119, 50, 7, 118, 134, 87, 38, 82, 6, 134,
                     151, 50, 7]
    buff = Buffer(bits(codeword))
    assert codeword_ints == list(buff.toints())
    error_block = bytearray([148, 116, 177, 212, 76, 133, 75, 242, 238, 76,
                             195, 230, 189, 10, 108, 240, 192, 141])
    ec_infos = (consts.ECC[5][consts.ERROR_LEVEL_Q][1],)
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert error_block == error_blocks[0]


def test_make_error_block4():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    codeword = '01000110 11110111 01110110 01010110 11000010 00000110 10010111 ' \
               '00110010 00010000 11101100 00010001 11101100 00010001 11101100 ' \
               '00010001 11101100'
    codeword_ints = [70, 247, 118, 86, 194, 6, 151, 50, 16, 236, 17, 236, 17,
                     236, 17, 236]
    buff = Buffer(bits(codeword))
    assert codeword_ints == list(buff.toints())
    error_block = bytearray([235, 159, 5, 173, 24, 147, 59, 33, 106, 40, 255,
                             172, 82, 2, 131, 32, 178, 236])
    ec_infos = (consts.ECC[5][consts.ERROR_LEVEL_Q][1],)
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert error_block == error_blocks[0]


def test_make_error_block_iso_i2():
    # ISO/IEC 18004:2006(E) - I.2 Encoding a QR Code symbol -- page 94
    # Input: 01234567
    # Symbol: 1-M
    s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 ' \
        '00010001 11101100 00010001 11101100 00010001 11101100 00010001 ' \
        '11101100 00010001'
    data_block = Buffer(bits(s))
    error_s = '10100101 00100100 11010100 11000001 11101101 00110110 11000111 ' \
              '10000111 00101100 01010101'
    error_block = list(Buffer(bits(error_s)).toints())
    ec_infos = consts.ECC[1][consts.ERROR_LEVEL_M]
    ec_info = ec_infos[0]
    assert ec_info.num_total - ec_info.num_data == len(error_block)
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, data_block)
    assert bytearray(error_block) == error_blocks[0]


def test_make_error_block_iso_i3():
    # ISO/IEC 18004:2006(E) - I.3 Encoding a Micro QR Code symbol  -- page 96
    # Input: 01234567
    # Symbol: M2-L
    s = '01000000 00011000 10101100 11000011 00000000'
    buff = Buffer(bits(s))
    error_s = '10000110 00001101 00100010 10101110 00110000'
    error_block = list(Buffer(bits(error_s)).toints())
    ec_infos = consts.ECC[consts.VERSION_M2][consts.ERROR_LEVEL_L]
    ec_info = ec_infos[0]
    assert ec_info.num_total - ec_info.num_data == len(error_block)
    data_blocks, error_blocks = encoder.make_blocks(ec_infos, buff)
    assert bytearray(error_block) == error_blocks[0]


def test_make_final_message_iso_i2():
    # ISO/IEC 18004:2015(E) - I.2 Encoding a QR Code symbol  -- page 94
    # Input: 01234567
    # Symbol: 1-M
    s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 ' \
        '00010001 11101100 00010001 11101100 00010001 11101100 00010001 ' \
        '11101100 00010001'
    codewords = Buffer(bits(s))
    expected_s = '00010000 00100000 00001100 01010110 01100001 10000000 ' \
                 '11101100 00010001 11101100 00010001 11101100 00010001 ' \
                 '11101100 00010001 11101100 00010001 10100101 00100100 ' \
                 '11010100 11000001 11101101 00110110 11000111 10000111 ' \
                 '00101100 01010101'
    expected = bits(expected_s)
    assert expected == encoder.make_final_message(1, consts.ERROR_LEVEL_M,
                                                  codewords).getbits()


def test_make_final_message_iso_i3():
    # ISO/IEC 18004:2015(E) - I.3 Encoding a Micro QR Code symbol  -- page 96
    # Input: 01234567
    # Symbol: M2-L
    s = '01000000 00011000 10101100 11000011 00000000'
    codewords = Buffer(bits(s))
    expected_s = '01000000 00011000 10101100 11000011 00000000 10000110 ' \
                 '00001101 00100010 10101110 00110000'
    expected = bits(expected_s)
    assert expected == encoder.make_final_message(consts.VERSION_M2,
                                                  consts.ERROR_LEVEL_L,
                                                  codewords).getbits()


def test_make_final_message_thonky():
    # <http://www.thonky.com/qr-code-tutorial/structure-final-message>
    # 5-Q
    codewords = '01000011 01010101 01000110 10000110 01010111 00100110 01010101 ' \
                '11000010 01110111 00110010 00000110 00010010 00000110 01100111 ' \
                '00100110 11110110 11110110 01000010 00000111 01110110 10000110 ' \
                '11110010 00000111 00100110 01010110 00010110 11000110 11000111 ' \
                '10010010 00000110 10110110 11100110 11110111 01110111 00110010 ' \
                '00000111 01110110 10000110 01010111 00100110 01010010 00000110 ' \
                '10000110 10010111 00110010 00000111 01000110 11110111 01110110 ' \
                '01010110 11000010 00000110 10010111 00110010 00010000 11101100 ' \
                '00010001 11101100 00010001 11101100 00010001 11101100'
    codewords_int = [67, 85, 70, 134, 87, 38, 85, 194, 119, 50, 6, 18, 6, 103, 38,
                     246, 246, 66, 7, 118, 134, 242, 7, 38, 86, 22, 198, 199, 146, 6,
                     182, 230, 247, 119, 50, 7, 118, 134, 87, 38, 82, 6, 134, 151, 50, 7,
                     70, 247, 118, 86, 194, 6, 151, 50, 16, 236, 17, 236, 17, 236, 17, 236]
    s = '0100001111110110101101100100011001010101111101101110011011110111010001' \
        '1001000010111101110111011010000110000001110111011101010110010101110111' \
        '0110001100101100001000100110100001100000011100000110010101011111001001' \
        '1101101001011111000010000001111000011000110010011101110010011001010111' \
        '0001000000110010010101100010011011101100000001100001011001010010000100' \
        '0100010010110001100000011011101100000001101100011110000110000100010110' \
        '0111100100101001011111101100001001100000011000110010000100010000011111' \
        '1011001101010101010111100101001110101111000111110011000111010010011111' \
        '0000101101100000101100010000010100101101001111001101010010101101011100' \
        '1111001010010011000001100011110111101101101000010110010011111100010111' \
        '1100010010110011101111011111100111011111001000100001111001011100100011' \
        '1011100110101011111000100001100100110000101000100110100001101111000011' \
        '1111111101110101100000011110011010101100100110101101000110111101010100' \
        '1001101111000100010000101000000010010101101010001101101100100000111010' \
        '0001101000111111000000100000011011110111100011000000101100100010011110' \
        '00010110001101111011000000000'
    expected = bits(s)
    buff = Buffer(bits(codewords))
    assert codewords_int == list(buff.toints())
    res = encoder.make_final_message(5, consts.ERROR_LEVEL_Q, buff)
    assert len(expected) == len(res)
    assert expected == res.getbits()


def test_encode_iso_fig1():
    # ISO/IEC 18004:2015(E) - page 7
    # 'QR Code Symbol' as 1-M symbol
    qr = encoder.encode('QR Code Symbol', error='M', mask=None, micro=False, boost_error=False)
    assert consts.ERROR_LEVEL_M == qr.error
    assert 1 == qr.version
    assert 5 == qr.mask, f'Wrong mask, got: {qr.mask}'
    ref_matrix = read_matrix('iso-fig-1')[0]
    assert ref_matrix == qr.matrix


def test_encode_iso_i2():
    # ISO/IEC 18004:2015(E) - page 94
    # 01234567 as 1-M symbol
    # TODO: Without the mask param Segno chooses mask 3 which seems to be correct
    # Mask 2 is IMO an error in the standard
    qr = encoder.encode('01234567', error='m', version=1, mask=2, micro=False, boost_error=False)
    assert consts.ERROR_LEVEL_M == qr.error
    assert 1 == qr.version
    assert 2 == qr.mask, f'Wrong mask, got: {qr.mask}'
    qr = encoder.encode('01234567', error='m', mask=2, micro=False, boost_error=False)
    assert consts.ERROR_LEVEL_M == qr.error
    assert 1 == qr.version
    assert 2 == qr.mask, f'Wrong mask, got: {qr.mask}'
    ref_matrix = read_matrix('iso-i2')[0]
    assert ref_matrix == qr.matrix


def test_encode_iso_i3():
    # ISO/IEC 18004:2015(E) - page 96
    # 01234567 as M2-L symbol
    ref_matrix = read_matrix('iso-i3')[0]
    qr = encoder.encode('01234567', error='l', version='m2', boost_error=False)
    assert consts.ERROR_LEVEL_L == qr.error
    assert consts.VERSION_M2 == qr.version
    assert 1 == qr.mask, f'Wrong mask, got: {qr.mask}'
    assert ref_matrix == qr.matrix
    qr = encoder.encode('01234567', error='l', version=None, micro=True, boost_error=False)
    assert consts.ERROR_LEVEL_L == qr.error
    assert consts.VERSION_M2 == qr.version
    assert 1 == qr.mask, f'Wrong mask, got: {qr.mask}'
    assert ref_matrix == qr.matrix


def test_encode_iso_fig29():
    # ISO/IEC 18004:2015(E) - page 60
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ

    # TODO: If mask is None, Segno chooses mask 3, but the figure uses mask 4...
    qr = encoder.encode('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        error='m', mask=4, boost_error=False)
    assert 4 == qr.mask
    assert 4 == qr.version
    ref_matrix = read_matrix('iso-fig-29')[0]
    assert ref_matrix == qr.matrix


def test_codeword_placement_iso_i2():
    # ISO/IEC 18004:2015(E) - page 94
    # 01234567 as 1-M symbol
    s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 00010001 ' \
        '11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001'
    codewords = Buffer(bits(s))
    version = 1
    width, height = 21, 21
    buff = encoder.make_final_message(version, consts.ERROR_LEVEL_M, codewords)
    expected_s = '00010000 00100000 00001100 01010110 01100001 10000000 11101100 ' \
                 '00010001 11101100 00010001 11101100 00010001 11101100 00010001 ' \
                 '11101100 00010001 10100101 00100100 11010100 11000001 11101101 ' \
                 '00110110 11000111 10000111 00101100 01010101'
    expected = bits(expected_s)
    assert expected == buff.getbits()
    matrix = encoder.make_matrix(width, height)
    encoder.add_finder_patterns(matrix, width, height)
    encoder.add_codewords(matrix, buff, version=version)
    ref_matrix = read_matrix('iso-i2_code_placement')[0]
    assert ref_matrix == matrix


def test_codeword_placement_iso_i3():
    # ISO/IEC 18004:2015(E) - page 96
    # 01234567 as M2-L symbol
    s = '01000000 00011000 10101100 11000011 00000000'
    codewords = Buffer(bits(s))
    version = consts.VERSION_M2
    width, height = 13, 13
    buff = encoder.make_final_message(version, consts.ERROR_LEVEL_L, codewords)
    expected_s = '01000000 00011000 10101100 11000011 00000000 10000110 00001101 ' \
                 '00100010 10101110 00110000'
    expected = bits(expected_s)
    assert expected == buff.getbits()
    matrix = encoder.make_matrix(width, height)
    encoder.add_finder_patterns(matrix, width, height)
    encoder.add_codewords(matrix, buff, version=version)
    ref_matrix = read_matrix('iso-i3_code_placement')[0]
    assert ref_matrix == matrix


def _make_figure22_matrix():
    width, height = 17, 17  # M4
    matrix = encoder.make_matrix(width, height)
    for row in matrix:
        for i in range(len(row)):
            if row[i] == 0x2:
                row[i] = 0x0
    encoder.add_finder_patterns(matrix, width, height)
    return matrix, width, height


def test_figure22_mask0():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 0
    matrix, width, height = _make_figure22_matrix()
    mask, matrix = encoder.find_and_apply_best_mask(matrix, width, height, proposed_mask=0)
    assert 0 == mask
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix, ref_width, ref_height = read_matrix('fig-22-mask-0')
    assert ref_width, ref_height == (width, height)
    assert ref_matrix == matrix


def test_figure22_mask1():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 1
    matrix, width, height = _make_figure22_matrix()
    mask, matrix = encoder.find_and_apply_best_mask(matrix, width, height, proposed_mask=1)
    assert 1 == mask
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix, ref_width, ref_height = read_matrix('fig-22-mask-1')
    assert ref_width, ref_height == (width, height)
    assert ref_matrix == matrix


def test_figure22_mask2():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 2
    matrix, width, height = _make_figure22_matrix()
    mask, matrix = encoder.find_and_apply_best_mask(matrix, width, height, proposed_mask=2)
    assert 2 == mask
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix, ref_width, ref_height = read_matrix('fig-22-mask-2')
    assert ref_width, ref_height == (width, height)
    assert ref_matrix == matrix


def test_figure22_mask3():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 22 - Mask 3
    matrix, width, height = _make_figure22_matrix()
    mask, matrix = encoder.find_and_apply_best_mask(matrix, width, height, proposed_mask=3)
    assert 3 == mask
    # Format info = dark modules
    for i in range(9):
        matrix[8][i] = 0x1
        matrix[i][8] = 0x1
    ref_matrix, ref_width, ref_height = read_matrix('fig-22-mask-3')
    assert ref_width, ref_height == (width, height)
    assert ref_matrix == matrix


def test_fig23_best_mask():
    # ISO/IEC 18004:2015(E) - 7.8.2 Data mask patterns
    # Figure 23
    matrix, width, height = read_matrix('fig-23-unmasked')
    mask, matrix = encoder.find_and_apply_best_mask(matrix, width, height)
    assert 0 == mask
    ref_matrix, ref_width, ref_height = read_matrix('fig-23-mask-0')
    assert ref_width, ref_height == (width, height)
    assert ref_matrix == matrix


def test_format_info_figure26():
    # 7.9.2 Micro QR Code symbols (page 57)
    version = consts.VERSION_M1
    width, height = 10, 10
    mask = 3
    matrix = tuple([bytearray([0x0] * 11) for i in range(11)])
    encoder.add_timing_pattern(matrix, is_micro=True)
    encoder.add_finder_patterns(matrix, width, height)
    encoder.add_format_info(matrix, version=version, error=None, mask_pattern=mask)
    ref_matrix = read_matrix('fig-26')[0]
    assert ref_matrix == matrix


if __name__ == '__main__':
    pytest.main([__file__])
