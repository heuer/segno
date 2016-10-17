# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Additional factory functions for common QR Codes.

The factory functions which return a QR Code use the minimum error correction
level "M". To create a (Micro) QR Code which should use a specific error
correction level or version etc., use the "_data" factory functions which return
a string which can be used as input for :py:func:`segno.make()`.
"""
from __future__ import absolute_import, unicode_literals
import segno
try:  # pragma: no cover
    from urllib.parse import urlsplit, quote
    str_type = str
except ImportError:  # pragma: no cover
    from urlparse import urlsplit
    from urllib import quote
    str = unicode
    str_type = basestring


_MECARD_ESCAPE = {
    ord('\\'): '\\\\',
    ord(';'): '\\;',
    ord(':'): '\\:',
    ord('"'): '\\"',
}


def _escape(s):
    """\
    Escapes ``\\``, ``;``, ``"`` and ``:`` in the provided string.

    :param str|unicode s: The string to escape.
    :rtype unicode
    """
    return str(s).translate(_MECARD_ESCAPE)


def make_wifi_data(ssid, password, security, hidden=False):
    """\
    Creates WIFI configuration string.

    :param str|unicode ssid: The SSID of the network.
    :param str|unicode|None password: The password.
    :param str|unicode|None security: Authentication type; the value should
            be "WEP" or "WPA". Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: unicode
    """
    def quotation_mark(x):
        """\
        Returns '"' if x could be interpreted as hexadecimal value, otherwise
        an empty string.

        See: <https://github.com/zxing/zxing/wiki/Barcode-Contents>
        [...] Enclose in double quotes if it is an ASCII name, but could be
        interpreted as hex (i.e. "ABCD") [...]
        """
        try:
            int(x, 16)
        except ValueError:
            return ''
        return '"'

    data = 'WIFI:'
    if security:
        data += 'T:{0};'.format(security.upper() if security != 'nopass' else security)
    data += 'S:{1}{0}{1};'.format(_escape(ssid), quotation_mark(ssid))
    if password:
        data += 'P:{1}{0}{1};'.format(_escape(password), quotation_mark(password))
    data += 'H:true;' if hidden else ';'
    return data


def make_wifi(ssid, password, security, hidden=False):
    """\
    Creates a WIFI configuration QR Code.

    :param str|unicode ssid: The SSID of the network.
    :param str|unicode|None password: The password.
    :param str|unicode|None security: Authentication type; the value should
            be "WEP" or "WPA". Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
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

    :param str|unicode name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param str|unicode|None reading: Designates a text string to be set as the
            kana name in the phonebook
    :param str|unicode|iterable email: E-mail address. Multiple values are
            allowed.
    :param str|unicode|iterable phone: Phone number. Multiple values are
            allowed.
    :param str|unicode|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str|unicode memo: A notice for the contact.
    :param str|unicode nickname: Nickname.
    :param (str|unicode|int|date) birthday: Birthday. If a string is provided,
            it should encode the date as YYYYMMDD value.
    :param str|unicode|iterable url: Homepage. Multiple values are allowed.
    :param str|unicode|None pobox: P.O. box (address information).
    :param str|unicode|None roomno: Room number (address information).
    :param str|unicode|None houseno: House number (address information).
    :param str|unicode|None city: City (address information).
    :param str|unicode|None prefecture: Prefecture (address information).
    :param str|unicode|None zipcode: Zip code (address information).
    :param str|unicode|None country: Country (address information).
    :rtype: unicode
    """
    def make_multifield(name, val):
        if val is None:
            return ()
        if isinstance(val, str_type):
            val = (val,)
        return ['{0}:{1};'.format(name, _escape(i)) for i in val]

    data = ['MECARD:N:{0};'.format(_escape(name))]
    if reading:
        data.append('SOUND:{0};'.format(_escape(reading)))
    data.extend(make_multifield('TEL', phone))
    data.extend(make_multifield('TELAV', videophone))
    data.extend(make_multifield('EMAIL', email))
    if nickname:
        data.append('NICKNAME:{0};'.format(_escape(nickname)))
    if birthday:
        try:
            birthday = birthday.strftime('%Y%m%d')
        except AttributeError:
            pass
        data.append('BDAY:{0};'.format(birthday))
    data.extend(make_multifield('URL', url))
    adr_properties = (pobox, roomno, houseno, city, prefecture, zipcode, country)
    if any(adr_properties):
        adr_data = [_escape(i or '') for i in adr_properties]
        data.append('ADR:{0},{1},{2},{3},{4},{5},{6};'.format(*adr_data))
    if memo:
        data.append('MEMO:{0};'.format(_escape(memo)))
    data.append(';')
    return ''.join(data)


def make_mecard(name, reading=None, email=None, phone=None, videophone=None,
                memo=None, nickname=None, birthday=None, url=None, pobox=None,
                roomno=None, houseno=None, city=None, prefecture=None,
                zipcode=None, country=None):
    """\
    Returns a QR Code which encodes a `MeCard <https://en.wikipedia.org/wiki/MeCard>`_

    :param str|unicode name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param str|unicode|None reading: Designates a text string to be set as the
            kana name in the phonebook
    :param str|unicode|iterable email: E-mail address. Multiple values are
            allowed.
    :param str|unicode|iterable phone: Phone number. Multiple values are
            allowed.
    :param str|unicode|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str|unicode memo: A notice for the contact.
    :param str|unicode nickname: Nickname.
    :param str|unicode|int|date birthday: Birthday. If a string is provided,
            it should encode the date as YYYYMMDD value.
    :param str|unicode|iterable url: Homepage. Multiple values are allowed.
    :param str|unicode|None pobox: P.O. box (address information).
    :param str|unicode|None roomno: Room number (address information).
    :param str|unicode|None houseno: House number (address information).
    :param str|unicode|None city: City (address information).
    :param str|unicode|None prefecture: Prefecture (address information).
    :param str|unicode|None zipcode: Zip code (address information).
    :param str|unicode|None country: Country (address information).
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


def make_geo_data(lat, lng):
    """\
    Creates a geo location URI.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: unicode
    """
    def float_to_str(f):
        return '{0:.8f}'.format(f).rstrip('0')

    return 'geo:{0},{1}'.format(float_to_str(lat), float_to_str(lng))


def make_geo(lat, lng):
    """\
    Returns a QR Code which encodes geographic location using the ``geo`` URI
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

    :param str|unicode|iterable to: The email address (recipient). Multiple
            values are allowed.
    :param str|unicode|iterable|None cc: The carbon copy recipient. Multiple
            values are allowed.
    :param str|unicode|iterable|None bcc: The blind carbon copy recipient.
            Multiple values are allowed.
    :param str|unicode|None subject: The subject.
    :param str|unicode|None body: The message body.
    """
    def multi(val):
        if not val:
            return ()
        if isinstance(val, str_type):
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

    :param str|unicode|iterable to: The email address (recipient). Multiple
            values are allowed.
    :param str|unicode|iterable|None cc: The carbon copy recipient. Multiple
            values are allowed.
    :param str|unicode|iterable|None bcc: The blind carbon copy recipient.
            Multiple values are allowed.
    :param str|unicode|None subject: The subject.
    :param str|unicode|None body: The message body.
    """
    return segno.make_qr(make_make_email_data(to=to, cc=cc, bcc=bcc,
                                              subject=subject, body=body))
