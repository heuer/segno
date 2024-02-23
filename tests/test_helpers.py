#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against the helper factory functions.
Issue <https://github.com/heuer/segno/issues/19>
"""
import pytest
import segno
from segno import helpers
from datetime import date


def test_geo_default():
    qr = helpers.make_geo(38.8976763, -77.0365297)
    assert not qr.is_micro


def test_geo_data():
    data = helpers.make_geo_data(38.8976763, -77.0365297)
    assert 'geo:38.8976763,-77.0365297' == data


def test_geo_data2():
    data = helpers.make_geo_data(38.89, -77.0365297)
    assert 'geo:38.89,-77.0365297' == data


@pytest.mark.parametrize('expected, ssid, password, security, hidden',
                         (('WIFI:S:SSID;;', 'SSID', None, None, False),
                          ('WIFI:T:SECURITY;S:SSID;;', 'SSID', None, 'security', False),
                          ('WIFI:T:SECURITY;S:SSID;P:secret;;', 'SSID', 'secret', 'security', False),
                          ('WIFI:T:WPA;S:SSID;P:secret;;', 'SSID', 'secret', 'wpa', False),
                          ('WIFI:T:nopass;S:SSID;P:secret;;', 'SSID', 'secret', 'nopass', False),
                          ('WIFI:T:nopass;S:SSID;P:secret;H:true;', 'SSID', 'secret', 'nopass', True),
                          ('WIFI:T:nopass;S:ABCDE;P:abcde;H:true;', 'ABCDE', 'abcde', 'nopass', True),
                          ('WIFI:S:\\"foo\\;bar\\\\baz\\";;', '"foo;bar\\baz"', None, None, False),
                          ('WIFI:T:WPA2;S:\\"foo\\;bar\\\\baz\\";P:a\\:password;;',
                           '"foo;bar\\baz"', 'a:password', 'wpa2', False),
                          ))
def test_wifi_data(expected, ssid, password, security, hidden):
    data = helpers.make_wifi_data(ssid=ssid, password=password, security=security, hidden=hidden)
    assert expected == data


def test_wifi():
    qr = helpers.make_wifi(ssid='SSID', password=None, security='WEP')
    assert qr
    assert not qr.is_micro


def test_mecard_data():
    mecard = helpers.make_mecard_data(name='Mustermann,Max')
    assert 'MECARD:N:Mustermann,Max;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max',
                                      nickname='Maexchen')
    assert 'MECARD:N:Mustermann,Max;NICKNAME:Maexchen;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', phone=['+1', '+2'])
    assert 'MECARD:N:Mustermann,Max;TEL:+1;TEL:+2;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max',
                                      email='me@example.org')
    assert 'MECARD:N:Mustermann,Max;EMAIL:me@example.org;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max',
                                      birthday=date.today())
    assert 'MECARD:N:Mustermann,Max;BDAY:{0};;'.format(date.today().strftime('%Y%m%d')) == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', birthday=19760919)
    assert 'MECARD:N:Mustermann,Max;BDAY:19760919;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', country='Germany')
    assert 'MECARD:N:Mustermann,Max;ADR:,,,,,,Germany;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max',
                                      memo='this,is;a\\memo')
    assert 'MECARD:N:Mustermann,Max;MEMO:this,is\\;a\\\\memo;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max',
                                      reading='this,is;a\\sound')
    assert 'MECARD:N:Mustermann,Max;SOUND:this,is\\;a\\\\sound;;' == mecard


def test_mecard():
    qr = helpers.make_mecard(name='Mustermann,Max')
    assert qr


def test_vcard_data():
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Mustermann;Max\r\n' \
           'FN:Max Mustermann\r\n' \
           'END:VCARD\r\n' == vcard
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    org='ABC, Inc.')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Mustermann;Max\r\n' \
           'FN:Max Mustermann\r\n' \
           'ORG:ABC\\, Inc.\r\n' \
           'END:VCARD\r\n' == vcard
    vcard = helpers.make_vcard_data('Stevenson;John;Philip,Paul;Dr.;Jr.,M.D.,A.C.P.', 'John Stevenson')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Stevenson;John;Philip,Paul;Dr.;Jr.,M.D.,A.C.P.\r\n' \
           'FN:John Stevenson\r\n' \
           'END:VCARD\r\n' == vcard
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe', street='Street',
                                    city='City', zipcode='123456')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'ADR:;;Street;City;;123456;\r\n' \
           'END:VCARD\r\n' == vcard
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    street='123 Main Street', city='Any Town',
                                    region='CA', zipcode='91921-1234',
                                    country='Nummerland')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'ADR:;;123 Main Street;Any Town;CA;91921-1234;Nummerland\r\n' \
           'END:VCARD\r\n' == vcard
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    title='Python wrangler')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\nFN:John Doe\r\n' \
           'TITLE:Python wrangler\r\n' \
           'END:VCARD\r\n' == vcard
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    title=['Python wrangler', 'Snake charmer'])
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'TITLE:Python wrangler\r\n' \
           'TITLE:Snake charmer\r\n' \
           'END:VCARD\r\n' == vcard
    photo_uri = 'https://www.example.org/image.jpg'
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe', photo_uri=photo_uri)
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           f'PHOTO;VALUE=uri:{photo_uri}\r\n' \
           'END:VCARD\r\n' == vcard
    photo_uris = ('https://www.example.org/image.jpg',
                  'https://www.example.com/image_another.gif')
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    photo_uri=photo_uris)
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'PHOTO;VALUE=uri:{0}\r\n' \
           'PHOTO;VALUE=uri:{1}\r\n' \
           'END:VCARD\r\n'.format(*photo_uris) == vcard
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    phone='+1', fax='+12', videophone='+123',
                                    cellphone='+1234', homephone='+12345',
                                    workphone='+123456')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'TEL:+1\r\n' \
           'TEL;TYPE=FAX:+12\r\n' \
           'TEL;TYPE=VIDEO:+123\r\n' \
           'TEL;TYPE=CELL:+1234\r\n' \
           'TEL;TYPE=HOME:+12345\r\n' \
           'TEL;TYPE=WORK:+123456\r\n' \
           'END:VCARD\r\n' == vcard


def test_photo_uri():
    photo_uris = ('https://www.example.org/image.jpg',
                  'https://www.example.com/image_another.gif')
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    photo_uri=photo_uris)
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'PHOTO;VALUE=uri:{0}\r\n' \
           'PHOTO;VALUE=uri:{1}\r\n' \
           'END:VCARD\r\n'.format(*photo_uris) == vcard
    qr_from_data = segno.make_qr(vcard)
    assert qr_from_data
    assert qr_from_data.error == 'L'
    qr_from_vcard = helpers.make_vcard('Doe;John', 'John Doe',
                                       photo_uri=photo_uris)
    assert qr_from_vcard
    assert qr_from_vcard.error == 'L'
    assert qr_from_data == qr_from_vcard


def test_vcard_title_escape():
    vcard = helpers.make_vcard_data('Doe;John', 'John Doe',
                                    title='Director, Research and Development')
    assert 'BEGIN:VCARD\r\n' \
           'VERSION:3.0\r\n' \
           'N:Doe;John\r\n' \
           'FN:John Doe\r\n' \
           'TITLE:Director\\, Research and Development\r\n' \
           'END:VCARD\r\n' == vcard


def test_vcard_data_valid_bday():
    expected_vcard_data = 'BEGIN:VCARD\r\n' \
                          'VERSION:3.0\r\n' \
                          'N:Mustermann;Max\r\n' \
                          'FN:Max Mustermann\r\n' \
                          'BDAY:1976-09-19\r\n' \
                          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    birthday='1976-09-19')
    assert expected_vcard_data == vcard
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    birthday=date(year=1976, month=9, day=19))
    assert expected_vcard_data == vcard


def test_vcard_data_invalid_bday():
    with pytest.raises(ValueError):
        helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                birthday='19760919')
    with pytest.raises(ValueError):
        helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                birthday='1976-09-19TZ')


def test_vcard_data_source_url():
    source_url = 'https://example.org/this-is-the-SOURCE-url'
    expected_vcard_data = 'BEGIN:VCARD\r\n' \
                          'VERSION:3.0\r\n' \
                          'N:Mustermann;Max\r\n' \
                          'FN:Max Mustermann\r\n' \
                          f'SOURCE:{source_url}\r\n' \
                          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    source=source_url)
    assert expected_vcard_data == vcard


def test_vcard_data_nickname():
    nickname = 'Mäxchen'
    expected_vcard_data = 'BEGIN:VCARD\r\n' \
                          'VERSION:3.0\r\n' \
                          'N:Mustermann;Max\r\n' \
                          'FN:Max Mustermann\r\n' \
                          f'NICKNAME:{nickname}\r\n' \
                          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    nickname=nickname)
    assert expected_vcard_data == vcard


def test_vcard_data_note():
    note = 'test cases,; we need more test cases'
    expected_vcard_data = 'BEGIN:VCARD\r\n' \
                          'VERSION:3.0\r\n' \
                          'N:Mustermann;Max\r\n' \
                          'FN:Max Mustermann\r\n' \
                          'NOTE:test cases\\,\\; we need more test cases\r\n' \
                          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    memo=note)
    assert expected_vcard_data == vcard


def test_vcard_data_rev():
    expected_vcard_data = 'BEGIN:VCARD\r\n' \
                          'VERSION:3.0\r\n' \
                          'N:Mustermann;Max\r\n' \
                          'FN:Max Mustermann\r\n' \
                          'REV:1976-09-19\r\n' \
                          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    rev='1976-09-19')
    assert expected_vcard_data == vcard
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    rev=date(year=1976, month=9, day=19))
    assert expected_vcard_data == vcard


@pytest.mark.parametrize('rev', ['19760919'
                                 '1976-09-19TZ',
                                 '1976-09-19T-06',
                                 1.2, 1
                                 ])
def test_vcard_data_invalid_rev(rev):
    with pytest.raises(ValueError):
        helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann', rev=rev)


def test_vcard_data_invalid_geo():
    with pytest.raises(ValueError):
        helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann', lat=1.234)
    with pytest.raises(ValueError):
        helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann', lng=1.234)


def test_vcard_data_valid_geo():
    expected_vcard_data = 'BEGIN:VCARD\r\n' \
                          'VERSION:3.0\r\n' \
                          'N:Mustermann;Max\r\n' \
                          'FN:Max Mustermann\r\n' \
                          'GEO:46.235197;8.015445\r\n' \
                          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann',
                                    lat=46.235197, lng=8.015445)
    assert expected_vcard_data == vcard


def test_vcard():
    qr = helpers.make_vcard(name='Mustermann;Max', displayname='Max Mustermann')
    assert qr


def test_email_data():
    data = helpers.make_make_email_data('me@example.org')
    assert 'mailto:me@example.org' == data
    data = helpers.make_make_email_data(('me@example.org', 'you@example.org'))
    assert 'mailto:me@example.org,you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', cc='you@example.org')
    assert 'mailto:me@example.org?cc=you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', bcc='you@example.org')
    assert 'mailto:me@example.org?bcc=you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', cc=('me@example.org',
                                                              'you@example.org'))
    assert 'mailto:me@example.org?cc=me@example.org,you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', bcc=('me@example.org',
                                                               'you@example.org'))
    assert 'mailto:me@example.org?bcc=me@example.org,you@example.org' == data
    data = helpers.make_make_email_data('me@example.org', cc=('me@example.org',
                                                              'you@example.org'),
                                        subject='Test')
    assert 'mailto:me@example.org?cc=me@example.org,you@example.org&subject=Test' == data
    data = helpers.make_make_email_data('me@example.org', cc=('me@example.org',
                                                              'you@example.org'),
                                        subject='Subject', body='Body')
    assert 'mailto:me@example.org?cc=me@example.org,you@example.org&subject=Subject&body=Body' == data
    data = helpers.make_make_email_data('me@example.org', subject='A subject',
                                        body='Hellöö')
    assert 'mailto:me@example.org?subject=A%20subject&body=Hell%C3%B6%C3%B6' == data


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
