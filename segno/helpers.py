# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Additional factory functions for common QR codes.

Aside from  :py:func:`make_epc_qr`, the factory functions return a QR code
with the minimum error correction level "L" (or better).

To create a (Micro) QR code which should use a specific error correction level
or version etc., use the "_data" factory functions which return a string which
can be used as input for :py:func:`segno.make()`.
"""
import re
import decimal
import segno
from urllib.parse import quote


_MECARD_ESCAPE = {
    ord('\\'): "\\\\",
    ord(';'): "\\;",
    ord(':'): "\\:",
    ord('"'): '\\"',
}


_VCARD_ESCAPE = {
    ord(','): '\\,',
    ord(';'): '\\;',
}


def _escape_mecard(s):
    """\
    Escapes ``\\``, ``;``, ``"`` and ``:`` in the provided string.

    :param str s: The string to escape.
    :rtype str
    """
    return str(s).translate(_MECARD_ESCAPE)


def _escape_vcard(s):
    """\
    Escapes ``\\``, ``;``, ``"`` and ``:`` in the provided string.

    :param str s: The string to escape.
    :rtype str
    """
    return str(s).translate(_VCARD_ESCAPE)


def make_wifi_data(ssid, password=None, security=None, hidden=False):
    """\
    Creates WIFI configuration string.

    :param str ssid: The SSID of the network.
    :param password: The password.
    :type password: str or None
    :param security: Authentication type; the value should be "WEP" or "WPA".
            Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :type security: str or None
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: str
    """
    escape = _escape_mecard
    data = 'WIFI:'
    if security:
        data += 'T:{0};'.format(security.upper() if security != 'nopass' else security)
    data += f'S:{escape(ssid)};'
    if password is not None:
        data += f'P:{escape(password)};'
    data += 'H:true;' if hidden else ';'
    return data


def make_wifi(ssid, password=None, security=None, hidden=False):
    """\
    Creates a WIFI configuration QR code.

    :param str ssid: The SSID of the network.
    :param password: The password.
    :type password: str or None
    :param security: Authentication type; the value should be "WEP" or "WPA".
            Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :type security: str or None
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_wifi_data(ssid, password, security, hidden))


def make_mecard_data(name, reading=None, email=None, phone=None, videophone=None,
                     memo=None, nickname=None, birthday=None, url=None,
                     pobox=None, roomno=None, houseno=None, city=None,
                     prefecture=None, zipcode=None, country=None):
    """\
    Creates a string encoding the contact information as MeCard.

    :param str name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param reading: Designates a text string to be set as the kana name in the phonebook
    :type reading: str or None
    :param email: E-mail address. Multiple values are allowed.
    :type email: str, iterable of strings, or None
    :param phone: Phone number. Multiple values are allowed.
    :type phone: str, iterable of strings, or None
    :param videophone: Phone number for video calls. Multiple values are allowed.
    :type videophone: str, iterable of strings, or None
    :param memo: A notice for the contact.
    :type memo: str or None
    :param nickname: Nickname.
    :type nickname: str or None
    :param birthday: Birthday. If a string is provided, it should encode the date as YYYYMMDD value.
    :type birthday: str, datetime.date or None
    :param url: Homepage. Multiple values are allowed.
    :type url: str, iterable of strings, or None
    :param pobox: P.O. box (address information).
    :type pobox: str or None
    :param roomno: Room number (address information).
    :type roomno: str or None
    :param houseno: House number (address information).
    :type houseno: str or None
    :param city: City (address information).
    :type city: str or None
    :param prefecture: Prefecture (address information).
    :type prefecture: str or None
    :param zipcode: Zip code (address information).
    :type zipcode: str or None
    :param country: Country (address information).
    :type country: str or None
    :rtype: str
    """
    def make_multifield(name, val):
        if not val:
            return ()
        if isinstance(val, str):
            val = (val,)
        return ['{0}:{1};'.format(name, escape(i)) for i in val]

    escape = _escape_mecard
    data = [f'MECARD:N:{escape(name)};']
    if reading:
        data.append(f'SOUND:{escape(reading)};')
    data.extend(make_multifield('TEL', phone))
    data.extend(make_multifield('TELAV', videophone))
    data.extend(make_multifield('EMAIL', email))
    if nickname:
        data.append(f'NICKNAME:{escape(nickname)};')
    if birthday:
        try:
            birthday = birthday.strftime('%Y%m%d')
        except AttributeError:
            pass
        data.append(f'BDAY:{birthday};')
    data.extend(make_multifield('URL', url))
    adr_properties = (pobox, roomno, houseno, city, prefecture, zipcode, country)
    if any(adr_properties):
        adr_data = [escape(i or '') for i in adr_properties]
        data.append('ADR:{0},{1},{2},{3},{4},{5},{6};'.format(*adr_data))
    if memo:
        data.append(f'MEMO:{escape(memo)};')
    data.append(';')
    return ''.join(data)


