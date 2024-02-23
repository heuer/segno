#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Test against issue #95.
<https://github.com/heuer/segno/issues/95>

See <https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11>

This module borrows a lot of code from
<https://github.com/zxing/zxing/blob/master/core/src/test/java/com/google/zxing/client/result/WifiParsedResultTestCase.java#L59>  # noqa: E501
copyrighted by ZXing authors:

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import io
import pytest
import segno
from segno import helpers
_qr_decoder_available = False
try:
    from pyzbar.pyzbar import decode as zbardecode
    _qr_decoder_available = True
except (ImportError, FileNotFoundError):  # The latter may occur under Windows
    pass


def qr_to_bytes(qrcode, scale):
    if qrcode.is_micro:
        raise Exception('zbar cannot decode Micro QR codes')
    buff = io.BytesIO()
    for row in qrcode.matrix_iter(scale=scale):
        buff.write(bytearray(0x0 if b else 0xff for b in row))
    return buff.getvalue()


def decode(data):
    scale = 3
    qrcode = segno.make(data, micro=False)
    width, height = qrcode.symbol_size(scale=scale)
    qr_bytes = qr_to_bytes(qrcode, scale)
    decoded = zbardecode((qr_bytes, width, height))
    assert 1 == len(decoded)
    assert 'QRCODE' == decoded[0].type
    return decoded[0].data.decode('utf-8')


def test_issue_95():
    expected = 'WIFI:S:\\"foo\\;bar\\\\baz\\";;'
    data = helpers.make_wifi_data('"foo;bar\\baz"')
    assert data == expected
    if _qr_decoder_available:
        assert decode(data) == expected


# See <https://github.com/zxing/zxing/blob/master/core/src/test/java/com/google/zxing/client/result/WifiParsedResultTestCase.java#L38>  # noqa: E501
# See <https://github.com/zxing/zxing/blob/master/core/src/test/java/com/google/zxing/client/result/WifiParsedResultTestCase.java#L59>  # noqa: E501
@pytest.mark.parametrize('expected, ssid, password', (('WIFI:T:WEP;S:TenChars;P:0123456789;;',
                                                       'TenChars', '0123456789'),
                                                      ('WIFI:T:WEP;S:TenChars;P:abcde56789;;',
                                                       'TenChars', 'abcde56789'),
                                                      ('WIFI:T:WEP;S:TenChars;P:hellothere;;',
                                                       'TenChars', 'hellothere'),
                                                      ('WIFI:T:WEP;S:Ten\\;\\;Chars;P:0123456789;;',
                                                       'Ten;;Chars', '0123456789'),
                                                      ('WIFI:T:WEP;S:Ten\\:\\:Chars;P:0123456789;;',
                                                       'Ten::Chars', '0123456789'),
                                                      ('WIFI:T:WEP;S:TenChars;P:hellothere;;',
                                                       'TenChars', 'hellothere'),
                                                      ('WIFI:T:WEP;S:TenChars;P:hellothere;;',
                                                       'TenChars', 'hellothere'),
                                                      ('WIFI:T:WEP;S:Ten\\;\\;Chars;P:0123456789;;',
                                                       'Ten;;Chars', '0123456789'),
                                                      ('WIFI:T:WEP;S:Ten\\:\\:Chars;P:0123456789;;',
                                                       'Ten::Chars', '0123456789'),
                                                      # Escaped semicolons
                                                      ('WIFI:T:WEP;S:TenChars;P:hello\\;there;;',
                                                       'TenChars', 'hello;there'),
                                                      # Escaped colons
                                                      ('WIFI:T:WEP;S:TenChars;P:hello\\:there;;',
                                                       'TenChars', 'hello:there')
                                                      )
                         )
def test_wep(expected, ssid, password):
    data = helpers.make_wifi_data(ssid=ssid, password=password, security='WEP')
    assert data == expected
    if _qr_decoder_available:
        assert decode(data) == expected


# See <https://github.com/zxing/zxing/blob/master/core/src/test/java/com/google/zxing/client/result/WifiParsedResultTestCase.java#L56> # noqa: E501
@pytest.mark.parametrize('expected, ssid, password', (('WIFI:T:WPA;S:TenChars;P:wow;;',
                                                       'TenChars', 'wow'),
                                                      ('WIFI:T:WPA;S:TenChars;P:space is silent;;',
                                                       'TenChars', 'space is silent'),
                                                      )
                         )
def test_wpa(expected, ssid, password):
    data = helpers.make_wifi_data(ssid=ssid, password=password, security='WPA')
    assert data == expected
    if _qr_decoder_available:
        assert decode(data) == expected


# See <https://github.com/zxing/zxing/blob/master/core/src/test/java/com/google/zxing/client/result/WifiParsedResultTestCase.java#L68> # noqa: E501
@pytest.mark.parametrize('expected, ssid, password, security', (('WIFI:T:WPA;S:test;P:my_password\\\\;;',
                                                                 'test', 'my_password\\', 'WPA'),
                                                                ('WIFI:T:WPA;S:My_WiFi_SSID;P:abc123/;;',
                                                                 'My_WiFi_SSID', 'abc123/', 'WPA'),
                                                                ('WIFI:T:WPA;S:\\"foo\\;bar\\\\baz\\";;',
                                                                 '"foo;bar\\baz"', None, 'WPA')))
def test_escape(expected, ssid, password, security):
    data = helpers.make_wifi_data(ssid=ssid, password=password, security=security)
    assert data == expected
    if _qr_decoder_available:
        assert decode(data) == expected


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
