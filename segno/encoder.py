# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
QR Code and Micro QR Code encoder.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.
"""
from __future__ import absolute_import, division
from operator import itemgetter, gt, lt, xor
from functools import partial, reduce
import re
import math
import codecs
from collections import namedtuple
from . import consts
_PY2 = False
try:  # pragma: no cover
    from itertools import zip_longest
    str_type = str
    numeric = int
except ImportError:  # pragma: no cover
    _PY2 = True
    from itertools import izip_longest as zip_longest, imap as map
    str_type = basestring
    from numbers import Number
    numeric = Number
    str = unicode
    range = xrange

import sys
_MAX_PENALTY_SCORE = sys.maxsize
del sys

__all__ = ('encode', 'encode_sequence', 'QRCodeError', 'VersionError',
           'ModeError', 'ErrorLevelError', 'MaskError', 'DataOverflowError')

# <https://wiki.python.org/moin/PortingToPy3k/BilingualQuickRef#New_Style_Classes>
__metaclass__ = type


class QRCodeError(ValueError):
    """\
    Generic QR Code error.
    """


class VersionError(QRCodeError):
    """\
    Indicates errors related to the QR Code version.
    """


class ModeError(QRCodeError):
    """\
    Indicates errors related to QR Code mode.
    """


class ErrorLevelError(QRCodeError):
    """\
    Indicates errors related to QR Code error correction level.
    """


class MaskError(QRCodeError):
    """\
    Indicates errors related to QR Code data mask.
    """


class DataOverflowError(QRCodeError):
    """\
    Indicates a problem that the provided data does not fit into the
    provided QR Code version or the data is too large in general.
    """


Code = namedtuple('Code', 'matrix version error mask segments')


def encode(content, error=None, version=None, mode=None, mask=None,
           encoding=None, eci=False, micro=None, boost_error=True):
    """\
    Creates a (Micro) QR Code.

    See :py:func:`segno.make` for a detailed description of the parameters.

    Contrary to ``make`` this function returns a named tuple:
    ``(matrix, version, error, mask, segments)``

    Note that ``version`` is always an integer referring
    to the values of the :py:mod:`segno.consts` constants. ``error`` is ``None``
    iff a M1 QR Code was generated, otherwise it is always an integer.

    :rtype: namedtuple
    """
    version = normalize_version(version)
    if not micro and micro is not None and version in consts.MICRO_VERSIONS:
        raise VersionError('A Micro QR Code version ("{0}") is provided but '
                           'parameter "micro" is False'
                           .format(get_version_name(version)))
    if micro and version is not None and version not in consts.MICRO_VERSIONS:
        raise VersionError('Illegal Micro QR Code version "{0}"'
                           .format(get_version_name(version)))
    error = normalize_errorlevel(error, accept_none=True)
    mode = normalize_mode(mode)
    if mode is not None and version is not None \
            and not is_mode_supported(mode, version):
        raise ModeError('Mode "{0}" is not available in version "{1}"'
                        .format(get_mode_name(mode), get_version_name(version)))
    if error == consts.ERROR_LEVEL_H and (micro or version in consts.MICRO_VERSIONS):
        raise ErrorLevelError('Error correction level "H" is not available for '
                              'Micro QR Codes')
    if eci and (micro or version in consts.MICRO_VERSIONS):
        raise VersionError('The ECI mode is not available for Micro QR Codes')
    segments = prepare_data(content, mode, encoding, version)
    guessed_version = find_version(segments, error, eci=eci, micro=micro)
    if version is None:
        version = guessed_version
    elif guessed_version > version:
        raise DataOverflowError('The provided data does not fit into version '
                                '"{0}". Proposal: version {1}'
                                .format(get_version_name(version),
                                        get_version_name(guessed_version)))
    if error is None and version != consts.VERSION_M1:
        error = consts.ERROR_LEVEL_L
    is_micro = version < 1
    mask = normalize_mask(mask, is_micro)
    return _encode(segments, error, version, mask, eci, boost_error)


def encode_sequence(content, error=None, version=None, mode=None,
                    mask=None, encoding=None, eci=False, boost_error=True,
                    symbol_count=None):
    """\
    EXPERIMENTAL: Creates a sequence of QR Codes in Structured Append mode.

    :return: Iterable of named tuples, see :py:func:`encode` for details.
    """
    def one_item_segments(chunk, mode):
        """\
        Creates a Segments sequence with one item.
        """
        segs = Segments()
        segs.add_segment(make_segment(chunk, mode=mode, encoding=encoding))
        return segs

    def divide_into_chunks(data, num):
        k, m = divmod(len(data), num)
        return [data[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num)]

    def calc_qrcode_bit_length(char_count, ver_range, mode, encoding=None,
                               is_eci=False, is_sa=False):
        overhead = 4  # Mode indicator for QR Codes, only
        # Number of bits in character count indicator
        overhead += consts.CHAR_COUNT_INDICATOR_LENGTH[mode][ver_range]
        if is_eci and mode == consts.MODE_BYTE and encoding != consts.DEFAULT_BYTE_ENCODING:
            overhead += 4  # ECI indicator
            overhead += 8  # ECI assignment no
        if is_sa:
            # 4 bit for mode, 4 bit for the position, 4 bit for total number of symbols
            # 8 bit for parity data
            overhead += 5 * 4
        bits = 0
        if mode == consts.MODE_NUMERIC:
            num, remainder = divmod(char_count, 3)
            bits += num * 10 + (4 if remainder == 1 else 7)
        elif mode == consts.MODE_ALPHANUMERIC:
            num, remainder = divmod(char_count, 2)
            bits += num * 11 + (6 if remainder else 0)
        elif mode == consts.MODE_BYTE:
            bits += char_count * 8
        elif mode == consts.MODE_KANJI:
            bits += char_count * 13
        return overhead + bits

    def number_of_symbols_by_version(content, version, error, mode):
        """\
        Returns the number of symbols for the provided version.
        """
        length = len(content)
        ver_range = version_range(version)
        bit_length = calc_qrcode_bit_length(length, ver_range, mode, encoding,
                                            is_eci=eci, is_sa=True)
        capacity = consts.SYMBOL_CAPACITY[version][error]
        # Initial result does not contain the overhead of SA mode for all QR Codes
        cnt = int(math.ceil(bit_length / capacity))
        # Overhead of SA mode for all QR Codes
        bit_length += 5 * 4 * (cnt - 1) + (12 * (cnt - 1) if eci else 0)
        return int(math.ceil(bit_length / capacity))

    version = normalize_version(version)
    if version is not None:
        if version < 1:
            raise VersionError('This function does not accept Micro QR Code versions. '
                               'Provided: "{0}"'.format(get_version_name(version)))
    elif symbol_count is None:
        raise ValueError('Please provide a QR Code version or the symbol count')
    if symbol_count is not None and not 1 <= symbol_count <= 16:
        raise ValueError('The symbol count must be in range 1 .. 16')
    error = normalize_errorlevel(error, accept_none=True)
    if error is None:
        error = consts.ERROR_LEVEL_L
    mode = normalize_mode(mode)
    mask = normalize_mask(mask, is_micro=False)
    segments = prepare_data(content, mode, encoding, version)
    guessed_version = None
    if symbol_count is None:
        try:
            # Try to find a version which fits without using Structured Append
            guessed_version = find_version(segments, error, eci=eci, micro=False)
        except DataOverflowError:
            # Data does fit into a usual QR Code but ignore the error silently,
            # guessed_version is None
            pass
        if guessed_version and guessed_version <= (version or guessed_version):
            # Return iterable of size 1
            return [_encode(segments, error=error, version=(version or guessed_version),
                            mask=mask, eci=eci, boost_error=boost_error)]
    if len(segments.modes) > 1:
        raise ValueError('This function cannot handle more than one mode (yet). Sorry.')
    mode = segments.modes[0]  # CHANGE iff more than one mode is supported!
    # Creating one QR code failed or max_no is not None
    if mode == consts.MODE_NUMERIC:
        content = str(content)
    if symbol_count is not None and len(content) < symbol_count:
        raise ValueError('The content is not long enough to be divided into {0} symbols'.format(symbol_count))
    sa_parity_data = calc_structured_append_parity(content)
    num_symbols = symbol_count or 16
    if version is not None:
        num_symbols = number_of_symbols_by_version(content, version, error, mode)
    if num_symbols > 16:
        raise DataOverflowError('The data does not fit into Structured Append version {0}'.format(version))
    chunks = divide_into_chunks(content, num_symbols)
    if symbol_count is not None:
        segments = one_item_segments(max(chunks, key=len), mode)
        version = find_version(segments, error, eci=eci, micro=False, is_sa=True)
    sa_info = partial(_StructuredAppendInfo, total=len(chunks) - 1,
                      parity=sa_parity_data)
    return [_encode(one_item_segments(chunk, mode), error=error, version=version,
                    mask=mask, eci=eci, boost_error=boost_error,
                    sa_info=sa_info(i)) for i, chunk in enumerate(chunks)]


def _encode(segments, error, version, mask, eci, boost_error, sa_info=None):
    """\
    Creates a (Micro) QR Code.

    NOTE: This function does not check if the input is valid and does not belong
    to the public API.
    """
    is_micro = version < 1
    sa_mode = sa_info is not None
    buff = Buffer()
    ver = version
    ver_range = version
    if not is_micro:
        ver = None
        ver_range = version_range(version)
    if boost_error:
        error = boost_error_level(version, error, segments, eci, is_sa=sa_mode)
    if sa_mode:
        # ISO/IEC 18004:2015(E) -- 8 Structured Append (page 59)
        for i in sa_info[:3]:
            buff.append_bits(i, 4)
        buff.append_bits(sa_info.parity, 8)
    # ISO/IEC 18004:2015(E) -- 7.4 Data encoding (page 22)
    for segment in segments:
        write_segment(buff, segment, ver, ver_range, eci)
    capacity = consts.SYMBOL_CAPACITY[version][error]
    # ISO/IEC 18004:2015(E) -- 7.4.9 Terminator (page 32)
    write_terminator(buff, capacity, ver, len(buff))
    #  ISO/IEC 18004:2015(E) -- 7.4.10 Bit stream to codeword conversion (page 34)
    write_padding_bits(buff, version, len(buff))
    # ISO/IEC 18004:2015(E) -- 7.4.10 Bit stream to codeword conversion (page 34)
    write_pad_codewords(buff, version, capacity, len(buff))
    # ISO/IEC 18004:2015(E) -- 7.6 Constructing the final message codeword sequence (page 45)
    buff = make_final_message(version, error, buff.toints())
    # Matrix with timing pattern and reserved format / version regions
    matrix = make_matrix(version)
    # ISO/IEC 18004:2015 -- 6.3.3 Finder pattern (page 16)
    add_finder_patterns(matrix, is_micro)
    # ISO/IEC 18004:2015 -- 6.3.6 Alignment patterns (page 17)
    add_alignment_patterns(matrix, version)
    # ISO/IEC 18004:2015 -- 7.7 Codeword placement in matrix (page 46)
    add_codewords(matrix, buff, version)
    # ISO/IEC 18004:2015(E) -- 7.8.2 Data mask patterns (page 50)
    # ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results (page 53)
    mask = find_and_apply_best_mask(matrix, version, is_micro, mask)
    # ISO/IEC 18004:2015(E) -- 7.9 Format information (page 55)
    add_format_info(matrix, version, error, mask)
    # ISO/IEC 18004:2015(E) -- 7.10 Version information (page 58)
    add_version_info(matrix, version)
    return Code(matrix, version, error, mask, segments)


def boost_error_level(version, error, segments, eci, is_sa=False):
    """\
    Increases the error level if possible.

    :param int version: Version constant.
    :param int|None error: Error level constant or ``None``
    :param Segments segments: Instance of :py:class:`Segments`
    :param bool eci: Indicates if ECI designator should be written.
    :param bool is_sa: Indicates if Structured Append mode ist used.
    """
    if error not in (consts.ERROR_LEVEL_H, None) and len(segments) == 1:
        levels = [consts.ERROR_LEVEL_L, consts.ERROR_LEVEL_M,
                  consts.ERROR_LEVEL_Q, consts.ERROR_LEVEL_H]
        if version < 1:
            levels.pop()  # H isn't support by Micro QR Codes
            if version < consts.VERSION_M4:
                levels.pop()  # Error level Q isn't supported by M2 and M3
        data_length = segments.bit_length_with_overhead(version, eci, is_sa=is_sa)
        for level in levels[levels.index(error)+1:]:
            try:
                found = consts.SYMBOL_CAPACITY[version][level] >= data_length
            except KeyError:
                break
            if found:
                error = level
    return error


def write_segment(buff, segment, ver, ver_range, eci=False):
    """\
    Writes a segment.

    :param buff: The byte buffer.
    :param _Segment segment: The segment to serialize.
    :param ver: ``None`` if a QR Code is written, "M1", "M2", "M3", or "M4" if a
            Micro QR Code is written.
    :param ver_range: "M1", "M2", "M3", or "M4" if a Micro QR Code is written,
            otherwise a constant representing a range of QR Code versions.
    """
    mode = segment.mode
    append_bits = buff.append_bits
    # Write ECI header if requested
    if eci and mode == consts.MODE_BYTE \
            and segment.encoding != consts.DEFAULT_BYTE_ENCODING:
        append_bits(consts.MODE_ECI, 4)
        append_bits(get_eci_assignment_number(segment.encoding), 8)
    if ver is None:  # QR Code
        append_bits(mode, 4)
    elif ver > consts.VERSION_M1:  # Micro QR Code (M1 has no mode indicator)
        append_bits(consts.MODE_TO_MICRO_MODE_MAPPING[mode], ver + 3)
    # Character count indicator
    append_bits(segment.char_count,
                consts.CHAR_COUNT_INDICATOR_LENGTH[mode][ver_range])
    buff.extend(segment.bits)


def write_terminator(buff, capacity, ver, length):
    """\
    Writes the terminator.

    :param buff: The byte buffer.
    :param capacity: Symbol capacity.
    :param ver: ``None`` if a QR Code is written, "M1", "M2", "M3", or "M4" if a
            Micro QR Code is written.
    :param length: Length of the data bit stream.
    """
    # ISO/IEC 18004:2015 -- 7.4.9 Terminator (page 32)
    buff.extend([0] * min(capacity - length, consts.TERMINATOR_LENGTH[ver]))


def write_padding_bits(buff, version, length):
    """\
    Writes padding bits if the data stream does not meet the codeword boundary.

    :param buff: The byte buffer.
    :param int length: Data stream length.
    """
    # ISO/IEC 18004:2015(E) - 7.4.10 Bit stream to codeword conversion -- page 32
    # [...]
    # All codewords are 8 bits in length, except for the final data symbol
    # character in Micro QR Code versions M1 and M3 symbols, which is 4 bits
    # in length. If the bit stream length is such that it does not end at a
    # codeword boundary, padding bits with binary value 0 shall be added after
    # the final bit (least significant bit) of the data stream to extend it
    # to the codeword boundary. [...]
    if version not in (consts.VERSION_M1, consts.VERSION_M3):
        buff.extend([0] * (8 - (length % 8)))


def write_pad_codewords(buff, version, capacity, length):
    """\
    Writes the pad codewords iff the data does not fill the capacity of the
    symbol.

    :param buff: The byte buffer.
    :param int version: The (Micro) QR Code version.
    :param int capacity: The total capacity of the symbol (incl. error correction)
    :param int length: Length of the data bit stream.
    """
    # ISO/IEC 18004:2015(E) -- 7.4.10 Bit stream to codeword conversion (page 32)
    # The message bit stream shall then be extended to fill the data capacity
    # of the symbol corresponding to the Version and Error Correction Level, as
    # defined in Table 8, by adding the Pad Codewords 11101100 and 00010001
    # alternately. For Micro QR Code versions M1 and M3 symbols, the final data
    # codeword is 4 bits long. The Pad Codeword used in the final data symbol
    # character position in Micro QR Code versions M1 and M3 symbols shall be
    # represented as 0000.
    write = buff.extend
    if version in (consts.VERSION_M1, consts.VERSION_M3):
        write([0] * (capacity - length))
    else:
        pad_codewords = ((1, 1, 1, 0, 1, 1, 0, 0), (0, 0, 0, 1, 0, 0, 0, 1))
        for i in range(capacity // 8 - length // 8):
            write(pad_codewords[i % 2])


def add_finder_patterns(matrix, is_micro):
    """\
    Adds the finder pattern(s) to the matrix.

    QR Codes get three finder patterns, Micro QR Codes have just one finder
    pattern.

    ISO/IEC 18004:2015(E) -- 6.3.3 Finder pattern (page 16)
    ISO/IEC 18004:2015(E) -- 6.3.4 Separator (page 17)

    :param matrix: The matrix.
    :param bool is_micro: Indicates if the matrix represents a Micro QR Code.
    """
    add_finder_pattern(matrix, 0, 0)  # Upper left corner
    if not is_micro:
        add_finder_pattern(matrix, 0, -7)  # Upper right corner
        add_finder_pattern(matrix, -7, 0)  # Bottom left corner


# Finder pattern (includes separator around each side!)
_FINDER_PATTERN = ((0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0),
                   (0x0, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x0),
                   (0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0),
                   (0x0, 0x1, 0x0, 0x1, 0x1, 0x1, 0x0, 0x1, 0x0),
                   (0x0, 0x1, 0x0, 0x1, 0x1, 0x1, 0x0, 0x1, 0x0),
                   (0x0, 0x1, 0x0, 0x1, 0x1, 0x1, 0x0, 0x1, 0x0),
                   (0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0),
                   (0x0, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x0),
                   (0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0))

def add_finder_pattern(matrix, x, y):
    """\
    Adds the finder pattern (black rect with black square) and
    the finder separator (white horizontal line and white vertical line) to the
    provided `matrix`.

    ISO/IEC 18004:2015(E) -- 6.3.3 Finder pattern (page 16)
    ISO/IEC 18004:2015(E) -- 6.3.4 Separator (page 17)

    :param matrix: Matrix to add the finder into.
    :param x: x-index of the first *black* module (upper left corner)
    :param y: y-index of the first *black* module (upper left corner)
    """
    fidx1, fidx2 = (0, 8) if y != 0 else (1, 9)
    fyoff = 1 if x == 0 else 0
    idx1, idx2 = (0, 8) if y > -1 else (y - 1, len(matrix))
    x -= fyoff ^ 0x1
    for i in range(8):
        matrix[x + i][idx1:idx2] = _FINDER_PATTERN[fyoff + i][fidx1:fidx2]


def add_timing_pattern(matrix, is_micro):
    """\
    Adds the (horizontal and vertical) timinig pattern to the provided `matrix`.

    ISO/IEC 18004:2015(E) -- 6.3.5 Timing pattern (page 17)

    :param matrix: Matrix to add the timing pattern into.
    :param bool is_micro: Indicates if the timing pattern for a Micro QR Code
        should be added.
    """
    bit = 0x1
    y, stop = (0, len(matrix)) if is_micro else (6, len(matrix) - 8)
    for x in range(8, stop):
        matrix[x][y] = bit
        matrix[y][x] = bit
        bit ^= 0x1


_ALIGNMENT_PATTERN = ((0x1, 0x1, 0x1, 0x1, 0x1),
                      (0x1, 0x0, 0x0, 0x0, 0x1),
                      (0x1, 0x0, 0x1, 0x0, 0x1),
                      (0x1, 0x0, 0x0, 0x0, 0x1),
                      (0x1, 0x1, 0x1, 0x1, 0x1))

def add_alignment_patterns(matrix, version):
    """\
    Adds the adjustment patterns to the matrix. For versions < 2 this is a
    no-op.

    ISO/IEC 18004:2015(E) -- 6.3.6 Alignment patterns (page 17)
    ISO/IEC 18004:2015(E) -- Annex E Position of alignment patterns (page 83)
    """
    if version < 2:
        return
    matrix_size = len(matrix)
    positions = consts.ALIGNMENT_POS[version - 2]
    for pos_x in positions:
        for pos_y in positions:
            # Finder pattern?
            if pos_x - 6 == 0 and (pos_y - 6 == 0 or pos_y + 7 == matrix_size) \
                    or pos_y - 6 == 0 and pos_x + 7 == matrix_size:
                continue
            row, col = pos_x - 2, pos_y - 2
            for r in range(5):
                matrix[row + r][col:col+5] = _ALIGNMENT_PATTERN[r]


def add_codewords(matrix, codewords, version):
    """\
    Adds the codewords (data and error correction) to the provided matrix.

    ISO/IEC 18004:2015(E) -- 7.7.3 Symbol character placement (page 46)

    :param matrix: The matrix to add the codewords into.
    :param codewords: Sequence of ints
    """
    matrix_size = len(matrix)
    is_micro = version < 1
    # Necessary for M1 and M3: The algorithm would start at the upper right
    # corner, see <https://github.com/heuer/segno/issues/36>
    inc = 0 if version not in (consts.VERSION_M1, consts.VERSION_M3) else 2
    idx = 0  # Pointer to the current codeword
    # ISO/IEC 18004:2015(E) - page 48
    # [...] An alternative method for placement in the symbol [...] is to regard
    # the interleaved codeword sequence as a single bit stream, which is placed
    # (starting with the most significant bit) in the two-module wide columns
    # alternately upwards and downwards from the right to left of the symbol.
    # [...]
    for right in range(matrix_size - 1, 0, -2):
        if not is_micro and right <= 6:
            right -= 1
        for vertical in range(matrix_size):
            for z in range(2):
                j = right - z
                upwards = ((right + inc) & 2) == 0
                if not is_micro:
                    upwards ^= j < 6
                i = (matrix_size - 1 - vertical) if upwards else vertical
                if matrix[i][j] == 0x2 and idx < len(codewords):
                    matrix[i][j] = codewords[idx]
                    idx += 1
    if idx != len(codewords):  # pragma: no cover
        raise QRCodeError('Internal error: Adding codewords to matrix failed. '
                          'Added {0} of {1} codewords'.format(idx, len(codewords)))


def make_final_message(version, error, codewords):
    """\
    Constructs the final message (codewords incl. error correction).

    ISO/IEC 18004:2015(E) -- 7.6 Constructing the final message codeword sequence (page 45)

    :param int version: (Micro) QR Code version constant.
    :param int error: Error level constant.
    :param codewords: An iterable sequence of codewords (ints)
    :return: Byte buffer representing the final message.
    """
    ec_infos = consts.ECC[version][error]
    last_cw_is_four = version in (consts.VERSION_M1, consts.VERSION_M3)
    data_blocks, error_blocks = make_blocks(ec_infos, codewords)
    if last_cw_is_four:
        # All codewords are 8 bit by default, M1 and M3 symbols use 4 bits
        # to represent the last last codeword
        # datablocks[0] is save since Micro QR Codes use just one datablock and
        # one error block
        data_blocks[0][-1] >>= 4
    buff = Buffer()
    append_int = partial(buff.append_bits, length=8)
    # Write codewords
    for i in range(max(info.num_data for info in ec_infos)):
        for block in data_blocks:
            if i >= len(block):
                continue
            if last_cw_is_four and i + 1 == len(block):
                buff.append_bits(block[i], 4)
            else:
                append_int(block[i])
    # Write error codewords
    for i in range(max(info.num_total - info.num_data for info in ec_infos)):
        for block in error_blocks:
            if i >= len(block):
                continue
            append_int(block[i])
    # ISO/IEC 18004:2015(E) -- 7.6 Constructing the final message codeword sequence
    # [...] In certain QR Code versions, however, where the number of modules
    # available for data and error correction codewords is not an exact multiple
    # of 8, there may be a need for 3, 4 or 7 Remainder Bits to be appended to
    # the final message bit stream in order to fill exactly the number of
    # modules in the encoding region
    remainder = 0  # Calculation: Number of Data modules - number of bits
    if version in (2, 3, 4, 5, 6):
        remainder = 7
    elif version in (14, 15, 16, 17, 18, 19, 20, 28, 29, 30, 31, 32, 33, 34):
        remainder = 3
    elif version in (21, 22, 23, 24, 25, 26, 27):
        remainder = 4
    buff.extend(b'\0' * remainder)
    return buff


def make_blocks(ec_infos, codewords):
    """\
    Returns the data and error blocks.

    :param ec_infos: Iterable of ECC information
    :param codewords: Iterable of (integer) code words.
    """
    data_blocks, error_blocks = [], []
    offset = 0
    for ec_info in ec_infos:
        for i in range(ec_info.num_blocks):
            block = codewords[offset:offset + ec_info.num_data]
            data_blocks.append(block)
            error_blocks.append(make_error_block(ec_info, block))
            offset += ec_info.num_data
    return data_blocks, error_blocks


def make_error_block(ec_info, data_block):
    """\
    Creates the error code words for the provided data block.

    :param ec_info: ECC information (number of blocks, number of code words etc.)
    :param data_block: Iterable of (integer) code words.
    """
    num_error_words = ec_info.num_total - ec_info.num_data

    error_block = bytearray(data_block)
    error_block.extend([0] * num_error_words)

    gen = consts.GEN_POLY[num_error_words]
    gen_log = consts.GALIOS_LOG
    gen_exp = consts.GALIOS_EXP
    len_data = len(data_block)

    # Extended synthetic division, see http://research.swtch.com/field
    for i in range(len_data):
        coef = error_block[i]
        if coef != 0:  # log(0) is undefined
            lcoef = gen_log[coef]
            for j in range(num_error_words):
                error_block[i + j + 1] ^= gen_exp[lcoef + gen[j]]
    return error_block[len_data:]


def find_and_apply_best_mask(matrix, version, is_micro, proposed_mask=None):
    """\
    Applies all mask patterns against the provided QR Code matrix and returns
    the best matrix and best pattern.

    ISO/IEC 18004:2015(E) -- 7.8.2 Data mask patterns (page 50)
    ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results (page 53)
    ISO/IEC 18004:2015(E) -- 7.8.3.1 Evaluation of QR Code symbols (page 53/54)
    ISO/IEC 18004:2015(E) -- 7.8.3.2 Evaluation of Micro QR Code symbols (page 54/55)

    :param matrix: A matrix.
    :param int version: A version (Micro) QR Code version constant.
    :param bool is_micro: Indicates if the matrix represents a Micro QR Code
    :param proposed_mask: Optional int to indicate the preferred mask.
    :rtype: tuple
    :return: A tuple of the best matrix and best data mask pattern index.
    """
    matrix_size = len(matrix)
    # ISO/IEC 18004:2015 -- 7.8.3.1 Evaluation of QR Code symbols (page 53/54)
    # The data mask pattern which results in the lowest penalty score shall
    # be selected for the symbol.
    is_better = lt
    best_score = _MAX_PENALTY_SCORE
    eval_mask = evaluate_mask
    if is_micro:
        # ISO/IEC 18004:2015(E) - 7.8.3.2 Evaluation of Micro QR Code symbols (page 54/55)
        # The data mask pattern which results in the highest score shall be
        # selected for the symbol.
        is_better = gt
        best_score = -1
        eval_mask = evaluate_micro_mask
    # Matrix to check if a module belongs to the encoding region
    # or function patterns
    function_matrix = make_matrix(version)
    add_finder_patterns(function_matrix, is_micro)
    add_alignment_patterns(function_matrix, version)
    if not is_micro:
        function_matrix[-8][8] = 0x1

    def is_encoding_region(i, j):
        return function_matrix[i][j] == 0x2

    mask_patterns = get_data_mask_functions(is_micro)

    # If the user supplied a mask pattern, the evaluation step is skipped
    if proposed_mask is not None:
        apply_mask(matrix, mask_patterns[proposed_mask], matrix_size,
                   is_encoding_region)
        return proposed_mask

    for mask_number, mask_pattern in enumerate(mask_patterns):
        apply_mask(matrix, mask_pattern, matrix_size, is_encoding_region)
        # NOTE: DO NOT add format / version info in advance of evaluation
        # See ISO/IEC 18004:2015(E) -- 7.8. Data masking (page 50)
        score = eval_mask(matrix, matrix_size)
        if is_better(score, best_score):
            best_score = score
            best_pattern = mask_number
        # Undo mask
        apply_mask(matrix, mask_pattern, matrix_size, is_encoding_region)
    apply_mask(matrix, mask_patterns[best_pattern], matrix_size, is_encoding_region)
    return best_pattern


def apply_mask(matrix, mask_pattern, matrix_size, is_encoding_region):
    """\
    Applies the provided mask pattern on the `matrix`.

    ISO/IEC 18004:2015(E) -- 7.8.2 Data mask patterns (page 50)

    :param tuple matrix: A tuple of bytearrays
    :param mask_pattern: A mask pattern (a function)
    :param int matrix_size: width or height of the matrix
    :param is_encoding_region: A function which returns ``True`` iff the
            row index / col index belongs to the data region.
    """
    for i in range(matrix_size):
        for j in range(matrix_size):
            if is_encoding_region(i, j):
                matrix[i][j] ^= mask_pattern(i, j)


def evaluate_mask(matrix, matrix_size):
    """\
    Evaluates the provided `matrix` of a QR code.

    ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results (page 53)

    :param matrix: The matrix to evaluate
    :param matrix_size: The width (or height) of the matrix.
    :return int: The penalty score of the matrix.
    """
    return score_n1(matrix, matrix_size) + score_n2(matrix, matrix_size) \
           + score_n3(matrix, matrix_size) + score_n4(matrix, matrix_size)


def score_n1(matrix, matrix_size):
    """\
    Implements the penalty score feature 1.

    ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results - Table 11 (page 54)

    ============================================   ========================    ======
    Feature                                        Evaluation condition        Points
    ============================================   ========================    ======
    Adjacent modules in row/column in same color   No. of modules = (5 + i)    N1 + i
    ============================================   ========================    ======

    N1 = 3

    :param matrix: The matrix to evaluate
    :param matrix_size: The width (or height) of the matrix.
    :return int: The penalty score (feature 1) of the matrix.
    """
    score = 0
    for i in range(matrix_size):
        prev_bit_row, prev_bit_col = -1, -1
        row_counter, col_counter = 0, 0
        for j in range(matrix_size):
            # Row-wise
            bit = matrix[i][j]
            if bit == prev_bit_row:
                row_counter += 1
            else:
                if row_counter >= 5:
                    score += row_counter - 2  # N1 == 3
                row_counter = 1
                prev_bit_row = bit
            # Col-wise
            bit = matrix[j][i]
            if bit == prev_bit_col:
                col_counter += 1
            else:
                if col_counter >= 5:
                    score += col_counter - 2  # N1 == 3
                col_counter = 1
                prev_bit_col = bit
        if row_counter >= 5:
            score += row_counter - 2  # N1 == 3
        if col_counter >= 5:
            score += col_counter - 2  # N1 == 3
    return score


def score_n2(matrix, matrix_size):
    """\
    Implements the penalty score feature 2.

    ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results - Table 11 (page 54)

    ==============================   ====================   ===============
    Feature                          Evaluation condition   Points
    ==============================   ====================   ===============
    Block of modules in same color   Block size = m × n     N2 ×(m-1)×(n-1)
    ==============================   ====================   ===============

    N2 = 3

    :param matrix: The matrix to evaluate
    :param matrix_size: The width (or height) of the matrix.
    :return int: The penalty score (feature 2) of the matrix.
    """
    score = 0
    for i in range(matrix_size - 1):
        for j in range(matrix_size - 1):
            bit = matrix[i][j]
            if bit == matrix[i][j + 1] and bit == matrix[i + 1][j] \
                and bit == matrix[i + 1][j + 1]:
                score += 1
    return score * 3  # N2 == 3


_N3_PATTERN = bytearray((0x1, 0x0, 0x1, 0x1, 0x1, 0x0, 0x1))
def score_n3(matrix, matrix_size):
    """\
    Implements the penalty score feature 3.

    ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results - Table 11 (page 54)

    =========================================   ========================   ======
    Feature                                     Evaluation condition       Points
    =========================================   ========================   ======
    1 : 1 : 3 : 1 : 1 ratio                     Existence of the pattern   N3
    (dark:light:dark:light:dark) pattern in
    row/column, preceded or followed by light
    area 4 modules wide
    =========================================   ========================   ======

    N3 = 40

    :param matrix: The matrix to evaluate
    :param matrix_size: The width (or height) of the matrix.
    :return int: The penalty score (feature 3) of the matrix.
    """
    def is_match(seq, start, end):
        start = max(start, 0)
        end = min(end, matrix_size)
        for i in range(start, end):
            if seq[i] == 0x1:
                return False
        return True

    def find_occurrences(seq):
        count = 0
        idx = seq.find(_N3_PATTERN)
        while idx != -1:
            offset = idx + 7
            if is_match(seq, idx - 4, idx) or is_match(seq, offset, offset + 4):
                count += 1
            else:
                # Found no / not enough light patterns, start at next possible
                # match:
                #                   v
                # dark light dark dark dark light dark
                #                   ^
                offset = idx + 4
            idx = seq.find(_N3_PATTERN, offset)
        return count

    score = 0
    for i in range(matrix_size):
        score += find_occurrences(matrix[i])
        score += find_occurrences(bytearray([matrix[y][i] for y in range(matrix_size)]))
    return score * 40  # N3 = 40


def score_n4(matrix, matrix_size):
    """\
    Implements the penalty score feature 4.

    ISO/IEC 18004:2015(E) -- 7.8.3 Evaluation of data masking results - Table 11 (page 54)

    ===========================================   ====================================   ======
    Feature                                       Evaluation condition                   Points
    ===========================================   ====================================   ======
    Proportion of dark modules in entire symbol   50 × (5 × k)% to 50 × (5 × (k + 1))%   N4 × k
    ===========================================   ====================================   ======

    N4 = 10

    :param matrix: The matrix to evaluate
    :param matrix_size: The width (or height) of the matrix.
    :return int: The penalty score (feature 4) of the matrix.
    """
    dark_modules = sum(map(sum, matrix))
    total_modules = matrix_size ** 2
    k = int(abs(dark_modules * 2 - total_modules) * 10 // total_modules)
    return 10 * k  # N4 = 10


def evaluate_micro_mask(matrix, matrix_size):
    """\
    Evaluates the provided `matrix` of a Micro QR code.

    ISO/IEC 18004:2015(E) -- 7.8.3.2 Evaluation of Micro QR Code symbols (page 54)

    :param matrix: The matrix to evaluate
    :param matrix_size: The width (or height) of the matrix.
    :return int: The penalty score of the matrix.
    """
    sum1 = sum(matrix[i][-1] == 0x1 for i in range(1, matrix_size))
    sum2 = sum(matrix[-1][i] == 0x1 for i in range(1, matrix_size))
    return sum1 * 16 + sum2 if sum1 <= sum2 else sum2 * 16 + sum1


def calc_format_info(version, error, mask_pattern):
    """\
    Returns the format information for the provided error level and mask patttern.

    ISO/IEC 18004:2015(E) -- 7.9 Format information (page 55)
    ISO/IEC 18004:2015(E) -- Table C.1 — Valid format information bit sequences (page 80)

    :param int version: Version constant
    :param int error: Error level constant.
    :param int mask_pattern: Mask pattern number.
    """
    fmt = mask_pattern
    if version > 0:
        if error == consts.ERROR_LEVEL_L:
            fmt += 0x08
        elif error == consts.ERROR_LEVEL_H:
            fmt += 0x10
        elif error == consts.ERROR_LEVEL_Q:
            fmt += 0x18
        format_info = consts.FORMAT_INFO[fmt]
    else:
        fmt += consts.ERROR_LEVEL_TO_MICRO_MAPPING[version][error] << 2
        format_info = consts.FORMAT_INFO_MICRO[fmt]
    return format_info


def add_format_info(matrix, version, error, mask_pattern):
    """\
    Adds the format information into the provided matrix.

    ISO/IEC 18004:2015(E) -- 7.9 Format information (page 55)
    ISO/IEC 18004:2015(E) -- 7.9.1 QR Code symbols
    ISO/IEC 18004:2015(E) -- 7.9.2 Micro QR Code symbols

    :param matrix: The matrix.
    :param int version: Version constant
    :param int error: Error level constant.
    :param int mask_pattern: Mask pattern number.
    """
    # 14: most significant bit
    #  0: least significant bit
    #
    # QR Code format info:                                          Micro QR format info
    # col 0                col 7              col matrix[-1]      col 1
    #                        0                       |               |                [ ]
    #                        1                                                         0
    #                        2                                                         1
    #                        3                                                         2
    #                        4                                                         3
    #                        5                                                         4
    #                       [ ]                                                        5
    #                        6                                                         6
    # 14 13 12 11 10 9 [ ] 8 7    ...  7 6 5 4 3 2 1 0              14 13 12 11 10 9 8 7
    #
    # ...
    #                       [ ] (dark module)
    #                        8
    #                        9
    #                       10
    #                       11
    #                       12
    #                       13
    #                       14
    is_micro = version < 1
    format_info = calc_format_info(version, error, mask_pattern)
    offset = int(is_micro)
    for i in range(8):
        bit = (format_info >> i) & 0x01
        if i == 6 and not is_micro:  # Timing pattern
            offset += 1
        # vertical row, upper left corner
        matrix[i + offset][8] = bit
        if not is_micro:
            # horizontal row, upper right corner
            matrix[8][-1 - i] = bit
    offset = int(is_micro)
    for i in range(8):
        bit = (format_info >> (14 - i)) & 0x01
        if i == 6 and not is_micro:  # Timing pattern
            offset = 1
        # horizontal row, upper left corner
        matrix[8][i + offset] = bit
        if not is_micro:
            # vertical row, bottom left corner
            matrix[-1 - i][8] = bit
    if not is_micro:
        # Dark module
        matrix[-8][8] = 0x1


def add_version_info(matrix, version):
    """\
    Adds the version information to the matrix, for versions < 7 this is a no-op.

    ISO/IEC 18004:2015(E) -- 7.10 Version information (page 58)
    """
    #
    # module  0 = least significant bit
    # module 17 = most significant bit
    #
    # Figure 27 — Version information positioning (page 58)
    #
    # Lower left                    Upper right
    # ----------                    -----------
    #  0  3  6  9 12 15               0  1  2
    #  1  4  7 10 13 16               3  4  5
    #  2  5  8 11 14 17               6  7  8
    #                                 9 10 11
    #                                12 13 14
    #                                15 16 17
    #
    if version < 7:
        return
    version_info = consts.VERSION_INFO[version - 7]
    for i in range(6):
        bit1 = (version_info >> (i * 3)) & 0x01
        bit2 = (version_info >> ((i * 3) + 1)) & 0x01
        bit3 = (version_info >> ((i * 3) + 2)) & 0x01
        # Lower left
        matrix[-11][i] = bit1
        matrix[-10][i] = bit2
        matrix[-9][i] = bit3
        # Upper right
        matrix[i][-11] = bit1
        matrix[i][-10] = bit2
        matrix[i][-9] = bit3


def prepare_data(content, mode, encoding, version=None):
    """\
    Returns an iterable of `Segment` instances.

    If `content` is a string, an integer, or bytes, the returned tuple will
    have a single item. If `content` is a list or a tuple, a tuple of
    `Segment` instances of the same length is returned.

    :param content: Either a string, bytes, an integer or an iterable.
    :type content: str, bytes, int, tuple, list or any iterable
    :param mode: The global mode. If `content` is list/tuple, the `Segment`
            instances may have a different mode.
    :param encoding: The global encoding. If `content` is a list or a tuple,
            the `Segment` instances may have a different encoding.
    :param int version: Version constant or ``None``. This refers to the version
                which was provided by the user.
    :rtype: Segments
    """
    segments = Segments()
    add_segment = segments.add_segment
    if isinstance(content, (str_type, bytes, numeric)):
        add_segment(make_segment(content, mode, encoding))
        return segments
    for item in content:
        seg_content, seg_mode, seg_encoding = item, mode, encoding
        if isinstance(item, tuple):
            seg_content = item[0]
            if len(item) > 1:
                seg_mode = item[1] or mode  # item[1] could be None
            if len(item) > 2:
                seg_encoding = item[2] or encoding # item[2] may be None
        add_segment(make_segment(seg_content, seg_mode, seg_encoding))
    return segments


def data_to_bytes(data, encoding):
    """\
    Converts the provided data into bytes. If the data is already a byte
    sequence, it will be left unchanged.

    This function tries to use the provided `encoding` (if not ``None``)
    or the default encoding (ISO/IEC 8859-1). It uses UTF-8 as fallback.

    Returns the (byte) data, the data length and the encoding of the data.

    :param data: The data to encode
    :type data: str or bytes
    :param encoding: str or ``None``
    :rtype: tuple: data, data length, encoding
    """
    if isinstance(data, bytes):
        return data, len(data), encoding or consts.DEFAULT_BYTE_ENCODING
    data = str(data)
    if encoding is not None:
        # Use the provided encoding; could raise an exception by intention
        data = data.encode(encoding)
    else:
        try:
            # Try to use the default byte encoding
            encoding = consts.DEFAULT_BYTE_ENCODING
            data = data.encode(encoding)
        except UnicodeError:
            try:
                # Try Kanji / Shift_JIS
                encoding = consts.KANJI_ENCODING
                data = data.encode(encoding)
            except UnicodeError:
                # Use UTF-8
                encoding = 'utf-8'
                data = data.encode(encoding)
    return data, len(data), encoding


def make_segment(data, mode, encoding=None):
    """\
    Creates a :py:class:`Segment`.

    :param data: The segment data
    :param mode: The mode.
    :param encoding: The encoding.
    :rtype: _Segment
    """
    segment_data, segment_length, segment_encoding = data_to_bytes(data, encoding)
    segment_mode = mode
    # If the user prefers BYTE, use BYTE and do not try to find a better mode
    # Necessary since BYTE < KANJI and find_mode may return KANJI as (more)
    # appropriate mode and the encoder throws an exception
    # if "user provided mode" < "found mode"
    guessed_mode = find_mode(segment_data) if segment_mode != consts.MODE_BYTE else consts.MODE_BYTE
    if segment_mode is not None:
        # Check if user provided mode is applicable for the given segment_data
        if segment_mode < guessed_mode:
            raise ModeError('The provided mode "{0}" is not applicable '
                            'for {1}. Proposal: {2}'
                            .format(get_mode_name(segment_mode),
                                    repr(segment_data),
                                    get_mode_name(guessed_mode)))
    else:
        segment_mode = guessed_mode
    if segment_mode != consts.MODE_BYTE:
        segment_encoding = None
    buff = Buffer()
    append_bits = buff.append_bits
    if segment_mode == consts.MODE_NUMERIC:
        # ISO/IEC 18004:2015(E) -- 7.4.3 Numeric mode (page 25)
        # The input data string is divided into groups of three digits, and
        # each group is converted to its 10-bit binary equivalent. If the number
        # of input digits is not an exact multiple of three, the final one or
        # two digits are converted to 4 or 7 bits respectively.
        for i in range(0, segment_length, 3):
            chunk = segment_data[i:i + 3]
            append_bits(int(chunk), len(chunk) * 3 + 1)
    elif segment_mode == consts.MODE_ALPHANUMERIC:
        # ISO/IEC 18004:2015(E) -- 7.4.4 Alphanumeric mode (page 26)
        to_byte = consts.ALPHANUMERIC_CHARS.find
        for i in range(0, segment_length, 2):
            chunk = segment_data[i:i + 2]
            # Input data characters are divided into groups of two characters
            # which are encoded as 11-bit binary codes. The character value of
            # the first character is multiplied by 45 and the character value
            # of the second digit is added to the product. The sum is then
            # converted to an 11-bit binary number.
            if len(chunk) > 1:
                append_bits(to_byte(chunk[0]) * 45 + to_byte(chunk[1]), 11)
            else:
                # If the number of input data characters is not a multiple of
                # two, the character value of the final character is encoded
                # as a 6-bit binary number.
                append_bits(to_byte(chunk), 6)
    elif segment_mode == consts.MODE_BYTE:
        # ISO/IEC 18004:2015(E) -- 7.4.5 Byte mode (page 27)
        if _PY2:
            segment_data = (ord(b) for b in segment_data)
        for b in segment_data:
            append_bits(b, 8)
    else:
        # ISO/IEC 18004:2015(E) -- 7.4.6 Kanji mode (page 29)
        if _PY2:
            segment_data = [ord(b) for b in segment_data]
        # Note: len(segment.data)! segment.data_length = len(segment.data) / 2!!
        for i in range(0, len(segment_data), 2):
            code = (segment_data[i] << 8) | segment_data[i + 1]
            if 0x8140 <= code <= 0x9ffc:
                # For characters with Shift JIS values from 8140HEX to 9FFCHEX:
                # a) Subtract 8140HEX from Shift JIS value;
                diff = code - 0x8140
            elif 0xe040 <= code <= 0xebbf:
                # For characters with Shift JIS values from E040HEX to EBBFHEX:
                # a) Subtract C140HEX from Shift JIS value;
                diff = code - 0xc140
            else:  # pragma: no cover
                raise QRCodeError('Invalid Kanji bytes: {0}'.format(code))
            # b) Multiply most significant byte of result by C0HEX;
            # c) Add least significant byte to product from b);
            # d) Convert result to a 13-bit binary string.
            append_bits(((diff >> 8) * 0xc0) + (diff & 0xff), 13)
    return _Segment(buff.getbits(), segment_length, segment_mode, segment_encoding)


def make_matrix(version, reserve_regions=True, add_timing=True):
    """\
    Creates a matrix of the provided `size` (w x h) initialized with the
    (illegal) value 0x2.

    The "timing pattern" is already added to the matrix and the version
    and format areas are initialized with 0x0.

    :param int version: The (Micro) QR Code version
    :rtype: tuple of bytearrays
    """
    size = calc_matrix_size(version)
    row = [0x2] * size
    matrix = tuple([bytearray(row) for i in range(size)])
    if reserve_regions:
        if version > 6:
            # Reserve version pattern areas
            for i in range(6):
                # Upper right
                matrix[i][-11] = 0x0
                matrix[i][-10] = 0x0
                matrix[i][-9] = 0x0
                # Lower left
                matrix[-11][i] = 0x0
                matrix[-10][i] = 0x0
                matrix[-9][i] = 0x0
        # Reserve format pattern areas
        for i in range(9):
            matrix[i][8] = 0x0  # Upper left
            matrix[8][i] = 0x0  # Upper bottom
            if version > 0:
                matrix[-i][8] = 0x0  # Bottom left
                matrix[8][- i] = 0x0  # Upper right
    if add_timing:
        # ISO/IEC 18004:2015 -- 6.3.5 Timing pattern (page 17)
        add_timing_pattern(matrix, version < 1)
    return matrix


def normalize_version(version):
    """\
    Canonicalizes the provided `version`.

    If the `version` is ``None``, this function returns ``None``. Otherwise
    this function checks if `version` is an integer or a Micro QR Code version.
    In case the string represents a Micro QR Code version, an uppercased
    string identifier is returned.

    If the `version` does not represent a valid version identifier (aside of
    ``None``, a VersionError is raised.

    :param version: An integer, a string or ``None``.
    :raises: VersionError: In case the version is not ``None`` and does not
                represent a valid (Micro) QR Code version.
    :rtype: int, str or ``None``
    """
    if version is None:
        return None
    error = False
    try:
        version = int(version)
        # Don't want Micro QR Code constants as input
        error = version < 1
    except (ValueError, TypeError):
        try:
            version = consts.MICRO_VERSION_MAPPING[version.upper()]
        except (KeyError, AttributeError):
            error = True
    if error or not 0 < version < 41 and version not in consts.MICRO_VERSIONS:
        raise VersionError('Unsupported version "{0}". '
                           'Supported: {1} and 1 .. 40'
                           .format(version, ', '.join(sorted(consts.MICRO_VERSION_MAPPING.keys()))))
    return version


def normalize_mode(mode):
    """\
    Returns a (Micro) QR Code mode constant which is equivalent to the
    provided `mode`.

    In case the provided `mode` is ``None``, this function returns ``None``.
    Otherwise a mode constant is returned unless the provided parameter cannot
    be mapped to a valid mode. In the latter case, a ModeError is raised.

    :param mode: An integer or string or ``None``.
    :raises: ModeError: In case the provided `mode` does not represent a valid
             QR Code mode.
    :rtype: int or None
    """
    if mode is None or (isinstance(mode, int)
                        and mode in consts.MODE_MAPPING.values()):
        return mode
    try:
        return consts.MODE_MAPPING[mode.lower()]
    except:  # KeyError or mode.lower() fails
        raise ModeError('Illegal mode "{0}". Supported values: {1}'
                        .format(mode, ', '.join(sorted(consts.MODE_MAPPING.keys()))))


def normalize_mask(mask, is_micro):
    """\
    Normalizes the (user specified) mask.

    :param mask: A mask constant
    :type mask: int or None
    :param bool is_micro: Indicates if the mask is meant to be used for a
            Micro QR Code.
    """
    if mask is None:
        return None
    try:
        mask = int(mask)
    except ValueError:
        raise MaskError('Invalid data mask "{0}". Must be an integer or a string which represents an integer value.'.format(mask))
    if is_micro:
        if not 0 <= mask < 4:
            raise MaskError('Invalid data mask "{0}" for Micro QR Code. Must be in range 0 .. 3'.format(mask))
    else:
        if not 0 <= mask < 8:
            raise MaskError('Invalid data mask "{0}". Must be in range 0 .. 7'.format(mask))
    return mask


def normalize_errorlevel(error, accept_none=False):
    """\
    Returns a constant for the provided error level.

    This function returns ``None`` if the provided parameter is ``None`` and
    `accept_none` is set to ``True`` (default: ``False``). If `error` is ``None``
    and `accept_none` is ``False`` or if the provided parameter cannot be
    mapped to a valid QR Code error level, a ErrorLevelError is raised.

    :param error: String or ``None``.
    :param bool accept_none: Indicates if ``None`` is accepted as error level.
    :rtype: int
    """
    if error is None:
        if not accept_none:
            raise ErrorLevelError('The error level must be provided')
        return error
    try:
        return consts.ERROR_MAPPING[error.upper()]
    except:  # KeyError or error.upper() fails
        if error in consts.ERROR_MAPPING.values():
            return error
        raise ErrorLevelError('Illegal error correction level: "{0}".'
                              'Supported levels: {1}'
                              .format(error, ', '.join(sorted(consts.ERROR_MAPPING.keys()))))


def get_mode_name(mode_const):
    """\
    Returns the mode name for the provided mode constant.

    :param int mode_const: The mode constant (see :py:module:`segno.consts`)
    """
    for name, val in consts.MODE_MAPPING.items():
        if val == mode_const:
            return name
    raise ModeError('Unknown mode "{0}"'.format(mode_const))


def get_error_name(error_const):
    """\
    Returns the error name for the provided error constant.

    :param int error_const: The error constant (see :py:module:`segno.consts`)
    """
    for name, val in consts.ERROR_MAPPING.items():
        if val == error_const:
            return name
    raise ErrorLevelError('Unknown error level "{0}"'.format(error_const))


def get_version_name(version_const):
    """\
    Returns the version name.

    For version 1 .. 40 it returns the version as integer, for Micro QR Codes
    it returns a string like ``M1`` etc.

    :raises: VersionError: In case the `version_constant` is unknown.
    """
    if 0 < version_const < 41:
        return version_const
    for name, v in consts.MICRO_VERSION_MAPPING.items():
        if v == version_const:
            return name
    raise VersionError('Unknown version constant "{0}"'.format(version_const))



_ALPHANUMERIC_PATTERN = re.compile(br'^[' + re.escape(consts.ALPHANUMERIC_CHARS) + br']+\Z')
def is_alphanumeric(data):
    """\
    Returns if the provided `data` can be encoded in "alphanumeric" mode.

    :param bytes data: The data to check.
    :rtype: bool
    """
    return _ALPHANUMERIC_PATTERN.match(data)


def is_kanji(data):
    """\
    Returns if the `data` can be encoded in "kanji" mode.

    :param bytes data: The data to check.
    :rtype: bool
    """
    data_len = len(data)
    if not data_len or data_len % 2:
        return False
    if _PY2:
        data = (ord(c) for c in data)
    data_iter = iter(data)
    for i in range(0, data_len, 2):
        code = (next(data_iter) << 8) | next(data_iter)
        if not (0x8140 <= code <= 0x9ffc or 0xe040 <= code <= 0xebbf):
            return False
    return True


def find_mode(data):
    """\
    Returns the appropriate QR Code mode (an integer constant) for the
    provided `data`.

    :param bytes data: Data to check.
    :rtype: int
    """
    if data.isdigit():
        return consts.MODE_NUMERIC
    if is_alphanumeric(data):
        return consts.MODE_ALPHANUMERIC
    if is_kanji(data):
        return consts.MODE_KANJI
    return consts.MODE_BYTE


def find_version(segments, error, eci, micro, is_sa=False):
    """\

    """
    assert not (eci and micro)
    min_version = 1 if micro is False else consts.VERSION_M1
    max_version = 40 if micro is not True else consts.VERSION_M4
    if min_version < 1:
        min_version = max([find_minimum_version_for_mode(mode) for mode in segments.modes])
    if error is not None and micro is not False:
        min_version = consts.VERSION_M2
    for version in range(min_version, max_version + 1):
        if error is None and version != consts.VERSION_M1:
            error = consts.ERROR_LEVEL_L
        found = False
        try:
            found = consts.SYMBOL_CAPACITY[version][error] >= segments.bit_length_with_overhead(version, eci, is_sa)
        except KeyError:
            pass
        if found:
            return version
    help_txt = ''
    if micro is None:
        help_txt = '(Micro) '
    elif micro:
        help_txt = 'Micro '
    raise DataOverflowError('Data too large. No {0}QR Code can handle the '
                            'provided data'.format(help_txt))


def calc_matrix_size(ver):
    """\
    Returns the matrix size according to the provided `version`.

    Note: This function does not check if `version` is actually a valid
    (Micro) QR Code version. Invalid versions like ``41`` may return a
    size as well.

    :param int ver: (Micro) QR Code version constant.
    :rtype: int
    """
    return ver * 4 + 17 if ver > 0 else (ver + 4) * 2 + 9


def calc_structured_append_parity(content):
    """\
    Calculates the parity data for the Structured Append mode.

    :param str content: The content.
    :rtype: int
    """
    if not isinstance(content, str_type):
        content = str(content)
    try:
        data = content.encode('iso-8859-1')
    except UnicodeError:
        try:
            data = content.encode('shift-jis')
        except (LookupError, UnicodeError):
            data = content.encode('utf-8')
    if _PY2:
        data = (ord(c) for c in data)
    return reduce(xor, data)


def is_mode_supported(mode, ver):
    """\
    Returns if `mode` is supported by `version`.

    Note: This function does not check if `version` is actually a valid
    (Micro) QR Code version. Invalid versions like ``41`` may return an illegal
    value.

    :param int mode: Canonicalized mode.
    :param int or None ver: (Micro) QR Code version constant.
    :rtype: bool
    """
    ver = None if ver > 0 else ver
    try:
        return ver in consts.SUPPORTED_MODES[mode]
    except KeyError:
        raise ModeError('Unknown mode "{0}"'.format(mode))


def find_minimum_version_for_mode(mode):
    """\
    Returns the minimum Micro QR Code version which supports the provided mode.

    :param int mode: Canonicalized mode.
    :rtype: int
    """
    for v in consts.MICRO_VERSIONS:
        if is_mode_supported(mode, v):
            return v
    return 1


def version_range(version):
    """\
    Returns the version range for the provided version. This applies to QR Code
    versions, only.

    :param int version: The QR Code version (1 .. 40)
    :rtype: int
    """
    # ISO/IEC 18004:2015(E)
    # Table 3 — Number of bits in character count indicator for QR Code (page 23)
    if 0 < version < 10:
        return consts.VERSION_RANGE_01_09
    elif 9 < version < 27:
        return consts.VERSION_RANGE_10_26
    elif 26 < version < 41:
        return consts.VERSION_RANGE_27_40
    raise VersionError('Unknown version "{0}"'.format(version))


def get_eci_assignment_number(encoding):
    """\
    Returns the ECI number for the provided encoding.

    :param str encoding: A encoding name
    :return str: The ECI number.
    """
    try:
        return consts.ECI_ASSIGNMENT_NUM[codecs.lookup(encoding).name]
    except KeyError:
        raise QRCodeError('Unknown ECI assignment number for encoding "{0}".'
                          .format(encoding))


def get_data_mask_functions(is_micro):
    """
    Returns the data mask functions.

    ISO/IEC 18004:2015(E) -- 7.8.2 Data mask patterns (page 50)
    Table 10 — Data mask pattern generation conditions (page 50)

    ===============     =====================   =====================================
    QR Code Pattern     Micro QR Code Pattern￼  Condition
    ===============     =====================   =====================================
    000                                         (i + j) mod 2 = 0
    001                 00                      i mod 2 = 0
    010                                         j mod 3 = 0
    011                                         (i + j) mod 3 = 0
    100                 01                      ((i div 2) + (j div 3)) mod 2 = 0
    101                                         (i j) mod 2 + (i j) mod 3 = 0
    110                 10                      ((i j) mod 2 + (i j) mod 3) mod 2 = 0
    111                 11                      ((i+j) mod 2 + (i j) mod 3) mod 2 = 0
    ===============     =====================   =====================================

    :param is_micro: Indicates if data mask functions for a Micro QR Code
            should be returned
    :return: A tuple of functions
    """
    # i = row position, j = col position; (i, j) = (0, 0) = upper left corner
    def fn0(i, j):
        return (i + j) & 0x1 == 0

    def fn1(i, j):
        return i & 0x1 == 0

    def fn2(i, j):
        return j % 3 == 0

    def fn3(i, j):
        return (i + j) % 3 == 0

    def fn4(i, j):
        return (i // 2 + j // 3) & 0x1 == 0

    def fn5(i, j):
        tmp = i * j
        return (tmp & 0x1) + (tmp % 3) == 0

    def fn6(i, j):
        tmp = i * j
        return ((tmp & 0x1) + (tmp % 3)) & 0x1 == 0

    def fn7(i, j):
        return (((i + j) & 0x1) + (i * j) % 3) & 0x1 == 0

    if is_micro:
        return fn1, fn4, fn6, fn7
    return fn0, fn1, fn2, fn3, fn4, fn5, fn6, fn7


class Segments:
    """\
    Represents a sequence of `Segment` instances.

    Note: len(segments) returns the number of Segments and not the data length;
    use segments.data_length
    """
    __slots__ = ('segments', 'bit_length', 'modes')

    def __init__(self):
        self.segments = []
        self.bit_length = 0
        self.modes = []

    def add_segment(self, segment):
        """\

        :param _Segment segment: Segment to add.
        """
        if self.segments:
            prev_seg = self.segments[-1]
            if prev_seg.mode == segment.mode and prev_seg.encoding == segment.encoding:
                # Merge segment with previous segment
                segment = _Segment(prev_seg.bits + segment.bits,
                                   prev_seg.char_count + segment.char_count,
                                   segment.mode, segment.encoding)
                self.bit_length -= len(prev_seg.bits)
                del self.segments[-1]
                del self.modes[-1]
        self.segments.append(segment)
        self.bit_length += len(segment.bits)
        self.modes.append(segment.mode)

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, item):
        return self.segments[item]

    def __iter__(self):
        return iter(self.segments)

    def bit_length_with_overhead(self, version, eci, is_sa=False):
        overhead = 0
        # ECI overhead
        if eci:
            no_eci_indicators = sum([1 for segment in self.segments if segment.mode == consts.MODE_BYTE and segment.encoding != consts.DEFAULT_BYTE_ENCODING])
            overhead += no_eci_indicators * 4  # ECI indicator
            overhead += no_eci_indicators * 8  # ECI assignment no
        if is_sa:
            # 4 bit for mode, 4 bit for the position, 4 bit for total number of symbols
            # 8 bit for parity data
            overhead += 5 * 4
        # Mode indicator overhead
        if version > 0:  # QR Code
            overhead += len(self.modes) * 4
        elif version > consts.VERSION_M1:  # Micro QR Code (M1 has no mode indicator)
            overhead += len(self.modes) * (version + 3)
        # Char count indicator overhead
        ver_range = version_range(version) if version > 0 else version
        overhead += sum([consts.CHAR_COUNT_INDICATOR_LENGTH[mode][ver_range] for mode in self.modes])
        return overhead + self.bit_length


class _Segment(tuple):
    """\
    Represents a data segment.

    A segment provides the (encoding specific) byte data, the data length,
    the QR Code mode, and the used encoding. The latter is ``None`` iff mode
    is not "byte".

    Note that `data_length` may not be equal to len(data)!

    See also ISO/IEC 18004:2015(E) - 7.4.7 Mixing modes (page 30)
    """
    __slots__ = ()

    def __new__(cls, bits, char_count, mode, encoding=None):
        return tuple.__new__(cls, (bits, char_count, mode, encoding))

    bits = property(itemgetter(0))
    char_count = property(itemgetter(1))
    mode = property(itemgetter(2))
    encoding = property(itemgetter(3))


class Buffer:
    """\
    Wraps a bytearray and provides some useful methods to add bits.
    """
    def __init__(self, iterable=()):
        self._data = bytearray(iterable)

    def extend(self, iterable):
        self._data.extend(iterable)

    def append_bits(self, val, length):
        self._data.extend([(val >> i) & 1 for i in reversed(range(length))])

    def getbits(self):
        return self._data

    def toints(self):
        """\
        Returns an iterable of integers interpreting the content of `seq`
        as sequence of binary numbers of length 8.
        """
        def grouper(iterable, n, fillvalue=None):
            "Collect data into fixed-length chunks or blocks"
            # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
            return zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)
        return [int(''.join(map(str, group)), 2) for group in grouper(self._data, 8, 0)]

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]


class _StructuredAppendInfo(tuple):
    """\
    Represents Structured Append information.

    Note: This class provides the Structured Append header information in
    correct order (incl. Structured Append mode indicator); cf.
    ISO/IEC 18004:2015(E) -- 8 Structured Append (page 59).
    """
    def __new__(cls, number, total, parity):
        """\
        :param int number: Symbol number ``[0 .. 15]``
        :param int total: Total symbol count ``[2 .. 15]``
        :param int parity: Parity data.
        """
        return super(_StructuredAppendInfo, cls).__new__(cls, (consts.MODE_STRUCTURED_APPEND, number, total, parity))

    mode = property(itemgetter(0))
    number = property(itemgetter(1))
    total = property(itemgetter(2))
    parity = property(itemgetter(3))