def make_mecard(name, reading=None, email=None, phone=None, videophone=None,
                memo=None, nickname=None, birthday=None, url=None, pobox=None,
                roomno=None, houseno=None, city=None, prefecture=None,
                zipcode=None, country=None):
    """\
    Returns a QR code which encodes a `MeCard <https://en.wikipedia.org/wiki/MeCard>`_

    :param str name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param reading: Designates a text string to be set as the kana name in the phonebook
    :type reading: str or None
    :param email: E-mail address. Multiple values are allowed.
    :type email: str, iterable of strings, or None
    :param phone: Phone number. Multiple values are allowed.
    :type phone: str, iterable of strings, or None
    :param videophone: Phone number for video calls. Multiple values are allowed.
    :type videophone: str, iterable of strings, or None
    :param memo: A notice for the contact.
    :type memo: str or None
    :param nickname: Nickname.
    :type nickname: str or None
    :param birthday: Birthday. If a string is provided, it should encode the date as YYYYMMDD value.
    :type birthday: str, datetime.date or None
    :param url: Homepage. Multiple values are allowed.
    :type url: str, iterable of strings, or None
    :param pobox: P.O. box (address information).
    :type pobox: str or None
    :param roomno: Room number (address information).
    :type roomno: str or None
    :param houseno: House number (address information).
    :type houseno: str or None
    :param city: City (address information).
    :type city: str or None
    :param prefecture: Prefecture (address information).
    :type prefecture: str or None
    :param zipcode: Zip code (address information).
    :type zipcode: str or None
    :param country: Country (address information).
    :type country: str or None
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_mecard_data(name=name, reading=reading,
                                          email=email, phone=phone,
                                          videophone=videophone, memo=memo,
                                          nickname=nickname, birthday=birthday,
                                          url=url, pobox=pobox, roomno=roomno,
                                          houseno=houseno, city=city,
                                          prefecture=prefecture, zipcode=zipcode,
                                          country=country))


_looks_like_datetime = re.compile(r'^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:(?:-?\d{2}:\d{2})|Z)?)?$').match


def make_vcard_data(name, displayname, email=None, phone=None, fax=None,
                    videophone=None, memo=None, nickname=None, birthday=None,
                    url=None, pobox=None, street=None, city=None, region=None,
                    zipcode=None, country=None, org=None, lat=None, lng=None,
                    source=None, rev=None, title=None, photo_uri=None,
                    cellphone=None, homephone=None, workphone=None):
    """\
    Creates a string encoding the contact information as vCard 3.0.

    Only a subset of available `vCard 3.0 properties <https://tools.ietf.org/html/rfc2426>`
    is supported.

    :param str name: The name. If it contains a semicolon, , the first part
            is treated as lastname and the second part is treated as forename.
    :param str displayname: Common name.
    :param email: E-mail address. Multiple values are allowed.
    :type email: str, iterable of strings, or None
    :param phone: Phone number. Multiple values are allowed.
    :type phone: str, iterable of strings, or None
    :param fax: Fax number. Multiple values are allowed.
    :type fax: str, iterable of strings, or None
    :param videophone: Phone number for video calls. Multiple values are allowed.
    :type videophone: str, iterable of strings, or None
    :param memo: A notice for the contact.
    :type memo: str or None
    :param nickname: Nickname.
    :type nickname: str or None
    :param birthday: Birthday. If a string is provided, it should encode the
                     date as ``YYYY-MM-DD`` value.
    :type birthday: str, datetime.date or None
    :param url: Homepage. Multiple values are allowed.
    :type url: str, iterable of strings, or None
    :param pobox: P.O. box (address information).
    :type pobox: str or None
    :param street: Street address.
    :type street: str or None
    :param city: City (address information).
    :type city: str or None
    :param region: Region (address information).
    :type region: str or None
    :param zipcode: Zip code (address information).
    :type zipcode: str or None
    :param country: Country (address information).
    :type country: str or None
    :param org: Company / organization name.
    :type org: str or None
    :param lat: Latitude.
    :type lat: float or None
    :param lng: Longitude.
    :type lng: float or None
    :param source: URL where to obtain the vCard.
    :type source: str or None
    :param rev: Revision of the vCard / last modification date.
    :type rev: str, datetime.date or None
    :param title: Job Title. Multiple values are allowed.
    :type title: str, iterable of strings, or None
    :param photo_uri: Photo URI. Multiple values are allowed.
    :type photo_uri: str, iterable of strings, or None
    :param cellphone: Cell phone number. Multiple values are allowed.
    :type cellphone: str, iterable of strings, or None
    :param homephone: Home phone number. Multiple values are allowed.
    :type homephone: str, iterable of strings, or None
    :param workphone: Work phone number. Multiple values are allowed.
    :type workphone: str, iterable of strings, or None
    :rtype: str
    """
    def make_multifield(name, val):
        if not val:
            return ()
        if isinstance(val, str):
            val = (val,)
        return ['{0}:{1}'.format(name, escape(i)) for i in val]

    escape = _escape_vcard
    data = ['BEGIN:VCARD', 'VERSION:3.0',
            f'N:{name}',
            f'FN:{escape(displayname)}']
    if org:
        data.append('ORG:{0}'.format(escape(org)))
    data.extend(make_multifield('EMAIL', email))
    data.extend(make_multifield('TEL', phone))
    data.extend(make_multifield('TEL;TYPE=FAX', fax))
    data.extend(make_multifield('TEL;TYPE=VIDEO', videophone))
    data.extend(make_multifield('TEL;TYPE=CELL', cellphone))
    data.extend(make_multifield('TEL;TYPE=HOME', homephone))
    data.extend(make_multifield('TEL;TYPE=WORK', workphone))
    data.extend(make_multifield('URL', url))
    data.extend(make_multifield('TITLE', title))
    data.extend(make_multifield('PHOTO;VALUE=uri', photo_uri))
    if nickname:
        data.append(f'NICKNAME:{escape(nickname)}')
    adr_properties = (pobox, street, city, region, zipcode, country)
    if any(adr_properties):
        adr_data = [escape(i or '') for i in adr_properties]
        data.append('ADR:{0};;{1};{2};{3};{4};{5}'.format(*adr_data))
    if birthday:
        try:
            birthday = birthday.strftime('%Y-%m-%d')
        except AttributeError:
            pass
        if not isinstance(birthday, str) or not _looks_like_datetime(birthday):
            raise ValueError('"birthday" does not seem to be a valid date or date/time representation')
        data.append(f'BDAY:{birthday}')
    if lat and not lng or lng and not lat:
        raise ValueError('Incomplete geo information, please specify latitude and longitude.')
    if lat and lng:
        data.append(f'GEO:{lat};{lng}')
    if source:
        data.append(f'SOURCE:{escape(source)}')
    if memo:
        data.append(f'NOTE:{escape(memo)}')
    if rev:
        try:
            rev = rev.strftime('%Y-%m-%d')
        except AttributeError:
            pass
        if not isinstance(rev, str) or not _looks_like_datetime(rev):
            raise ValueError('"rev" does not seem to be a valid date or date/time representation')
        data.append(f'REV:{rev}')
    data.append('END:VCARD')
    data.append('')
    return '\r\n'.join(data)


def make_vcard(name, displayname, email=None, phone=None, fax=None,
               videophone=None, memo=None, nickname=None, birthday=None,
               url=None, pobox=None, street=None, city=None, region=None,
               zipcode=None, country=None, org=None, lat=None, lng=None,
               source=None, rev=None, title=None, photo_uri=None,
               cellphone=None, homephone=None, workphone=None):
    """\
    Creates a QR code which encodes a `vCard <https://en.wikipedia.org/wiki/VCard>`_
    version 3.0.

    Only a subset of available `vCard 3.0 properties <https://tools.ietf.org/html/rfc2426>`
    is supported.

    :param str name: The name. If it contains a semicolon, , the first part
            is treated as lastname and the second part is treated as forename.
    :param str displayname: Common name.
    :param email: E-mail address. Multiple values are allowed.
    :type email: str, iterable of strings, or None
    :param phone: Phone number. Multiple values are allowed.
    :type phone: str, iterable of strings, or None
    :param fax: Fax number. Multiple values are allowed.
    :type fax: str, iterable of strings, or None
    :param videophone: Phone number for video calls. Multiple values are allowed.
    :type videophone: str, iterable of strings, or None
    :param memo: A notice for the contact.
    :type memo: str or None
    :param nickname: Nickname.
    :type nickname: str or None
    :param birthday: Birthday. If a string is provided, it should encode the
                     date as ``YYYY-MM-DD`` value.
    :type birthday: str, datetime.date or None
    :param url: Homepage. Multiple values are allowed.
    :type url: str, iterable of strings, or None
    :param pobox: P.O. box (address information).
    :type pobox: str or None
    :param street: Street address.
    :type street: str or None
    :param city: City (address information).
    :type city: str or None
    :param region: Region (address information).
    :type region: str or None
    :param zipcode: Zip code (address information).
    :type zipcode: str or None
    :param country: Country (address information).
    :type country: str or None
    :param org: Company / organization name.
    :type org: str or None
    :param lat: Latitude.
    :type lat: float or None
    :param lng: Longitude.
    :type lng: float or None
    :param source: URL where to obtain the vCard.
    :type source: str or None
    :param rev: Revision of the vCard / last modification date.
    :type rev: str, datetime.date or None
    :param title: Job Title. Multiple values are allowed.
    :type title: str, iterable of strings, or None
    :param photo_uri: Photo URI. Multiple values are allowed.
    :type photo_uri: str, iterable of strings, or None
    :param cellphone: Cell phone number. Multiple values are allowed.
    :type cellphone: str, iterable of strings, or None
    :param homephone: Home phone number. Multiple values are allowed.
    :type homephone: str, iterable of strings, or None
    :param workphone: Work phone number. Multiple values are allowed.
    :type workphone: str, iterable of strings, or None
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_vcard_data(name, displayname, email=email,
                                         phone=phone, fax=fax,
                                         videophone=videophone, memo=memo,
                                         nickname=nickname, birthday=birthday,
                                         url=url, pobox=pobox, street=street,
                                         city=city, region=region,
                                         zipcode=zipcode, country=country,
                                         org=org, lat=lat, lng=lng,
                                         source=source, rev=rev, title=title,
                                         photo_uri=photo_uri,
                                         cellphone=cellphone,
                                         homephone=homephone,
                                         workphone=workphone))


