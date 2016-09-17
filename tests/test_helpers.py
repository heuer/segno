# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the helper factory functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import pytest
from segno import helpers
from datetime import date


def test_geo_default():
    qr = helpers.make_geo(38.8976763,-77.0365297)
    assert not qr.is_micro


def test_geo_data():
    data = helpers.make_geo_data(38.8976763,-77.0365297)
    assert 'geo:38.8976763,-77.0365297' == data


def test_geo_data2():
    data = helpers.make_geo_data(38.89,-77.0365297)
    assert 'geo:38.89,-77.0365297' == data


def test_wifi_data():
    data = helpers.make_wifi_data(ssid='SSID', password=None, security=None)
    assert 'WIFI:S:SSID;;' == data
    data = helpers.make_wifi_data(ssid='SSID', password='secret', security=None)
    assert 'WIFI:S:SSID;P:secret;;' == data
    data = helpers.make_wifi_data(ssid='SSID', password='secret', security='wpa')
    assert 'WIFI:T:WPA;S:SSID;P:secret;;' == data
    data = helpers.make_wifi_data(ssid='SSID', password='secret', security='nopass')
    assert 'WIFI:T:nopass;S:SSID;P:secret;;' == data
    data = helpers.make_wifi_data(ssid='SSID', password='secret', security='nopass', hidden=True)
    assert 'WIFI:T:nopass;S:SSID;P:secret;H:true;' == data
    data = helpers.make_wifi_data(ssid='ABCDE', password='abcde', security='nopass', hidden=True)
    assert 'WIFI:T:nopass;S:"ABCDE";P:"abcde";H:true;' == data
    data = helpers.make_wifi_data(ssid='"foo;bar\\baz"', password=None, security=None)
    assert 'WIFI:S:\\"foo\\;bar\\\\baz\\";;' == data


def test_wifi():
    qr = helpers.make_wifi(ssid='SSID', password=None, security='WEP')
    assert qr
    assert not qr.is_micro


def test_mecard_data():
    mecard = helpers.make_mecard_data(name='Mustermann,Max')
    assert 'MECARD:N:Mustermann,Max;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', nickname='Maexchen')
    assert 'MECARD:N:Mustermann,Max;NICKNAME:Maexchen;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', phone=['+1', '+2'])
    assert 'MECARD:N:Mustermann,Max;TEL:+1;TEL:+2;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', email='me@example.org')
    assert 'MECARD:N:Mustermann,Max;EMAIL:me@example.org;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', birthday=date.today())
    assert 'MECARD:N:Mustermann,Max;BDAY:{0};;'.format(date.today().strftime('%Y%m%d')) == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', birthday=19760919)
    assert 'MECARD:N:Mustermann,Max;BDAY:19760919;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', country='Germany')
    assert 'MECARD:N:Mustermann,Max;ADR:,,,,,,Germany;;' == mecard


def test_mecard():
    qr = helpers.make_mecard(name='Mustermann,Max')
    assert qr


def test_email_data():
    data = helpers.make_make_email_data('me@example.org')
    assert 'mailto:me@example.org' == data
    data = helpers.make_make_email_data(('me@example.org', 'you@example.org'))
    assert 'mailto:me@example.org,you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', cc='you@example.org')
    assert 'mailto:me@example.org?cc:you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', cc=('me@example.org', 'you@example.org'))
    assert 'mailto:me@example.org?cc:me@example.org,you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', cc=('me@example.org', 'you@example.org'), subject='Test')
    assert 'mailto:me@example.org?cc:me@example.org,you@example.org&subject:Test' == data
    data = helpers.make_make_email_data('me@example.org', cc=('me@example.org', 'you@example.org'), subject='Subject', body='Body')
    assert 'mailto:me@example.org?cc:me@example.org,you@example.org&subject:Subject&body:Body' == data


def test_email_data_illegal():
    with pytest.raises(ValueError):
        helpers.make_make_email_data(None)
    with pytest.raises(ValueError):
        helpers.make_make_email_data('')
    with pytest.raises(ValueError):
        helpers.make_make_email_data([])


def test_email():
    qr = helpers.make_email('me@example.org')
    assert qr


if __name__ == '__main__':
    pytest.main([__file__])
