# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2017 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #29.
<https://github.com/heuer/segno/issues/29>
"""
from __future__ import absolute_import, unicode_literals
import os
import io
import tempfile
import shutil
import pytest
import segno
from segno import encoder
try:
    from .utils import read_matrix
except (ValueError, SystemError):  # Attempted relative import in non-package
    from utils import read_matrix


def test_iso_figure29():
    pass


def test_seq_behave_like_qrcode():
    qr = segno.make_qr('Something')
    sa = segno.QRCodeSequence([qr])
    assert 1 == len(sa)
    assert not qr.is_micro
    assert qr.is_micro == sa.is_micro
    assert qr.version == sa.version
    assert qr.error == sa.error
    assert qr.default_border_size == sa.default_border_size
    assert qr.mask == sa.mask
    assert qr.symbol_size() == sa.symbol_size()
    assert qr.is_micro == sa.is_micro
    assert qr == sa[0]
    assert qr.png_data_uri() == sa.png_data_uri()


def test_seq_dont_behave_like_qrcode():
    qr = segno.make_qr('Something')
    seq = segno.QRCodeSequence([qr, qr])
    assert 2 == len(seq)
    with pytest.raises(AttributeError):
        assert not seq.is_micro


_DATA_PARITY = (
    # Expected, Input
    # See ISO/IEC 18004:2015(E) page 61:
    # 30 ⊕ 31 ⊕ 32 ⊕ 33 ⊕ 34 ⊕ 35 ⊕ 36 ⊕ 37 ⊕ 38 ⊕ 39 ⊕ 93 ⊕ FA ⊕ 96 ⊕ 7B = 85
    (int('85', 16), '0123456789日本'),
    (int('85', 16), '01234日本56789'),
    (49, '123456789'),
    (49, 123456789),
    (160, 'Mürrisch'),
)

@pytest.mark.parametrize('expected, data', _DATA_PARITY)
def test_calc_sa_parity(expected, data):
    assert expected == encoder.calc_structured_append_parity(data)


def test_illegal_version():
    with pytest.raises(segno.VersionError):
        segno.make_sequence('ABCD', version='M4')


# @pytest.mark.skipif(True, reason='TODO')
# def test_encode_single():
#     # ISO/IEC 18004:2015(E) - page 60
#     seq = segno.make_sequence('ABCDEFGHIJKLMN'
#                               'OPQRSTUVWXYZ0123'
#                               '456789ABCDEFGHIJ'
#                               'KLMNOPQRSTUVWXYZ',
#                               error='m', mask=4, boost_error=False)
#     assert 1 == len(seq)
#     ref_matrix = read_matrix('iso-fig-29')
#     qr = seq[0]
#     assert ref_matrix == qr.matrix
#     assert 4 == qr.version
#     assert '4-M' == qr.designator


def test_encode_single2():
    # ISO/IEC 18004:2015(E) - page 7
    # 'QR Code Symbol' as 1-M symbol
    seq = segno.make_sequence('QR Code Symbol', version=1, error='M',
                              boost_error=False)
    assert '1-M' == seq.designator
    ref_matrix = read_matrix('iso-fig-1')
    assert ref_matrix == seq.matrix
    qr = seq[0]
    assert '1-M' == qr.designator
    ref_matrix = read_matrix('iso-fig-1')
    assert ref_matrix == qr.matrix


def test_encode_multi_by_version():
    # ISO/IEC 18004:2015(E) - page 60
    seq = segno.make_sequence('ABCDEFGHIJKLMN'
                              'OPQRSTUVWXYZ0123'
                              '456789ABCDEFGHIJ'
                              'KLMNOPQRSTUVWXYZ',
                              version=1, error='m', mask=4, boost_error=False)
    assert 4 == len(seq)


def test_too_much_for_one_qrcode():
    data = 'A' * 4300  # Version 40 supports max. 4296 alphanumeric chars (40-L)
    with pytest.raises(segno.DataOverflowError):
        segno.make(data)


# @pytest.mark.skipif(True, reason='Cannot divide content automatically, yet')
# def test_too_much_for_one_qrcode_but_fits_into_seq():
#     data = 'A' * 4300  # Version 40 supports max. 4296 alphanumeric chars (40-L)
#     seq = segno.make_sequence(data)


def test_dataoverflow():
    data = 'A' * 25 * 16  # Version 1: max. 25 alphanumeric chars, 16 symbols
    seq = segno.make_sequence(data, version=1)
    assert 16 == len(seq)
    data += 'B'  # Should be too much data for 16 symbols using version 1
    with pytest.raises(segno.DataOverflowError):
        segno.make_sequence(data, version=1)


def test_dataoverflow2():
    data = 'A' * 4296  # Version 40: max. 4296 alphanumeric chars
    seq = segno.make_sequence(data, version=40)
    assert 1 == len(seq)
    data += 'B'
    seq = segno.make_sequence(data, version=40)
    assert 2 == len(seq)


def test_no_version_provided():
    with pytest.raises(ValueError):
        segno.make_sequence('A')


def test_int():
    data = int('1' * 42)
    seq = segno.make_sequence(data, version=1)
    assert 2 == len(seq)


def test_save_one():
    directory = tempfile.mkdtemp()
    assert 0 == len(os.listdir(directory))
    seq = segno.make_sequence('ABC', version=1)
    assert 1 == len(seq)
    seq.save(os.path.join(directory, 'test.svg'))
    number_of_files = len(os.listdir(directory))
    shutil.rmtree(directory)
    assert 1 == number_of_files


def test_save_multiple():
    directory = tempfile.mkdtemp()
    assert 0 == len(os.listdir(directory))
    seq = segno.make_sequence('ABCDEFGHIJKLMN'
                              'OPQRSTUVWXYZ0123'
                              '456789ABCDEFGHIJ'
                              'KLMNOPQRSTUVWXYZ', version=1, error='m')
    assert 4 == len(seq)
    seq.save(os.path.join(directory, 'test.svg'))
    number_of_files = len(os.listdir(directory))
    shutil.rmtree(directory)
    assert 4 == number_of_files


def test_save_terminal_one():
    out_multiple = io.StringIO()
    data = 'QR Code Symbol'
    seq = segno.make_sequence(data, version=1)
    assert 1 == len(seq)
    seq.terminal(out_multiple)
    qr = segno.make_qr(data, version=1)
    out_single = io.StringIO()
    qr.terminal(out_single)
    assert out_single.getvalue() == out_multiple.getvalue()


def test_save_terminal_multiple():
    out_multiple = io.StringIO()
    data = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    seq = segno.make_sequence(data, version=1, error='m')
    assert 4 == len(seq)
    seq.terminal(out_multiple)
    out_single = io.StringIO()
    for qr in seq:
        qr.terminal(out_single)
    assert out_single.getvalue() == out_multiple.getvalue()


if __name__ == '__main__':
    pytest.main([__file__])