def make_geo_data(lat, lng):
    """\
    Creates a geo location URI.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: str
    """
    def float_to_str(f):
        return '{0:.8f}'.format(f).rstrip('0').rstrip('.')

    return f'geo:{float_to_str(lat)},{float_to_str(lng)}'


def make_geo(lat, lng):
    """\
    Returns a QR code which encodes geographic location using the ``geo`` URI
    scheme.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_geo_data(lat, lng))


def make_make_email_data(to, cc=None, bcc=None, subject=None, body=None):
    """\
    Creates either a simple "mailto:" URL or complete e-mail message with
    (blind) carbon copies and a subject and a body.

    :param to: The email address (recipient). Multiple values are allowed.
    :type to: str or iterable of strings
    :param cc: The carbon copy recipient. Multiple values are allowed.
    :type cc: str, iterable of strings, or None
    :param bcc: The blind carbon copy recipient. Multiple values are allowed.
    :type bcc: str, iterable of strings, or None
    :param subject: The subject.
    :type subject: str or None
    :param body: The message body.
    :type body: str or None
    :rtype: str
    """
    def multi(val):
        if not val:
            return ()
        if isinstance(val, str):
            return (val,)
        return tuple(val)

    delim = '?'
    data = ['mailto:']
    if not to:
        raise ValueError('"to" must not be empty or None')
    data.append(','.join(multi(to)))
    for key, val in (('cc', cc), ('bcc', bcc)):
        vals = multi(val)
        if vals:
            data.append('{0}{1}={2}'.format(delim, key, ','.join(vals)))
            delim = '&'
    for key, val in (('subject', subject), ('body', body)):
        if val is not None:
            data.append('{0}{1}={2}'.format(delim, key, quote(val.encode('utf-8'))))
        delim = '&'
    return ''.join(data)


def make_email(to, cc=None, bcc=None, subject=None, body=None):
    """\
    Encodes either a simple e-mail address or a complete message with
    (blind) carbon copies and a subject and a body.

    :param to: The email address (recipient). Multiple values are allowed.
    :type to: str or iterable of strings
    :param cc: The carbon copy recipient. Multiple values are allowed.
    :type cc: str, iterable of strings, or None
    :param bcc: The blind carbon copy recipient. Multiple values are allowed.
    :type bcc: str, iterable of strings, or None
    :param subject: The subject.
    :type subject: str or None
    :param body: The message body.
    :type body: str or None
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_make_email_data(to=to, cc=cc, bcc=bcc,
                                              subject=subject, body=body))


