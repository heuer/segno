# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Simple benchmarks.
"""
from __future__ import unicode_literals
import timeit

NO = 100


# QR Code Symbol
if False:
    print('qrcode standard', timeit.timeit("import qrcode; import qrcode.image.svg; factory = qrcode.image.svg.SvgImage; qrcode.make('QR Code Symbol', error_correction=qrcode.ERROR_CORRECT_M, box_size=10, image_factory=factory).save('benchmark/qrcode.svg')", number=NO))
    print('qrcode path', timeit.timeit("import qrcode; import qrcode.image.svg; factory = qrcode.image.svg.SvgPathImage; qrcode.make('QR Code Symbol', error_correction=qrcode.ERROR_CORRECT_M, box_size=10, image_factory=factory).save('benchmark/qrcode_path.svg')", number=NO))

    print('pyqrcode', timeit.timeit("import pyqrcode; pyqrcode.create('QR Code Symbol', error='M').svg('benchmark/pyqrcode-QRCodeSymbol.svg', scale=10)", number=NO))

    print('qrcodegen', timeit.timeit("from qrcodegen import QrCode; f = open('benchmark/qrcodegen-QRCodeSymbol.svg', 'wt'); f.write(QrCode.encode_text('QR Code Symbol'.encode('latin1'), QrCode.Ecc.MEDIUM).to_svg_str(border=4)); f.close()", number=NO))

    print('Segno', timeit.timeit("import segno; segno.make_qr('QR Code Symbol', error='M').svg('benchmark/segno-QRCodeSymbol.svg', scale=10)", number=NO))

    print('pyqrcode HW SVG', timeit.timeit("import pyqrcode; pyqrcode.create('HELLO WORLD', error='Q').svg('benchmark/pyqrcode-HELLO-WORLD.svg', scale=10)", number=NO))
    print('qrcodegen HW SVG', timeit.timeit("from qrcodegen import QrCode; f = open('benchmark/qrcodegen-HELLO_WORLD.svg', 'wt'); f.write(QrCode.encode_text('HELLO WORLD', QrCode.Ecc.QUARTILE).to_svg_str(border=4)); f.close()", number=NO))
    print('Segno HW SVG', timeit.timeit("import segno; segno.make_qr('HELLO WORLD', error='Q').svg('benchmark/segno-HELLO_WORLD.svg', scale=10)", number=NO))

    print('qrcode PNG', timeit.timeit("import qrcode; qrcode.make('QR Code Symbol', error_correction=qrcode.ERROR_CORRECT_Q, box_size=10).save('benchmark/qrcode-HELLO-WORLD.png')", number=NO))
    print('pyqrcode PNG', timeit.timeit("import pyqrcode; pyqrcode.create('QR Code Symbol', error='Q').png('benchmark/pyqrcode-HELLO-WORLD.png', scale=10)", number=NO))
    print('Segno PNG', timeit.timeit("import segno; segno.make_qr('QR Code Symbol', error='Q').png('benchmark/segno-HELLO_WORLD.png', scale=10, addad=False)", number=NO))

    print('qrcode 123 PNG', timeit.timeit("import qrcode; qrcode.make(123456789, error_correction=qrcode.ERROR_CORRECT_Q, box_size=10).save('benchmark/qrcode-123456789.png')", number=NO))
    print('pyqrcode 123 PNG', timeit.timeit("import pyqrcode; pyqrcode.create(123456789, error='q').png('benchmark/pyqrcode-123456789.png', scale=10)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr('123456789', error='q', mask=0).png('benchmark/segno-123456789-0.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=1).png('benchmark/segno-123456789-1.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=2).png('benchmark/segno-123456789-2.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=3).png('benchmark/segno-123456789-3.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=4).png('benchmark/segno-123456789-4.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=5).png('benchmark/segno-123456789-5.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=6).png('benchmark/segno-123456789-6.png', scale=10, addad=False)", number=NO))
    print('Segno 123 PNG', timeit.timeit("import segno; segno.make_qr(123456789, error='q', mask=7).png('benchmark/segno-123456789-7.png', scale=10, addad=False)", number=NO))



#print('pyqrcode HW', timeit.timeit("import pyqrcode; pyqrcode.create('HELLO WORLD', error='Q')", number=NO))
#print('qrcodegen HW', timeit.timeit("from qrcodegen import QrCode; QrCode.encode_text('HELLO WORLD', QrCode.Ecc.QUARTILE)", number=NO))
#print('Segno HW', timeit.timeit("import segno; segno.make_qr('HELLO WORLD', error='Q')", number=NO))



# 01234567

if False:

    print(timeit.timeit("import qrcode; import qrcode.image.svg; factory = qrcode.image.svg.SvgImage; qrcode.make('01234567', error_correction=qrcode.ERROR_CORRECT_M, box_size=10, image_factory=factory).save('benchmark/qrcode-01234567.svg')", number=NO))
    print(timeit.timeit("import qrcode; import qrcode.image.svg; factory = qrcode.image.svg.SvgPathImage; qrcode.make('01234567', error_correction=qrcode.ERROR_CORRECT_M, box_size=10, image_factory=factory).save('benchmark/qrcode_path-01234567.svg')", number=NO))

    print(timeit.timeit("import pyqrcode; pyqrcode.create('01234567', error='M').svg('benchmark/pyqrcode-01234567.svg', scale=10)", number=NO))

if False:
    print(timeit.timeit("import qrcode; qrcode.make('QR Code Symbol', error_correction=qrcode.ERROR_CORRECT_M, box_size=10).save('benchmark/qrcode.png')", number=NO))

    print(timeit.timeit("import pyqrcode; pyqrcode.create('QR Code Symbol', error='M').png('benchmark/pyqrcode.png', scale=10)", number=NO))

    print(timeit.timeit("import segno; segno.make_qr('QR Code Symbol', error='M').png('benchmark/segno.png', scale=10, compresslevel=-1)", number=NO))

if False:
    #print(timeit.timeit("import segno; segno.make_qr('01234567', error='M').svg('benchmark/segno-01234567.svg', scale=10)", number=NO))
    print(timeit.timeit("import segno; segno.make_qr('QR Code Symbol', error='M').svg('benchmark/segno-QR-Code-Symbol.svg', scale=10)", number=NO))
    print(timeit.timeit("import segno; segno.make_qr(u'ΑΒΓΔΕ'.encode('ISO-8859-7'), error='M', encoding='ISO-8859-7', eci=True).svg('benchmark/segno-ΑΒΓΔΕ.svg', scale=10)", number=NO))
    print(timeit.timeit("import segno; segno.make_qr(u'ΑΒΓΔΕ', error='M', encoding='ISO-8859-7', eci=True).svg('benchmark/segno-ΑΒΓΔΕ-2.svg', scale=10)", number=NO))
    print(timeit.timeit("import segno; segno.make_qr(u'ΑΒΓΔΕ', error='M').svg('benchmark/segno-ΑΒΓΔΕ-3.svg', scale=10)", number=NO))
    print(timeit.timeit("import segno; segno.make_qr(u'\u2018\u2019\u00A3\u20AC\u20AF', error='M').svg('benchmark/segno-ΑΒΓΔΕ-4.svg', scale=10)", number=NO))
    #print(timeit.timeit("import qrcode; import qrcode.image.svg; factory = qrcode.image.svg.SvgPathImage; qrcode.make('QR Code Symbol', error_correction=qrcode.ERROR_CORRECT_M, box_size=10, image_factory=factory).save('benchmark/qrcode_path-QR-Code-Symbol.svg')", number=NO))
    #'