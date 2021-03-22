# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2021 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Constants.

Internal module. May change without further warning.
"""
from collections import namedtuple

ALPHANUMERIC_CHARS = br'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'

# ISO/IEC 18004:2015(E) -- Table 2 — Mode indicators for QR Code (page 23)
MODE_NUMERIC = 0x1
MODE_ALPHANUMERIC = 0x2
MODE_STRUCTURED_APPEND = 0x3
MODE_BYTE = 0x4
MODE_ECI = 0x7
MODE_KANJI = 0x8
# Hanzi is not part of ISO/IEC 18004 and must be enabled by the user explicitly
MODE_HANZI = 0xD

# Micro QR Code uses different mode indicators
# ISO/IEC 18004:2015(E) -- Table 2 — Mode indicators for QR Code (page 23)
MODE_TO_MICRO_MODE_MAPPING = {
    MODE_NUMERIC: 0x0,
    MODE_ALPHANUMERIC: 0x1,
    MODE_BYTE: 0x2,
    MODE_KANJI: 0x3,
}

# Note: These versions must be comparable: Version 1 > M4 > M3 > M2 > M1
VERSION_M4 = 0
VERSION_M3 = -1
VERSION_M2 = -2
VERSION_M1 = -3

MICRO_VERSION_MAPPING = {
    'M1': VERSION_M1,
    'M2': VERSION_M2,
    'M3': VERSION_M3,
    'M4': VERSION_M4,
}

MICRO_VERSIONS = tuple(sorted(MICRO_VERSION_MAPPING.values()))

# ISO/IEC 18004:2015(E)
# Table 12 — Error correction level indicators for QR Code symbols (page 55)
ERROR_LEVEL_L = 1
ERROR_LEVEL_M = 0
ERROR_LEVEL_Q = 3
ERROR_LEVEL_H = 2

ERROR_LEVEL_TO_MICRO_MAPPING = {
    VERSION_M1: {None: 0},
    VERSION_M2: {ERROR_LEVEL_L: 1,
                 ERROR_LEVEL_M: 2},
    VERSION_M3: {ERROR_LEVEL_L: 3,
                 ERROR_LEVEL_M: 4},
    VERSION_M4: {ERROR_LEVEL_L: 5,
                 ERROR_LEVEL_M: 6,
                 ERROR_LEVEL_Q: 7},
}

DEFAULT_BYTE_ENCODING = 'iso-8859-1'
KANJI_ENCODING = 'shift_jis'
HANZI_ENCODING = 'gb2312'

MODE_MAPPING = {
    'numeric': MODE_NUMERIC,
    'alphanumeric': MODE_ALPHANUMERIC,
    'byte': MODE_BYTE,
    'kanji': MODE_KANJI,
    'hanzi': MODE_HANZI,
}

ERROR_MAPPING = {
    'L': ERROR_LEVEL_L,
    'M': ERROR_LEVEL_M,
    'Q': ERROR_LEVEL_Q,
    'H': ERROR_LEVEL_H,
}

#
# ISO/IEC 18004:2015(E) -- 7.3.2 Extended Channel Interpretation (ECI) mode (page 20)
#
# <https://strokescribe.com/en/ECI.html>
# ECI       Reference
# ------    ---------
# 000000    Represents the default encodation scheme
# 000001    Represents the GLI encodation scheme of a number of symbologies
#           with characters 0 to 127 being identical to those of
#           ISO/IEC 646 : 1991 IRV (equivalent to ANSI X3.4) and characters
#           128 to 255 being identical to those values of ISO 8859-1
# 000002    An equivalent code table to ECI 000000, without the return-to-GLI 0
#           logic. It is the default encodation scheme for encoders fully
#           compliant with this standard.
# 000003    ISO/IEC 8859-1 Latin alphabet No. 1
# 000004    ISO/IEC 8859-2 Latin alphabet No. 2
# 000005    ISO/IEC 8859-3 Latin alphabet No. 3
# 000006    ISO/IEC 8859-4 Latin alphabet No. 4
# 000007    ISO/IEC 8859-5 Latin/Cyrillic alphabet
# 000008    ISO/IEC 8859-6 Latin/Arabic alphabet
# 000009    ISO/IEC 8859-7 Latin/Greek alphabet
# 000010    ISO/IEC 8859-8 Latin/Hebrew alphabet
# 000011    ISO/IEC 8859-9 Latin alphabet No. 5
# 000012    ISO/IEC 8859-10 Latin alphabet No. 6
# 000013    ISO/IEC 8859-11 Latin/Thai alphabet
# 000014    Reserved
# 000015    ISO/IEC 8859-13 Latin alphabet No. 7 (Baltic Rim)
# 000016    ISO/IEC 8859-14 Latin alphabet No. 8 (Celtic)
# 000017    ISO/IEC 8859-15 Latin alphabet No. 9
# 000018    ISO/IEC 8859-16 Latin alphabet No. 10
# 000019    Reserved
# 000020    Shift JIS (JIS X 0208 Annex 1 + JIS X 0201)
# 000021    Windows 1250 Latin 2 (Central Europe)
# 000022    Windows 1251 Cyrillic
# 000023    Windows 1252 Latin 1
# 000024    Windows 1256 Arabic
# 000025    ISO/IEC 10646 UCS-2 (High order byte first)
# 000026    ISO/IEC 10646 UTF-8 (See information above)
# 000027    ISO/IEC 646:1991 International Reference Version of ISO 7-bit
#           coded character set
# 000028    Big 5 (Taiwan) Chinese Character Set
# 000029    GB (PRC) Chinese Character Set
# 000030    Korean Character Set
ECI_ASSIGNMENT_NUM = {
    # Codecs name (``codecs.lookup(some-charset).name``) -> ECI designator
    'cp437': 1,
    'iso8859-1': 3,
    'iso8859-2': 4,
    'iso8859-3': 5,
    'iso8859-4': 6,
    'iso8859-5': 7,
    'iso8859-6': 8,
    'iso8859-7': 9,
    'iso8859-8': 10,
    'iso8859-9': 11,
    'iso8859-10': 12,
    'iso8859-11': 13,
    'iso8859-13': 15,
    'iso8859-14': 16,
    'iso8859-15': 17,
    'iso8859-16': 18,
    'shift_jis': 20,
    'cp1250': 21,
    'cp1251': 22,
    'cp1252': 23,
    'cp1256': 24,
    'utf-16-be': 25,
    'utf-8': 26,
    'ascii': 27,
    'big5': 28,
    'gb18030': 29, 'gbk': 29,  # GBK is treated as GB-18030
    'euc_kr': 30,
}


# ISO/IEC 18004:2015(E) -- Table 2 — Mode indicators for QR Code (page 23)
SUPPORTED_MODES = {
    MODE_NUMERIC: (None, VERSION_M1, VERSION_M2, VERSION_M3, VERSION_M4),
    MODE_ALPHANUMERIC: (None, VERSION_M2, VERSION_M3, VERSION_M4),
    MODE_BYTE: (None, VERSION_M3, VERSION_M4),
    MODE_ECI: (None,),
    MODE_KANJI: (None, VERSION_M3, VERSION_M4),
    MODE_HANZI: (None,),
}

# ISO/IEC 18004:2015(E) -- Table 2 — Mode indicators for QR Code (page 23)
TERMINATOR_LENGTH = {
    None: 4,  # QR Codes, all versions
    VERSION_M1: 3,
    VERSION_M2: 5,
    VERSION_M3: 7,
    VERSION_M4: 9
}

VERSION_RANGE_01_09 = 1  # Version  1 ..  9
VERSION_RANGE_10_26 = 2  # Version 10 .. 26
VERSION_RANGE_27_40 = 3  # Version 27 .. 40

# ISO/IEC 18004:2015(E)
# Table 3 — Number of bits in character count indicator for QR Code (page 23)
CHAR_COUNT_INDICATOR_LENGTH = {
    MODE_NUMERIC: {
        VERSION_RANGE_01_09: 10,
        VERSION_RANGE_10_26: 12,
        VERSION_RANGE_27_40: 14, VERSION_M1: 3, VERSION_M2: 4, VERSION_M3: 5, VERSION_M4: 6},
    MODE_ALPHANUMERIC: {
        VERSION_RANGE_01_09: 9,
        VERSION_RANGE_10_26: 11,
        VERSION_RANGE_27_40: 13,                VERSION_M2: 3, VERSION_M3: 4, VERSION_M4: 5},
    MODE_BYTE: {
        VERSION_RANGE_01_09: 8,
        VERSION_RANGE_10_26: 16,
        VERSION_RANGE_27_40: 16,                               VERSION_M3: 4, VERSION_M4: 5},
    MODE_KANJI: {
        VERSION_RANGE_01_09: 8,
        VERSION_RANGE_10_26: 10,
        VERSION_RANGE_27_40: 12,                               VERSION_M3: 3, VERSION_M4: 4},
    MODE_HANZI: {
        VERSION_RANGE_01_09: 8,
        VERSION_RANGE_10_26: 10,
        VERSION_RANGE_27_40: 12},
}


# ISO/IEC 18004:2015(E) - 6.4.10 Bit stream to codeword conversion (page 33)
# Table 7 — Number of symbol characters and input data capacity for QR Code
SYMBOL_CAPACITY = {
    VERSION_M1: {
           None:          20},
    VERSION_M2: {
           ERROR_LEVEL_L: 40,    ERROR_LEVEL_M: 32},
    VERSION_M3: {
           ERROR_LEVEL_L: 84,    ERROR_LEVEL_M: 68},
    VERSION_M4: {
           ERROR_LEVEL_L: 128,   ERROR_LEVEL_M: 112,   ERROR_LEVEL_Q: 80},
    1:    {ERROR_LEVEL_L: 152,   ERROR_LEVEL_M: 128,   ERROR_LEVEL_Q: 104,   ERROR_LEVEL_H: 72},
    2:    {ERROR_LEVEL_L: 272,   ERROR_LEVEL_M: 224,   ERROR_LEVEL_Q: 176,   ERROR_LEVEL_H: 128},
    3:    {ERROR_LEVEL_L: 440,   ERROR_LEVEL_M: 352,   ERROR_LEVEL_Q: 272,   ERROR_LEVEL_H: 208},
    4:    {ERROR_LEVEL_L: 640,   ERROR_LEVEL_M: 512,   ERROR_LEVEL_Q: 384,   ERROR_LEVEL_H: 288},
    5:    {ERROR_LEVEL_L: 864,   ERROR_LEVEL_M: 688,   ERROR_LEVEL_Q: 496,   ERROR_LEVEL_H: 368},
    6:    {ERROR_LEVEL_L: 1088,  ERROR_LEVEL_M: 864,   ERROR_LEVEL_Q: 608,   ERROR_LEVEL_H: 480},
    7:    {ERROR_LEVEL_L: 1248,  ERROR_LEVEL_M: 992,   ERROR_LEVEL_Q: 704,   ERROR_LEVEL_H: 528},
    8:    {ERROR_LEVEL_L: 1552,  ERROR_LEVEL_M: 1232,  ERROR_LEVEL_Q: 880,   ERROR_LEVEL_H: 688},
    9:    {ERROR_LEVEL_L: 1856,  ERROR_LEVEL_M: 1456,  ERROR_LEVEL_Q: 1056,  ERROR_LEVEL_H: 800},
    10:   {ERROR_LEVEL_L: 2192,  ERROR_LEVEL_M: 1728,  ERROR_LEVEL_Q: 1232,  ERROR_LEVEL_H: 976},
    11:   {ERROR_LEVEL_L: 2592,  ERROR_LEVEL_M: 2032,  ERROR_LEVEL_Q: 1440,  ERROR_LEVEL_H: 1120},
    12:   {ERROR_LEVEL_L: 2960,  ERROR_LEVEL_M: 2320,  ERROR_LEVEL_Q: 1648,  ERROR_LEVEL_H: 1264},
    13:   {ERROR_LEVEL_L: 3424,  ERROR_LEVEL_M: 2672,  ERROR_LEVEL_Q: 1952,  ERROR_LEVEL_H: 1440},
    14:   {ERROR_LEVEL_L: 3688,  ERROR_LEVEL_M: 2920,  ERROR_LEVEL_Q: 2088,  ERROR_LEVEL_H: 1576},
    15:   {ERROR_LEVEL_L: 4184,  ERROR_LEVEL_M: 3320,  ERROR_LEVEL_Q: 2360,  ERROR_LEVEL_H: 1784},
    16:   {ERROR_LEVEL_L: 4712,  ERROR_LEVEL_M: 3624,  ERROR_LEVEL_Q: 2600,  ERROR_LEVEL_H: 2024},
    17:   {ERROR_LEVEL_L: 5176,  ERROR_LEVEL_M: 4056,  ERROR_LEVEL_Q: 2936,  ERROR_LEVEL_H: 2264},
    18:   {ERROR_LEVEL_L: 5768,  ERROR_LEVEL_M: 4504,  ERROR_LEVEL_Q: 3176,  ERROR_LEVEL_H: 2504},
    19:   {ERROR_LEVEL_L: 6360,  ERROR_LEVEL_M: 5016,  ERROR_LEVEL_Q: 3560,  ERROR_LEVEL_H: 2728},
    20:   {ERROR_LEVEL_L: 6888,  ERROR_LEVEL_M: 5352,  ERROR_LEVEL_Q: 3880,  ERROR_LEVEL_H: 3080},
    21:   {ERROR_LEVEL_L: 7456,  ERROR_LEVEL_M: 5712,  ERROR_LEVEL_Q: 4096,  ERROR_LEVEL_H: 3248},
    22:   {ERROR_LEVEL_L: 8048,  ERROR_LEVEL_M: 6256,  ERROR_LEVEL_Q: 4544,  ERROR_LEVEL_H: 3536},
    23:   {ERROR_LEVEL_L: 8752,  ERROR_LEVEL_M: 6880,  ERROR_LEVEL_Q: 4912,  ERROR_LEVEL_H: 3712},
    24:   {ERROR_LEVEL_L: 9392,  ERROR_LEVEL_M: 7312,  ERROR_LEVEL_Q: 5312,  ERROR_LEVEL_H: 4112},
    25:   {ERROR_LEVEL_L: 10208, ERROR_LEVEL_M: 8000,  ERROR_LEVEL_Q: 5744,  ERROR_LEVEL_H: 4304},
    26:   {ERROR_LEVEL_L: 10960, ERROR_LEVEL_M: 8496,  ERROR_LEVEL_Q: 6032,  ERROR_LEVEL_H: 4768},
    27:   {ERROR_LEVEL_L: 11744, ERROR_LEVEL_M: 9024,  ERROR_LEVEL_Q: 6464,  ERROR_LEVEL_H: 5024},
    28:   {ERROR_LEVEL_L: 12248, ERROR_LEVEL_M: 9544,  ERROR_LEVEL_Q: 6968,  ERROR_LEVEL_H: 5288},
    29:   {ERROR_LEVEL_L: 13048, ERROR_LEVEL_M: 10136, ERROR_LEVEL_Q: 7288,  ERROR_LEVEL_H: 5608},
    30:   {ERROR_LEVEL_L: 13880, ERROR_LEVEL_M: 10984, ERROR_LEVEL_Q: 7880,  ERROR_LEVEL_H: 5960},
    31:   {ERROR_LEVEL_L: 14744, ERROR_LEVEL_M: 11640, ERROR_LEVEL_Q: 8264,  ERROR_LEVEL_H: 6344},
    32:   {ERROR_LEVEL_L: 15640, ERROR_LEVEL_M: 12328, ERROR_LEVEL_Q: 8920,  ERROR_LEVEL_H: 6760},
    33:   {ERROR_LEVEL_L: 16568, ERROR_LEVEL_M: 13048, ERROR_LEVEL_Q: 9368,  ERROR_LEVEL_H: 7208},
    34:   {ERROR_LEVEL_L: 17528, ERROR_LEVEL_M: 13800, ERROR_LEVEL_Q: 9848,  ERROR_LEVEL_H: 7688},
    35:   {ERROR_LEVEL_L: 18448, ERROR_LEVEL_M: 14496, ERROR_LEVEL_Q: 10288, ERROR_LEVEL_H: 7888},
    36:   {ERROR_LEVEL_L: 19472, ERROR_LEVEL_M: 15312, ERROR_LEVEL_Q: 10832, ERROR_LEVEL_H: 8432},
    37:   {ERROR_LEVEL_L: 20528, ERROR_LEVEL_M: 15936, ERROR_LEVEL_Q: 11408, ERROR_LEVEL_H: 8768},
    38:   {ERROR_LEVEL_L: 21616, ERROR_LEVEL_M: 16816, ERROR_LEVEL_Q: 12016, ERROR_LEVEL_H: 9136},
    39:   {ERROR_LEVEL_L: 22496, ERROR_LEVEL_M: 17728, ERROR_LEVEL_Q: 12656, ERROR_LEVEL_H: 9776},
    40:   {ERROR_LEVEL_L: 23648, ERROR_LEVEL_M: 18672, ERROR_LEVEL_Q: 13328, ERROR_LEVEL_H: 10208}
}


# ISO/IEC 18004:2015(E) -- Table 9 — Error correction characteristics for QR Code (page 38)
EC = namedtuple('EC', 'num_blocks num_total num_data')

ECC = {
    VERSION_M1: {None: (EC(1, 5, 3),)},
    VERSION_M2: {ERROR_LEVEL_L: (EC(1, 10, 5),), ERROR_LEVEL_M: (EC(1, 10, 4),)},
    VERSION_M3: {ERROR_LEVEL_L: (EC(1, 17, 11),), ERROR_LEVEL_M: (EC(1, 17, 9),)},
    VERSION_M4: {ERROR_LEVEL_L: (EC(1, 24, 16),), ERROR_LEVEL_M: (EC(1, 24, 14),),
                 ERROR_LEVEL_Q: (EC(1, 24, 10),)},
    1: {
        ERROR_LEVEL_L: (EC(1, 26, 19),), ERROR_LEVEL_M: (EC(1, 26, 16),),
        ERROR_LEVEL_Q: (EC(1, 26, 13),), ERROR_LEVEL_H: (EC(1, 26, 9),)},
    2: {
        ERROR_LEVEL_L: (EC(1, 44, 34),), ERROR_LEVEL_M: (EC(1, 44, 28),),
        ERROR_LEVEL_Q: (EC(1, 44, 22),), ERROR_LEVEL_H: (EC(1, 44, 16),)},
    3: {
        ERROR_LEVEL_L: (EC(1, 70, 55),), ERROR_LEVEL_M: (EC(1, 70, 44),),
        ERROR_LEVEL_Q: (EC(2, 35, 17),), ERROR_LEVEL_H: (EC(2, 35, 13),)},
    4: {
        ERROR_LEVEL_L: (EC(1, 100, 80),), ERROR_LEVEL_M: (EC(2, 50, 32),),
        ERROR_LEVEL_Q: (EC(2, 50, 24),),  ERROR_LEVEL_H: (EC(4, 25, 9),)},
    5: {
        ERROR_LEVEL_L: (EC(1, 134, 108),), ERROR_LEVEL_M: (EC(2, 67, 43),),
        ERROR_LEVEL_Q: (EC(2, 33, 15), EC(2, 34, 16)),
        ERROR_LEVEL_H: (EC(2, 33, 11), EC(2, 34, 12))},
    6: {
        ERROR_LEVEL_L: (EC(2, 86, 68),), ERROR_LEVEL_M: (EC(4, 43, 27),),
        ERROR_LEVEL_Q: (EC(4, 43, 19),), ERROR_LEVEL_H: (EC(4, 43, 15),)},
    7: {
        ERROR_LEVEL_L: (EC(2, 98, 78),), ERROR_LEVEL_M: (EC(4, 49, 31),),
        ERROR_LEVEL_Q: (EC(2, 32, 14), EC(4, 33, 15)),
        ERROR_LEVEL_H: (EC(4, 39, 13), EC(1, 40, 14))},
    8: {
        ERROR_LEVEL_L: (EC(2, 121, 97),),
        ERROR_LEVEL_M: (EC(2, 60, 38), EC(2, 61, 39)),
        ERROR_LEVEL_Q: (EC(4, 40, 18), EC(2, 41, 19)),
        ERROR_LEVEL_H: (EC(4, 40, 14), EC(2, 41, 15))},
    9: {
        ERROR_LEVEL_L: (EC(2, 146, 116),),
        ERROR_LEVEL_M: (EC(3, 58, 36), EC(2, 59, 37)),
        ERROR_LEVEL_Q: (EC(4, 36, 16), EC(4, 37, 17)),
        ERROR_LEVEL_H: (EC(4, 36, 12), EC(4, 37, 13))},
    10: {
        ERROR_LEVEL_L: (EC(2, 86, 68), EC(2, 87, 69)),
        ERROR_LEVEL_M: (EC(4, 69, 43), EC(1, 70, 44)),
        ERROR_LEVEL_Q: (EC(6, 43, 19), EC(2, 44, 20)),
        ERROR_LEVEL_H: (EC(6, 43, 15), EC(2, 44, 16))},
    11: {
        ERROR_LEVEL_L: (EC(4, 101, 81),),
        ERROR_LEVEL_M: (EC(1, 80, 50), EC(4, 81, 51)),
        ERROR_LEVEL_Q: (EC(4, 50, 22), EC(4, 51, 23)),
        ERROR_LEVEL_H: (EC(3, 36, 12), EC(8, 37, 13))},
    12: {
        ERROR_LEVEL_L: (EC(2, 116, 92), EC(2, 117, 93)),
        ERROR_LEVEL_M: (EC(6, 58, 36), EC(2, 59, 37)),
        ERROR_LEVEL_Q: (EC(4, 46, 20), EC(6, 47, 21)),
        ERROR_LEVEL_H: (EC(7, 42, 14), EC(4, 43, 15))},
    13: {
        ERROR_LEVEL_L: (EC(4, 133, 107),),
        ERROR_LEVEL_M: (EC(8, 59, 37), EC(1, 60, 38)),
        ERROR_LEVEL_Q: (EC(8, 44, 20), EC(4, 45, 21)),
        ERROR_LEVEL_H: (EC(12, 33, 11), EC(4, 34, 12))},
    14: {
        ERROR_LEVEL_L: (EC(3, 145, 115), EC(1, 146, 116)),
        ERROR_LEVEL_M: (EC(4, 64, 40), EC(5, 65, 41)),
        ERROR_LEVEL_Q: (EC(11, 36, 16), EC(5, 37, 17)),
        ERROR_LEVEL_H: (EC(11, 36, 12), EC(5, 37, 13))},
    15: {
        ERROR_LEVEL_L: (EC(5, 109, 87), EC(1, 110, 88)),
        ERROR_LEVEL_M: (EC(5, 65, 41), EC(5, 66, 42)),
        ERROR_LEVEL_Q: (EC(5, 54, 24), EC(7, 55, 25)),
        ERROR_LEVEL_H: (EC(11, 36, 12), EC(7, 37, 13))},
    16: {
        ERROR_LEVEL_L: (EC(5, 122, 98), EC(1, 123, 99)),
        ERROR_LEVEL_M: (EC(7, 73, 45), EC(3, 74, 46)),
        ERROR_LEVEL_Q: (EC(15, 43, 19), EC(2, 44, 20)),
        ERROR_LEVEL_H: (EC(3, 45, 15), EC(13, 46, 16))},
    17: {
        ERROR_LEVEL_L: (EC(1, 135, 107), EC(5, 136, 108)),
        ERROR_LEVEL_M: (EC(10, 74, 46), EC(1, 75, 47)),
        ERROR_LEVEL_Q: (EC(1, 50, 22), EC(15, 51, 23)),
        ERROR_LEVEL_H: (EC(2, 42, 14), EC(17, 43, 15))},
    18: {
        ERROR_LEVEL_L: (EC(5, 150, 120), EC(1, 151, 121)),
        ERROR_LEVEL_M: (EC(9, 69, 43), EC(4, 70, 44)),
        ERROR_LEVEL_Q: (EC(17, 50, 22), EC(1, 51, 23)),
        ERROR_LEVEL_H: (EC(2, 42, 14), EC(19, 43, 15))},
    19: {
        ERROR_LEVEL_L: (EC(3, 141, 113), EC(4, 142, 114)),
        ERROR_LEVEL_M: (EC(3, 70, 44), EC(11, 71, 45)),
        ERROR_LEVEL_Q: (EC(17, 47, 21), EC(4, 48, 22)),
        ERROR_LEVEL_H: (EC(9, 39, 13), EC(16, 40, 14))},
    20: {
        ERROR_LEVEL_L: (EC(3, 135, 107), EC(5, 136, 108)),
        ERROR_LEVEL_M: (EC(3, 67, 41), EC(13, 68, 42)),
        ERROR_LEVEL_Q: (EC(15, 54, 24), EC(5, 55, 25)),
        ERROR_LEVEL_H: (EC(15, 43, 15), EC(10, 44, 16))},
    21: {
        ERROR_LEVEL_L: (EC(4, 144, 116), EC(4, 145, 117)),
        ERROR_LEVEL_M: (EC(17, 68, 42),),
        ERROR_LEVEL_Q: (EC(17, 50, 22), EC(6, 51, 23)),
        ERROR_LEVEL_H: (EC(19, 46, 16), EC(6, 47, 17))},
    22: {
        ERROR_LEVEL_L: (EC(2, 139, 111), EC(7, 140, 112)),
        ERROR_LEVEL_M: (EC(17, 74, 46),),
        ERROR_LEVEL_Q: (EC(7, 54, 24), EC(16, 55, 25)),
        ERROR_LEVEL_H: (EC(34, 37, 13),)},
    23: {
        ERROR_LEVEL_L: (EC(4, 151, 121), EC(5, 152, 122)),
        ERROR_LEVEL_M: (EC(4, 75, 47), EC(14, 76, 48)),
        ERROR_LEVEL_Q: (EC(11, 54, 24), EC(14, 55, 25)),
        ERROR_LEVEL_H: (EC(16, 45, 15), EC(14, 46, 16))},
    24: {
        ERROR_LEVEL_L: (EC(6, 147, 117), EC(4, 148, 118)),
        ERROR_LEVEL_M: (EC(6, 73, 45), EC(14, 74, 46)),
        ERROR_LEVEL_Q: (EC(11, 54, 24), EC(16, 55, 25)),
        ERROR_LEVEL_H: (EC(30, 46, 16), EC(2, 47, 17))},
    25: {
        ERROR_LEVEL_L: (EC(8, 132, 106), EC(4, 133, 107)),
        ERROR_LEVEL_M: (EC(8, 75, 47), EC(13, 76, 48)),
        ERROR_LEVEL_Q: (EC(7, 54, 24), EC(22, 55, 25)),
        ERROR_LEVEL_H: (EC(22, 45, 15), EC(13, 46, 16))},
    26: {
        ERROR_LEVEL_L: (EC(10, 142, 114), EC(2, 143, 115)),
        ERROR_LEVEL_M: (EC(19, 74, 46), EC(4, 75, 47)),
        ERROR_LEVEL_Q: (EC(28, 50, 22), EC(6, 51, 23)),
        ERROR_LEVEL_H: (EC(33, 46, 16), EC(4, 47, 17))},
    27: {
        ERROR_LEVEL_L: (EC(8, 152, 122), EC(4, 153, 123)),
        ERROR_LEVEL_M: (EC(22, 73, 45), EC(3, 74, 46)),
        ERROR_LEVEL_Q: (EC(8, 53, 23), EC(26, 54, 24)),
        ERROR_LEVEL_H: (EC(12, 45, 15), EC(28, 46, 16))},
    28: {
        ERROR_LEVEL_L: (EC(3, 147, 117), EC(10, 148, 118)),
        ERROR_LEVEL_M: (EC(3, 73, 45), EC(23, 74, 46)),
        ERROR_LEVEL_Q: (EC(4, 54, 24), EC(31, 55, 25)),
        ERROR_LEVEL_H: (EC(11, 45, 15), EC(31, 46, 16))},
    29: {
        ERROR_LEVEL_L: (EC(7, 146, 116), EC(7, 147, 117)),
        ERROR_LEVEL_M: (EC(21, 73, 45), EC(7, 74, 46)),
        ERROR_LEVEL_Q: (EC(1, 53, 23), EC(37, 54, 24)),
        ERROR_LEVEL_H: (EC(19, 45, 15), EC(26, 46, 16))},
    30: {
        ERROR_LEVEL_L: (EC(5, 145, 115), EC(10, 146, 116)),
        ERROR_LEVEL_M: (EC(19, 75, 47), EC(10, 76, 48)),
        ERROR_LEVEL_Q: (EC(15, 54, 24), EC(25, 55, 25)),
        ERROR_LEVEL_H: (EC(23, 45, 15), EC(25, 46, 16))},
    31: {
        ERROR_LEVEL_L: (EC(13, 145, 115), EC(3, 146, 116)),
        ERROR_LEVEL_M: (EC(2, 74, 46), EC(29, 75, 47)),
        ERROR_LEVEL_Q: (EC(42, 54, 24), EC(1, 55, 25)),
        ERROR_LEVEL_H: (EC(23, 45, 15), EC(28, 46, 16))},
    32: {
        ERROR_LEVEL_L: (EC(17, 145, 115),),
        ERROR_LEVEL_M: (EC(10, 74, 46), EC(23, 75, 47)),
        ERROR_LEVEL_Q: (EC(10, 54, 24), EC(35, 55, 25)),
        ERROR_LEVEL_H: (EC(19, 45, 15), EC(35, 46, 16))},
    33: {
        ERROR_LEVEL_L: (EC(17, 145, 115), EC(1, 146, 116)),
        ERROR_LEVEL_M: (EC(14, 74, 46), EC(21, 75, 47)),
        ERROR_LEVEL_Q: (EC(29, 54, 24), EC(19, 55, 25)),
        ERROR_LEVEL_H: (EC(11, 45, 15), EC(46, 46, 16))},
    34: {
        ERROR_LEVEL_L: (EC(13, 145, 115), EC(6, 146, 116)),
        ERROR_LEVEL_M: (EC(14, 74, 46), EC(23, 75, 47)),
        ERROR_LEVEL_Q: (EC(44, 54, 24), EC(7, 55, 25)),
        ERROR_LEVEL_H: (EC(59, 46, 16), EC(1, 47, 17))},
    35: {
        ERROR_LEVEL_L: (EC(12, 151, 121), EC(7, 152, 122)),
        ERROR_LEVEL_M: (EC(12, 75, 47), EC(26, 76, 48)),
        ERROR_LEVEL_Q: (EC(39, 54, 24), EC(14, 55, 25)),
        ERROR_LEVEL_H: (EC(22, 45, 15), EC(41, 46, 16))},
    36: {
        ERROR_LEVEL_L: (EC(6, 151, 121), EC(14, 152, 122)),
        ERROR_LEVEL_M: (EC(6, 75, 47), EC(34, 76, 48)),
        ERROR_LEVEL_Q: (EC(46, 54, 24), EC(10, 55, 25)),
        ERROR_LEVEL_H: (EC(2, 45, 15), EC(64, 46, 16))},
    37: {
        ERROR_LEVEL_L: (EC(17, 152, 122), EC(4, 153, 123)),
        ERROR_LEVEL_M: (EC(29, 74, 46), EC(14, 75, 47)),
        ERROR_LEVEL_Q: (EC(49, 54, 24), EC(10, 55, 25)),
        ERROR_LEVEL_H: (EC(24, 45, 15), EC(46, 46, 16))},
    38: {
        ERROR_LEVEL_L: (EC(4, 152, 122), EC(18, 153, 123)),
        ERROR_LEVEL_M: (EC(13, 74, 46), EC(32, 75, 47)),
        ERROR_LEVEL_Q: (EC(48, 54, 24), EC(14, 55, 25)),
        ERROR_LEVEL_H: (EC(42, 45, 15), EC(32, 46, 16))},
    39: {
        ERROR_LEVEL_L: (EC(20, 147, 117), EC(4, 148, 118)),
        ERROR_LEVEL_M: (EC(40, 75, 47), EC(7, 76, 48)),
        ERROR_LEVEL_Q: (EC(43, 54, 24), EC(22, 55, 25)),
        ERROR_LEVEL_H: (EC(10, 45, 15), EC(67, 46, 16))},
    40: {
        ERROR_LEVEL_L: (EC(19, 148, 118), EC(6, 149, 119)),
        ERROR_LEVEL_M: (EC(18, 75, 47), EC(31, 76, 48)),
        ERROR_LEVEL_Q: (EC(34, 54, 24), EC(34, 55, 25)),
        ERROR_LEVEL_H: (EC(20, 45, 15), EC(61, 46, 16))},
}


# ISO/IEC 18004:2015 -- Annex C - D.1 Error correction bit calculation
# Table C.1 — Valid format information bit sequences (page 80)
FORMAT_INFO = (
    # M: mask 0, mask 1 .. 7
    0x5412, 0x5125, 0x5e7c, 0x5b4b, 0x45f9, 0x40ce, 0x4f97, 0x4aa0,
    # L
    0x77c4, 0x72f3, 0x7daa, 0x789d, 0x662f, 0x6318, 0x6c41, 0x6976,
    # H
    0x1689, 0x13be, 0x1ce7, 0x19d0, 0x0762, 0x0255, 0x0d0c, 0x083b,
    # Q
    0x355f, 0x3068, 0x3f31, 0x3a06, 0x24b4, 0x2183, 0x2eda, 0x2bed,
)

FORMAT_INFO_MICRO = (
    0x4445, 0x4172, 0x4e2b, 0x4b1c, 0x55ae, 0x5099, 0x5fc0, 0x5af7,
    0x6793, 0x62a4, 0x6dfd, 0x68ca, 0x7678, 0x734f, 0x7c16, 0x7921,
    0x06de, 0x03e9, 0x0cb0, 0x0987, 0x1735, 0x1202, 0x1d5b, 0x186c,
    0x2508, 0x203f, 0x2f66, 0x2a51, 0x34e3, 0x31d4, 0x3e8d, 0x3bba,
)


# ISO/IEC 18004:2015 -- Annex D - D.1 Error correction bit calculation
# Table D.1 — Version information bit stream for each version (page 82)
VERSION_INFO = (
    # Version 7, 8, 9 .. 40
    0x07c94, 0x085bc, 0x09a99, 0x0a4d3, 0x0bbf6, 0x0c762, 0x0d847, 0x0e60d,
    0x0f928, 0x10b78, 0x1145d, 0x12a17, 0x13532, 0x149a6, 0x15683, 0x168c9,
    0x177ec, 0x18ec4, 0x191e1, 0x1afab, 0x1b08e, 0x1cc1a, 0x1d33f, 0x1ed75,
    0x1f250, 0x209d5, 0x216f0, 0x228ba, 0x2379f, 0x24b0b, 0x2542e, 0x26a64,
    0x27541, 0x28c69,
)


# ISO/IEC 18004:2015 -- Annex E - Position of alignment patterns
# Table E.1 — Row/column coordinates of center module of alignment patterns (page 83)
ALIGNMENT_POS = (
    (6, 18),  # Version 2 (version 1 has no additional alignment patterns)
    (6, 22),  # Version 3
    (6, 26),  # ..
    (6, 30),
    (6, 34),
    (6, 22, 38),  # Version 7
    (6, 24, 42),
    (6, 26, 46),
    (6, 28, 50),
    (6, 30, 54),
    (6, 32, 58),
    (6, 34, 62),
    (6, 26, 46, 66),  # Version 14
    (6, 26, 48, 70),
    (6, 26, 50, 74),
    (6, 30, 54, 78),
    (6, 30, 56, 82),
    (6, 30, 58, 86),
    (6, 34, 62, 90),
    (6, 28, 50, 72, 94),  # Version 21
    (6, 26, 50, 74, 98),
    (6, 30, 54, 78, 102),
    (6, 28, 54, 80, 106),
    (6, 32, 58, 84, 110),
    (6, 30, 58, 86, 114),
    (6, 34, 62, 90, 118),
    (6, 26, 50, 74, 98, 122),  # Version 28
    (6, 30, 54, 78, 102, 126),
    (6, 26, 52, 78, 104, 130),
    (6, 30, 56, 82, 108, 134),
    (6, 34, 60, 86, 112, 138),
    (6, 30, 58, 86, 114, 142),
    (6, 34, 62, 90, 118, 146),
    (6, 30, 54, 78, 102, 126, 150),  # Version 35
    (6, 24, 50, 76, 102, 128, 154),
    (6, 28, 54, 80, 106, 132, 158),
    (6, 32, 58, 84, 110, 136, 162),
    (6, 26, 54, 82, 110, 138, 166),
    (6, 30, 58, 86, 114, 142, 170),  # Version 40
)


# ISO/IEC 18004:2015 -- Annex A - Error detection and correction generator polynomials
# Table A.1 — Generator polynomials for Reed-Solomon error correction codewords (page 73)
GEN_POLY = {
    2: (25, 1),
    5: (113, 164, 166, 119, 10),
    6: (166, 0, 134, 5, 176, 15),
    7: (87, 229, 146, 149, 238, 102, 21),
    8: (175, 238, 208, 249, 215, 252, 196, 28),
    10: (251, 67, 46, 61, 118, 70, 64, 94, 32, 45),
    13: (74, 152, 176, 100, 86, 100, 106, 104, 130, 218, 206, 140, 78),
    14: (199, 249, 155, 48, 190, 124, 218, 137, 216, 87, 207, 59, 22, 91),
    15: (8, 183, 61, 91, 202, 37, 51, 58, 58, 237, 140, 124, 5, 99, 105),
    16: (120, 104, 107, 109, 102, 161, 76, 3, 91, 191, 147, 169, 182, 194, 225, 120),
    17: (43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136),
    18: (215, 234, 158, 94, 184, 97, 118, 170, 79, 187, 152, 148, 252, 179, 5, 98, 96, 153),
    20: (17, 60, 79, 50, 61, 163, 26, 187, 202, 180, 221, 225, 83, 239, 156, 164, 212, 212, 188, 190),
    22: (210, 171, 247, 242, 93, 230, 14, 109, 221, 53, 200, 74, 8, 172, 98, 80, 219, 134, 160, 105, 165, 231),
    24: (229, 121, 135, 48, 211, 117, 251, 126, 159, 180, 169, 152, 192, 226, 228, 218, 111, 0, 117, 232, 87, 96, 227, 21),  # noqa: E501
    26: (173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111, 28, 165, 53, 161, 21, 245, 142, 13, 102, 48, 227, 153, 145, 218, 70),  # noqa: E501
    28: (168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 195, 147, 205, 27, 232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 242, 37, 9, 123),  # noqa: E501
    30: (41, 173, 145, 152, 216, 31, 179, 182, 50, 48, 110, 86, 239, 96, 222, 125, 42, 173, 226, 193, 224, 130, 156, 37, 251, 216, 238, 40, 192, 180)  # noqa: E501
}

# Precomputed Galios Log tables
#
# prime polynomial: 0x11d (285) / generator: 2

# GF(256) log
GALIOS_LOG = (
    0, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100,
    224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138,
    101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181,
    194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191,
    139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136, 54, 208,
    148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66,
    182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94,
    155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112,
    192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165,
    153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63,
    209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242,
    86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45,
    67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108,
    161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203,
    89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215, 79,
    174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175
)

# GF(256) antilog
# Inverse of the logarithm table.  Maps integer logarithms to members
# of the field.
GALIOS_EXP = ([
    1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152,
    45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78,
    156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140, 5,
    10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97,
    194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211,
    187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226, 217, 175,
    67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31,
    62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23,
    46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84, 168, 77, 154,
    41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191,
    99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219,
    171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25,
    50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89,
    178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72,
    144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176,
    125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142] * 2
)


# Constants for module types

TYPE_FINDER_PATTERN_LIGHT = 6
"""\
Light finder module
"""
TYPE_FINDER_PATTERN_DARK = TYPE_FINDER_PATTERN_LIGHT << 8
"""\
Dark finder module.
"""
TYPE_SEPARATOR = 8
"""\
Separator around the finder patterns (light module)
"""
TYPE_ALIGNMENT_PATTERN_LIGHT = 10
"""\
Light alignment pattern module.
"""
TYPE_ALIGNMENT_PATTERN_DARK = TYPE_ALIGNMENT_PATTERN_LIGHT << 8
"""\
Dark alignment pattern module.
"""
TYPE_TIMING_LIGHT = 12
"""\
Light timing pattern module.
"""
TYPE_TIMING_DARK = TYPE_TIMING_LIGHT << 8
"""\
Dark timing patten module.
"""
TYPE_FORMAT_LIGHT = 14
"""\
Light format information module.
"""
TYPE_FORMAT_DARK = TYPE_FORMAT_LIGHT << 8
"""\
Dark format information module.
"""
TYPE_VERSION_LIGHT = 16
"""\
Light version information module.
"""
TYPE_VERSION_DARK = TYPE_VERSION_LIGHT << 8
"""\
Dark version information module.
"""
TYPE_DARKMODULE = 512
"""\
A single dark module which occurs in QR Codes (but not in Micro QR Codes).
"""
TYPE_DATA_LIGHT = 4
"""\
Light module in the encoding area (either a data module or an error correction module).
"""
TYPE_DATA_DARK = TYPE_DATA_LIGHT << 8
"""\
Dark module in the encoding area (either a data module or an error correction module).
"""
TYPE_QUIET_ZONE = 18
"""\
Border of light modules.
"""