def _make_epc_qr_data(name, iban, amount, text=None, reference=None, bic=None,
                      purpose=None, encoding=None):
    """\
    Validates the input and creates the data for an EPC QR Code.

    DOES NOT belong to the public API, kept separate from make_epc_qr to apply
    tests on the raw data.

    See :py:func:`make_epc_qr` for a description of the parameters.
    """
    # Ordering is important!
    encodings = ('utf-8', 'iso-8859-1', 'iso-8859-2', 'iso-8859-4',
                 'iso-8859-5', 'iso-8859-7', 'iso-8859-10', 'iso-8859-15')
    min_amount = decimal.Decimal('0.01')
    max_amount = decimal.Decimal('999999999.99')
    text = text.rstrip() if text else text
    reference = reference.rstrip() if reference else reference
    bic = bic.strip() if bic else bic
    name = name.strip() if name else name
    if encoding is not None:
        if isinstance(encoding, str):
            try:
                encoding = encodings.index(encoding.lower()) + 1
            except ValueError:
                raise ValueError('Invalid encoding "{0}", use one of {1}'.format(encoding, encodings))
        elif not isinstance(encoding, int) or not 1 <= encoding <= len(encodings):
            raise ValueError('Invalid encoding number only 1 .. 8 are allowed, got "{}"'.format(encoding))
    if not text and not reference or text and reference:
        raise ValueError('Either a text or a creditor reference (ISO 11649) must be provided')
    if text and not 0 < len(text) <= 140:
        raise ValueError('Invalid text, max. 140 characters are allowed, got "{}"'.format(len(text)))
    elif reference and not 0 < len(reference) <= 35:
        raise ValueError('Invalid creditor reference (ISO 11649), max. 35 characters are allowed, got "{}"'
                         .format(len(reference)))
    if name is None or not 0 < len(name) <= 70:
        raise ValueError('Invalid name, max. 70 characters are allowed, got "{}"'.format(name))
    if iban is None or not 4 < len(iban) <= 34:
        raise ValueError('Invalid IBAN, min. 5 and max. 34 characters are allowed, got "{}"'.format(iban))
    if bic and len(bic) not in (8, 11):
        raise ValueError('Invalid BIC, should be 8 or 11 characters long, got "{}"'.format(bic))
    if purpose and len(purpose) != 4:
        raise ValueError('Invalid purpose, 4 characters are allowed, got "{}"'.format(purpose))
    amount = decimal.Decimal(amount)
    if not min_amount <= amount <= max_amount:
        raise ValueError('Invalid amount, must be in bigger or equal {} and less or equal {}'
                         .format(min_amount, max_amount))
    tmp_data = ['BCD',  # Service tag
                '002',  # Version
                '',  # character set (will be set later)
                'SCT',  # Identification
                bic or '',  # BIC
                name,  # Name of the recipient
                iban,  # IBAN
                'EUR{:.2f}'.format(amount).rstrip('0').rstrip('.'),  # Amount
                purpose or '',  # Purpose
                reference or '',  # Remittance
                ]
    if text:
        tmp_data.append(text)
    data = '\n'.join(tmp_data)
    charset = -1 if encoding is None else encoding
    if charset < 0:
        for idx, enc in enumerate(encodings[1:], start=2):
            try:
                data.encode(enc)
                charset = idx
                break
            except UnicodeEncodeError:
                pass
    if charset < 0:
        charset = 1  # Use UTF-8
    tmp_data[2] = str(charset)  # Set character set
    data = '\n'.join(tmp_data).encode(encodings[charset - 1])
    # Max. payload: 331 bytes
    if len(data) > 331:  # pragma: no cover
        raise ValueError('Payload is too big: Max. 331 bytes allowed, got {} bytes'.format(len(data)))
    return data


