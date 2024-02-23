#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
QR Code tests.
"""
import os
import io
from itertools import chain
import gzip
import tempfile
import pytest
import segno
from segno import consts


_LEGAL_MICRO_VERSIONS = tuple(chain(consts.MICRO_VERSION_MAPPING.keys(),
                                    [v.lower() for v in consts.MICRO_VERSION_MAPPING.keys()]))
_LEGAL_VERSIONS = tuple(chain(range(1, 41), [str(v) for v in range(1, 41)]))

_LEGAL_ERROR_LEVELS = tuple(chain(consts.ERROR_MAPPING.keys(),
                                  [e.lower() for e in consts.ERROR_MAPPING.keys()]))


def test_eq():
    qr = segno.make('Equals')
    assert qr != qr.matrix


def test_eq2():
    qr = segno.make('Equals')
    qr2 = segno.make('Equals')
    assert qr == qr2


@pytest.mark.parametrize('version, mode', [('M1', 'alphanumeric'),
                                           ('M1', 'byte'),
                                           ('M2', 'byte')])
def test_illegal_mode_micro(version, mode):
    with pytest.raises(ValueError) as ex:
        segno.make(1, version=version, mode=mode)
    assert 'is not available' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        segno.make(1, version=version.lower(), mode=mode)


@pytest.mark.parametrize('version', _LEGAL_MICRO_VERSIONS)
def test_micro_version_contradicts_micro(version):
    with pytest.raises(ValueError) as ex:
        segno.make(1, version=version, micro=False)
    assert '"micro" is False' in str(ex.value)


@pytest.mark.parametrize('version', _LEGAL_VERSIONS)
def test_version_contradicts_micro(version):
    with pytest.raises(ValueError) as ex:
        segno.make(1, version=version, micro=True)
    assert 'version' in str(ex.value)


@pytest.mark.parametrize('version', ['M0', 'M5', -1, 0, 41, 'M1 ', object()])
def test_illegal_version(version):
    with pytest.raises(ValueError) as ex:
        segno.make('a', version=version)
    assert 'version' in str(ex.value)


@pytest.mark.parametrize('version', _LEGAL_MICRO_VERSIONS)
def test_valid_mirco_versions(version):
    qr = segno.make(1, version=version)
    assert qr.is_micro
    assert version.upper() == qr.version


@pytest.mark.parametrize('version', _LEGAL_VERSIONS)
def test_valid_versions(version):
    qr = segno.make(1, version=version)
    assert not qr.is_micro
    assert int(version) == qr.version


@pytest.mark.parametrize('error', _LEGAL_ERROR_LEVELS)
def test_legal_error_levels(error):
    qr = segno.make(1, error=error, boost_error=False)
    assert error.upper() == qr.error


@pytest.mark.parametrize('error', ['R', 'M ', ' L'])
def test_illegal_error_level(error):
    with pytest.raises(ValueError) as ex:
        segno.make(1, error=error)
    assert 'illegal error correction' in str(ex.value).lower()
    assert 'L, M, Q, H' in str(ex.value)


def test_illegal_error_level_micro():
    with pytest.raises(ValueError) as ex:
        segno.make('test', error='H', micro=True)
    assert 'is not available' in str(ex.value)


@pytest.mark.parametrize('data,version', [('abcdefghijklmnopqr', 1),
                                          (123456, 'M1')])
def test_data_too_large(data, version):
    with pytest.raises(segno.DataOverflowError) as ex:
        segno.make(data, version=version)
    assert 'does not fit' in str(ex.value)


def test_eci_and_micro():
    with pytest.raises(ValueError) as ex:
        segno.make('A', eci=True, micro=True)
    assert 'ECI mode' in str(ex.value)


def test_eci_and_micro2():
    with pytest.raises(ValueError) as ex:
        segno.make('A', eci=True, version='m4')
    assert 'ECI mode' in str(ex.value)


def _calc_size(dim, border, scale=1):
    return (dim + 2 * border) * scale


def test_symbol_size():
    qr = segno.make('Hello world', micro=False)
    width, height = 21, 21
    border = 0
    assert (width, height) == qr.symbol_size(border=border)
    border = 1
    assert (_calc_size(width, border) == _calc_size(width, border)), \
        qr.symbol_size(border=border)
    border = 4  # (default border)
    assert (_calc_size(width, border) == _calc_size(width, border)), \
        qr.symbol_size()
    assert (_calc_size(width, border) == _calc_size(width, border)), \
        qr.symbol_size(scale=1)
    assert (_calc_size(width, border, 4), _calc_size(width, border, 4)) == \
           qr.symbol_size(scale=4)
    border = 0
    assert (_calc_size(width, border, 4), _calc_size(width, border, 4)) == \
           qr.symbol_size(border=border, scale=4)


def test_symbol_size_micro():
    qr = segno.make('A', version='m2')
    width, height = 13, 13  # Micro QR Code Version M2 size
    border = 0
    assert (width, height) == qr.symbol_size(border=border)
    border = 1
    dim = _calc_size(width, border)
    assert (dim, dim) == qr.symbol_size(border=border)
    border = 2  # (default border)
    dim = _calc_size(width, border)
    assert (dim, dim) == qr.symbol_size()
    assert (dim, dim) == qr.symbol_size(scale=1)
    dim = _calc_size(width, border, 4)
    assert (dim, dim) == qr.symbol_size(scale=4)
    border = 0
    dim = _calc_size(width, border, 4)
    assert (dim, dim) == qr.symbol_size(border=border, scale=4)


def test_symbol_size_scale_int():
    qr = segno.make_qr('test')
    assert (21, 21) == qr.symbol_size(border=0)


def test_symbol_size_scale_int2():
    qr = segno.make_qr('test')
    border = 2
    dim = 21 + 2 * border
    assert (dim, dim) == qr.symbol_size(border=border)


def test_symbol_size_scale_float():
    qr = segno.make_qr('test')
    dim = 21 * 2.5
    assert (dim, dim) == qr.symbol_size(scale=2.5, border=0)


def test_symbol_size_scale_float2():
    qr = segno.make_qr('test')
    border = 2
    dim = (21 + 2 * border) * 1.5
    assert (dim, dim) == qr.symbol_size(scale=1.5, border=border)


def test_designator():
    qr = segno.make('test', version=40, error='L', boost_error=False)
    assert '40-L' == qr.designator


def test_designator2():
    qr = segno.make('test', version=8, error='m', boost_error=False)
    assert '8-M' == qr.designator


def test_designator_micro():
    qr = segno.make('test', version='M4', error='L', boost_error=False)
    assert 'M4-L' == qr.designator


def test_designator_micro2():
    qr = segno.make('12', version='M1')
    assert 'M1' == qr.designator


def test_error_m1():
    qr = segno.make('12')
    assert 'M1' == qr.version
    assert qr.error is None


def test_default_border():
    qr = segno.make_qr(12)
    assert 4 == qr.default_border_size


def test_default_border_mirco():
    qr = segno.make_micro(12, version='m4')
    assert 2 == qr.default_border_size


def test_neq():
    qr = segno.make('Hello')
    qr2 = segno.make('hello')
    assert qr == qr
    assert qr2 == qr2
    assert qr != qr2


@pytest.mark.parametrize('border', [.2, -1, 1.3])
def test_matrix_iter_invalid_border(border):
    qr = segno.make('A')
    with pytest.raises(ValueError):
        for row in qr.matrix_iter(border=border):
            pass


def test_matrix_iter_border_zero():
    qr = segno.make('No border')
    res = [bytearray(row) for row in qr.matrix_iter(border=0)]
    assert qr.matrix == tuple(res)


def test_matrix_iter_border_default():
    qr = segno.make('A', version=1)
    res = [bytearray(row) for row in qr.matrix_iter(border=None)]
    top_border = [bytearray([0x0] * 29)] * 4
    seq = bytearray([0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x0])
    assert top_border == res[:4]
    assert seq == res[4][:len(seq)]


def test_matrix_iter_border_3():
    qr = segno.make('A', version=1)
    res = [bytearray(row) for row in qr.matrix_iter(border=3)]
    top_border = [bytearray([0x0] * 27)] * 3
    seq = bytearray([0x0, 0x0, 0x0, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x0])
    assert top_border == res[:3]
    assert seq == res[3][:len(seq)]


@pytest.mark.parametrize('border', [.2, -1, 1.3])
def test_matrix_iter_verbose_invalid_border(border):
    qr = segno.make('A')
    with pytest.raises(ValueError):
        for row in qr.matrix_iter(border=border, verbose=True):
            pass


def test_matrix_iter_verbose_border_zero():
    qr = segno.make('No border')
    res = [bytearray([bool(v >> 8) for v in row]) for row in qr.matrix_iter(
        border=0,
        verbose=True)]
    assert qr.matrix == tuple(res)


def test_matrix_iter_verbose_border_default():
    qr = segno.make('A', version=1)
    res = [list(row) for row in qr.matrix_iter(border=None, verbose=True)]
    top_border = [[consts.TYPE_QUIET_ZONE] * 29] * 4
    seq = []
    seq.extend([consts.TYPE_QUIET_ZONE] * 4)
    seq.extend([consts.TYPE_FINDER_PATTERN_DARK] * 7)
    seq.extend([consts.TYPE_SEPARATOR, consts.TYPE_FORMAT_LIGHT])
    assert top_border == res[:4]
    assert seq == res[4][:len(seq)]


def test_matrix_iter_verbose_border_3():
    qr = segno.make('A', version=1)
    res = [list(row) for row in qr.matrix_iter(border=3, verbose=True)]
    top_border = [[consts.TYPE_QUIET_ZONE] * 27] * 3
    seq = []
    seq.extend([consts.TYPE_QUIET_ZONE] * 3)
    seq.extend([consts.TYPE_FINDER_PATTERN_DARK] * 7)
    seq.extend([consts.TYPE_SEPARATOR, consts.TYPE_FORMAT_LIGHT])
    assert top_border == res[:3]
    assert seq == res[3][:len(seq)]


def test_save_png_buffer():
    qr = segno.make_qr('test')
    out = io.BytesIO()
    qr.save(out, kind='png')
    out.seek(0)
    expected = b'\211PNG\r\n\032\n'  # PNG magic number
    val = out.read(len(expected))
    assert expected == val


def test_save_png_filestream():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.png', delete=False) as f:
        fn = f.name
        qr.save(f)
    expected = b'\211PNG\r\n\032\n'  # PNG magic number
    with open(fn, mode='rb') as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


def test_save_png_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.png', delete=False) as f:
        fn = f.name
    qr.save(fn)
    expected = b'\211PNG\r\n\032\n'  # PNG magic number
    with open(fn, mode='rb') as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


@pytest.mark.parametrize('ext', ['svg', 'SvG', 'SVG', 'Svg'])
def test_save_svg_filestream(ext):
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.' + ext, delete=False) as f:
        fn = f.name
        qr.save(f)
    with open(fn, mode='rb') as f:
        val = f.read(6)
    os.unlink(fn)
    assert b'<?xml ' == val


def test_save_svg_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.svg', delete=False) as f:
        fn = f.name
        qr.save(f.name)
    with open(fn, mode='rb') as f:
        val = f.read(6)
    os.unlink(fn)
    assert b'<?xml ' == val


def test_save_svgz_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.svgz', delete=False) as f:
        fn = f.name
    qr.save(fn)
    expected = b'\x1f\x8b\x08'  # gzip magic number
    with open(fn, mode='rb') as f:
        val = f.read(len(expected))
    with gzip.open(fn) as f:
        content = f.read(6)
    os.unlink(fn)
    assert expected == val
    assert b'<?xml ' == content


def test_save_pdf_filestream():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.pdf', delete=False) as f:
        fn = f.name
        qr.save(f)
    with open(fn, mode='rb') as f:
        val = f.read(5)
    os.unlink(fn)
    assert b'%PDF-' == val


def test_save_pdf_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('wb', suffix='.pdf', delete=False) as f:
        fn = f.name
        qr.save(fn)
    with open(fn, mode='rb') as f:
        val = f.read(5)
    os.unlink(fn)
    assert b'%PDF-' == val


def test_save_eps_filestream():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.eps', delete=False) as f:
        fn = f.name
        qr.save(f)
    expected = '%!PS-Adobe-3.0 EPSF-3.0'
    with open(fn) as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


def test_save_eps_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.eps', delete=False) as f:
        fn = f.name
    qr.save(fn)
    expected = '%!PS-Adobe-3.0 EPSF-3.0'
    with open(fn) as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


def test_save_txt_filestream():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        fn = f.name
        qr.save(f)
    expected = '000000'
    with open(fn) as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


def test_save_txt_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        fn = f.name
        qr.save(fn)
    expected = '000000'
    with open(fn, encoding='utf-8') as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


@pytest.mark.parametrize('kind', ['eps', 'EpS', 'EPS', 'Eps'])
def test_save_kind_filestream(kind):
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.murks', delete=False) as f:
        fn = f.name
        qr.save(f, kind=kind)
    expected = '%!PS-Adobe-3.0 EPSF-3.0'
    with open(fn) as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


def test_save_kind_filename():
    qr = segno.make_qr('test')
    f = tempfile.NamedTemporaryFile('w', suffix='.murks', delete=False)
    f.close()
    qr.save(f.name, kind='eps')
    f = open(f.name)
    expected = '%!PS-Adobe-3.0 EPSF-3.0'
    val = f.read(len(expected))
    f.close()
    os.unlink(f.name)
    assert expected == val


def test_save_kind_overrides_filename():
    qr = segno.make_qr('test')
    # SVG extension
    with tempfile.NamedTemporaryFile('w', suffix='.svg', delete=False) as f:
        fn = f.name
    # ... but we want EPS
    qr.save(fn, kind='eps')
    expected = '%!PS-Adobe-3.0 EPSF-3.0'
    with open(f.name) as f:
        val = f.read(len(expected))
    os.unlink(fn)
    assert expected == val


def test_save_invalid_filename():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.murks', delete=True) as f:
        fn = f.name
    with pytest.raises(ValueError):
        qr.save(fn)


def test_save_invalid_filename2():
    qr = segno.make_qr('test')
    with tempfile.NamedTemporaryFile('w', suffix='.murks', delete=True) as f:
        with pytest.raises(ValueError):
            qr.save(f)


def test_unknown_converter():
    qr = segno.make_qr('test')
    with pytest.raises(AttributeError):
        qr.to_murks()


if __name__ == '__main__':
    pytest.main([__file__])
