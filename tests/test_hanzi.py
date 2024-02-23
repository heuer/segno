#
# Copyright (c) 2016 - 2024 -- Shi Yan
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against Hanzi encoding.
"""
import pytest
import segno
from segno import consts, encoder


def test_detect_hanzi():
    qr = segno.make('汉字')
    assert 'byte' == qr.mode
    assert qr.is_micro
    assert 'M3-M' == qr.designator


def test_default_hanzi_mode():
    qr = segno.make('书读百遍其义自现')
    assert 'byte' == qr.mode
    assert '2-M' == qr.designator


def test_force_hanzi_mode():
    qr = segno.make('书读百遍其义自现', mode='hanzi')
    assert 'hanzi' == qr.mode
    assert '1-M' == qr.designator


def test_default_hanzi_mode2():
    qr = segno.make('大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。乱石穿空，'
                    '惊涛拍岸，卷起千堆雪。江山如画，一时多少豪杰。遥想公瑾当年，小乔初嫁了，雄姿英发。'
                    '羽扇纶巾，谈笑间，樯橹灰飞烟灭。故国神游，多情应笑我，早生华发。人生如梦，一尊还酹江月。')
    assert 'byte' == qr.mode
    assert '12-L' == qr.designator


def test_force_hanzi_mode2():
    qr = segno.make('大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。乱石穿空，'
                    '惊涛拍岸，卷起千堆雪。江山如画，一时多少豪杰。遥想公瑾当年，小乔初嫁了，'
                    '雄姿英发。羽扇纶巾，谈笑间，樯橹灰飞烟灭。故国神游，多情应笑我，早生华发。人生如梦，一尊还酹江月。',
                    mode='hanzi')
    assert 'hanzi' == qr.mode
    assert '9-L' == qr.designator


def test_force_hanzi_mode_and_encoding():
    qr = segno.make('书读百遍其义自现', mode='hanzi', encoding='gb2312')
    assert 'hanzi' == qr.mode
    assert '1-M' == qr.designator


def test_default_utf8_encoder():
    qr = encoder.encode('书读百遍其义自现')
    assert 1 == len(qr.segments)
    segment = qr.segments[0]
    assert consts.MODE_BYTE == segment.mode
    assert 24 == segment.char_count


def test_force_hanzi_encoder():
    qr = encoder.encode('书读百遍其义自现', mode='hanzi')
    assert 1 == len(qr.segments)
    segment = qr.segments[0]
    assert consts.MODE_HANZI == segment.mode
    assert 8 == segment.char_count


def test_detect_hanzi_encoder2():
    # detect as utf8
    qr = encoder.encode('汉字')
    assert 1 == len(qr.segments)
    segment = qr.segments[0]
    assert consts.MODE_BYTE == segment.mode
    assert 6 == segment.char_count


def test_hanzi_bytes():
    qr = encoder.encode('书读百遍其义自现'.encode(consts.HANZI_ENCODING), mode='hanzi')
    assert 1 == len(qr.segments)
    segment = qr.segments[0]
    assert consts.MODE_HANZI == segment.mode
    assert 8 == segment.char_count


def test_not_hanzi():
    qr = segno.make_qr('Ä')
    assert 'byte' == qr.mode
    assert '1-H' == qr.designator


def test_not_hanzi2():
    qr = segno.make_qr('Ä'.encode())
    assert 'byte' == qr.mode
    assert '1-H' == qr.designator


if __name__ == '__main__':
    pytest.main([__file__])