def make_epc_qr(name, iban, amount, text=None, reference=None, bic=None,
                purpose=None, encoding=None):
    """\
    Creates and returns an European Payments Council Quick Response Code
    (EPC QR Code) version 002.

    The returned :py:class:`segno.QRCode` uses always the error correction level
    "M" and utilizes max. version 13 to fulfill the constraints of the EPC QR
    Code standard.

    .. note::

        Either the ``text`` or ``reference`` must be provided but not both

    .. note::

        Neither the IBAN, BIC, nor remittance reference number or any other
        information is validated (aside from checks regarding the allowed string
        lengths).

    :param str name: Name of the recipient.
    :param str iban: International Bank Account Number (IBAN)
    :param amount: The amount (in EUR) to transfer.
            The currency is always Euro, no other currencies are supported.
    :type amount: int, float, decimal.Decimal
    :param str text: Remittance Information (unstructured)
    :param str reference: Remittance Information (structured)
    :param str bic: Bank Identifier Code (BIC). Optional, only required
                for non-EEA countries.
    :param str purpose: SEPA purpose code.
    :param encoding: By default, this function tries to find the best,
                minimal encoding. If another encoding should be used, the encoding
                name or the encoding constant (an integer) can be provided:
                ``1``: "UTF-8", ``2``: "ISO 8859-1", ``3``: "ISO 8859-2",
                ``4``: "ISO 8859-4", ``5``: "ISO 8859-5", ``6``: "ISO 8859-7",
                ``7``: "ISO 8859-10", ``8``: "ISO 8859-15"

                The encoding is case-insensitive.
    :type encoding: str or int
    :rtype: segno.QRCode
    """
    # Create a QR Code, error correction level "M".
    # It's not allowed to use another level therefore boost_error must be disabled
    qr = segno.make_qr(_make_epc_qr_data(name, iban, amount, text, reference,
                                         bic, purpose, encoding),
                       error='m', boost_error=False)
    # This shouldn't happen
    if qr.version > 13:  # pragma: no cover
        raise ValueError('Invalid EPC QR Code, max. QR Code version 13 is allowed, got "{}"'.format(qr.designator))
    return qr
