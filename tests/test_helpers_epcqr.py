#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
EPC QR Codes.

Test against issue <https://github.com/heuer/segno/issues/55>.
"""
import decimal
import pytest
from segno.helpers import make_epc_qr, _make_epc_qr_data as make_epc_qr_data


@pytest.mark.parametrize('amount', [12.3,
                                    12.30,
                                    decimal.Decimal('12.3'),
                                    decimal.Decimal('12.30'),
                                    '12.3',
                                    '12.30'])
def test_text_002(amount):
    name = "François D'Alsace S.A."
    iban = 'FR1420041010050500013M02606'
    text = 'Client:Marie Louise La Lune'
    kw = dict(name=name, iban=iban, text=text, amount=amount)
    data = make_epc_qr_data(**kw)
    # See. EPC069-12 Version 2.1 dtd. 9 February 2012 example 2
    assert len(data) == 103
    encoding = 'iso-8859-1'
    d = [x.decode(encoding) for x in data.split(b'\n')]
    assert 11 == len(d)
    assert 'BCD' == d[0]
    assert '002' == d[1]
    assert '2' == d[2]
    assert 'SCT' == d[3]
    assert name == d[5]
    assert iban == d[6]
    assert 'EUR12.3' == d[7]
    assert '' == d[8]
    assert '' == d[9]
    assert text == d[10]
    qr = make_epc_qr(**kw)
    assert qr
    assert not qr.is_micro
    assert qr.version <= 13
    assert 'M' == qr.error


@pytest.mark.parametrize('expected_amount, amount', [('EUR1000', 1000),
                                                     ('EUR1000', 1000.0),
                                                     ('EUR2000', decimal.Decimal('2000'))])
def test_trailing_zeros(expected_amount, amount):
    name = "François D'Alsace S.A."
    iban = 'FR1420041010050500013M02606'
    text = 'Client:Marie Louise La Lune'
    kw = dict(name=name, iban=iban, text=text, amount=amount)
    data = make_epc_qr_data(**kw)
    assert len(data) == 103  # See. EPC069-12 Version 2.1 dtd. 9 February 2012 example 2
    encoding = 'iso-8859-1'
    d = [x.decode(encoding) for x in data.split(b'\n')]
    assert expected_amount == d[7]


@pytest.mark.parametrize('amount', [5.0, 5, '5.00', decimal.Decimal('5.00000')])
def test_remove_dot(amount):
    kw = _make_valid_kw()
    kw['amount'] = amount
    d = make_epc_qr_data(**kw).split(b'\n')
    assert b'EUR5' == d[7]


@pytest.mark.parametrize('amount', [12.3,
                                    12.30,
                                    decimal.Decimal('12.3'),
                                    decimal.Decimal('12.30'),
                                    '12.3',
                                    '12.30'])
def test_reference_002(amount):
    name = 'Franz Mustermänn'
    iban = 'DE71110220330123456789'
    reference = 'RF18539007547034'
    purpose = 'GDDS'
    bic = 'BHBLDEHHXXX'
    kw = dict(name=name,
              iban=iban,
              reference=reference,
              bic=bic,
              purpose=purpose,
              amount=amount,
              encoding=1)
    data = make_epc_qr_data(**kw)
    assert len(data) == 96  # See. EPC069-12 Version 2.1 dtd. 9 February 2012 example 1
    encoding = 'utf-8'
    d = [x.decode(encoding) for x in data.split(b'\n')]
    assert 10 == len(d)
    assert 'BCD' == d[0]
    assert '002' == d[1]
    assert '1' == d[2]
    assert 'SCT' == d[3]
    assert name == d[5]
    assert iban == d[6]
    assert 'EUR12.3' == d[7]
    assert purpose == d[8]
    assert reference == d[9]
    qr = make_epc_qr(**kw)
    assert qr
    assert not qr.is_micro
    assert qr.version <= 13
    assert 'M' == qr.error


def _make_valid_kw():
    return dict(name="François D'Alsace S.A.",
                iban='FR1420041010050500013M02606',
                text='Client:Marie Louise La Lune',
                amount=12.3)


@pytest.mark.parametrize('amount', [0,
                                    0.004,
                                    '0.001',
                                    '999999999.999',
                                    9999999990.99])
def test_invalid_amount(amount):
    kw = _make_valid_kw()
    kw['amount'] = amount
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'amount' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'amount' in str(ex.value)


@pytest.mark.parametrize('bic', ['BHBLDE',  # Too short
                                 'BHBLDEHHXXXX',  # Too long
                                 'BHBLDEHHXX',  # Too short (either 8 or 11) not 8 <= bic <= 11
                                 'BHBLDEH ',  # Too short after removing trailing WS
                                 ])
def test_invalid_bic(bic):
    kw = _make_valid_kw()
    kw['bic'] = bic
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'BIC' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'BIC' in str(ex.value)


def test_utf8_required():
    kw = _make_valid_kw()
    kw['name'] = 'Funny 😃 name'
    d = make_epc_qr_data(**kw).split(b'\n')
    assert b'1' == d[2]


def test_utf8_explicit():
    kw = _make_valid_kw()
    kw['encoding'] = 'utf-8'
    kw['name'] = 'Funny 😃 name'
    d = make_epc_qr_data(**kw).split(b'\n')
    assert b'1' == d[2]


def test_utf8_explicit2():
    kw = _make_valid_kw()
    kw['encoding'] = 1
    kw['name'] = 'Funny 😃 name'
    d = make_epc_qr_data(**kw).split(b'\n')
    assert b'1' == d[2]


@pytest.mark.parametrize('encoding', range(1, 9))
def test_valid_encoding(encoding):
    kw = _make_valid_kw()
    kw['name'] = 'Simple name'
    kw['encoding'] = encoding
    d = make_epc_qr_data(**kw).split(b'\n')
    assert str(encoding).encode() == d[2]
    qr = make_epc_qr(**kw)
    assert qr


@pytest.mark.parametrize('encoding', [0, 9, '1', b'8', 1.0, 'shift-jis'])
def test_illegal_encoding(encoding):
    kw = _make_valid_kw()
    kw['encoding'] = encoding
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'encoding' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'encoding' in str(ex.value)


@pytest.mark.parametrize('text,reference', [('', ''), (' ', '    '),
                                            ('', None), (None, None),
                                            (None, ' '),
                                            ])
def test_no_text_no_reference(text, reference):
    kw = _make_valid_kw()
    kw['text'] = text
    kw['reference'] = reference
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'reference' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'reference' in str(ex.value)


@pytest.mark.parametrize('iban', ['DE1' + '1' * 34,
                                  '',
                                  None])
def test_illegal_iban(iban):
    kw = _make_valid_kw()
    kw['iban'] = iban
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'IBAN' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'IBAN' in str(ex.value)


@pytest.mark.parametrize('purpose', ['DE1', 'x', 'CDCBC'])
def test_illegal_purpose(purpose):
    kw = _make_valid_kw()
    kw['purpose'] = purpose
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'purpose' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'purpose' in str(ex.value)


@pytest.mark.parametrize('name', [None, '',
                                  'a' * 71,  # too long
                                  ])
def test_illegal_name(name):
    kw = _make_valid_kw()
    kw['name'] = name
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'name' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        make_epc_qr(**kw)
    assert 'name' in str(ex.value)


def test_text_too_long():
    kw = _make_valid_kw()
    kw['text'] = 'a' * 141
    kw['reference'] = None
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'text' in str(ex.value)


def test_reference_too_long():
    kw = _make_valid_kw()
    kw['text'] = None
    kw['reference'] = 'r' * 36
    with pytest.raises(ValueError) as ex:
        make_epc_qr_data(**kw)
    assert 'reference' in str(ex.value)


if __name__ == '__main__':
    pytest.main([__file__])
