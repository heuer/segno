#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 72

<https://github.com/heuer/segno/issues/72>
"""
import pytest
from segno.helpers import _make_epc_qr_data as make_epc_qr_data, make_epc_qr
from .test_helpers_epcqr import _make_valid_kw


@pytest.mark.parametrize('encoding, number', (('uTf-8', 1),
                                              ('utf-8', 1),
                                              ('iso-8859-1', 2),
                                              ('ISO-8859-2', 3),
                                              ('iSo-8859-4', 4),
                                              ('iso-8859-5', 5),
                                              ('iso-8859-7', 6),
                                              ('iso-8859-10', 7),
                                              ('iso-8859-15', 8)))
def test_valid_encoding(encoding, number):
    kw = _make_valid_kw()
    kw['name'] = 'Simple name'
    kw['encoding'] = encoding
    d = make_epc_qr_data(**kw).split(b'\n')
    assert str(number).encode() == d[2]
    qr = make_epc_qr(**kw)
    assert qr


@pytest.mark.parametrize('encoding', ('utf-16', 'iso-8859-6', 'ascii',
                                      'something'))
def test_illegal_encoding(encoding):
    kw = _make_valid_kw()
    kw['encoding'] = encoding
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'encoding' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'encoding' in str(ex.value)


if __name__ == '__main__':
    pytest.main([__file__])
