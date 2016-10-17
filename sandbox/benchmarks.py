# -*- encoding: utf-8 -*-
"""\
Some benchmarks running against QR Code generators
"""
from __future__ import print_function
import sys
import timeit
import segno
try:
    import qrcode
    from qrcode import QRCode, ERROR_CORRECT_M
    from qrcode.image.svg import SvgImage, SvgPathImage
except ImportError:
    QRCode = None
try:
    from qrcodegen import QrCode
except ImportError:
    QrCode = None
try:
    import pyqrcode
except ImportError:
    pyqrcode = None


if QRCode:
    def create_qrcode(data='QR Code Symbol'):
        """qrcode create"""
        qr = QRCode(error_correction=ERROR_CORRECT_M)
        qr.add_data(data, optimize=False)
        qr.make()

    def svg_qrcode_path(data='QR Code Symbol'):
        """qrcode SVG path"""
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=10,
                    image_factory=SvgPathImage)
        qr.add_data(data, optimize=False)
        qr.make_image().save('out/qrcode_path_%s.svg' % data)

    def svg_qrcode_rects(data='QR Code Symbol'):
        """qrcode SVG rects"""
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=10,
                    image_factory=SvgImage)
        qr.add_data(data, optimize=False)
        qr.make_image().save('out/qrcode_rects_%s.svg' % data)

    def png_qrcode(data='QR Code Symbol'):
        """qrcode PNG"""
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=10)
        qr.add_data(data, optimize=False)
        qr.make_image().save('out/qrcode_%s.png' % data)


if pyqrcode:
    def create_pyqrcode(data='QR Code Symbol'):
        """PyQRCode create"""
        pyqrcode.create(data, error='m')

    def svg_pyqrcode(data='QR Code Symbol'):
        """PyQRCode SVG"""
        pyqrcode.create(data, error='m').svg('out/pyqrcode_%s.svg' % data, scale=10)

    def png_pyqrcode(data='QR Code Symbol'):
        """PyQRCode PNG"""
        pyqrcode.create(data, error='m').png('out/pyqrcode_%s.png' % data, scale=10)


if QrCode:
    def create_qrcodegen(data='QR Code Symbol'):
        """qrcodegen create"""
        QrCode.encode_text(data, QrCode.Ecc.MEDIUM)

    def svg_qrcodegen(data='QR Code Symbol'):
        """qrcodegen SVG"""
        with open('out/qrcodegen_%s.svg' % data, 'wt') as f:
            f.write(QrCode.encode_text(data, QrCode.Ecc.MEDIUM).to_svg_str(border=4))


def create_segno(data='QR Code Symbol'):
    """Segno create"""
    segno.make_qr(data, error='m')


def svg_segno(data='QR Code Symbol'):
    """Segno SVG"""
    segno.make_qr(data, error='m').save('out/segno_%s.svg' % data, scale=10)


def png_segno(data='QR Code Symbol'):
    """Segno PNG"""
    segno.make_qr(data, error='m').save('out/segno_%s.png' % data, scale=10, addad=False)


def run_create_tests(which=None, number=200, table=None):
    tests = ('create_pyqrcode', 'create_qrcodegen',
             'create_qrcode', 'create_segno',)
    if which:
        tests = filter(lambda n: n[len('create_'):] in which, tests)
    _run_tests(tests, number, table)


def run_svg_tests(which=None, number=200, table=None):
    tests = ('svg_pyqrcode', 'svg_qrcodegen',
             'svg_qrcode_path', 'svg_qrcode_rects', 'svg_segno',)

    if which:
        tests = filter(lambda n: n[len('svg_'):] in which, tests)
    _run_tests(tests, number, table)


def run_png_tests(which=None, number=200, table=None):
    tests = ('png_pyqrcode', 'png_qrcode', 'png_segno',)
    if which:
        tests = filter(lambda n: n[len('png_'):] in which, tests)
    _run_tests(tests, number, table)


def _run_tests(tests, number, table=None):
    # Code taken from <https://genshi.edgewall.org/browser/trunk/examples/bench/bigtable.py>
    # Author: Jonas Borgström <jonas@edgewall.com>
    # License: BSD (I'd think since Genshi uses BSD as well)
    for test in [t for t in tests if hasattr(sys.modules[__name__], t)]:
        t = timeit.Timer(setup='from __main__ import %s;' % test, stmt='%s()' % test)
        time = t.timeit(number=number) / number
        if time < 0.00001:
            result = '   (not installed?)'
        else:
            result = '%16.2f ms' % (1000 * time)
        name = getattr(sys.modules[__name__], test).__doc__
        print('%-35s %s' % (name, result))
        if table is not None:
            table.append((name, '%.2f' % (1000 * time)))
        


if __name__ == '__main__':
    import csv
    table = []
    run_create_tests(table=table)
    run_svg_tests(table=table)
    run_png_tests(table=table)
    with open('out/results.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(table)
