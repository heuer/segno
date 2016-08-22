# -*- encoding: utf-8 -*-
"""\
Some benchmarks running against QR Code generators
"""
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
        qr.add_data(data)
        qr.make()

    def svg_qrcode_path(data='QR Code Symbol'):
        """qrcode SVG path"""
        qrcode.make(data, error_correction=qrcode.ERROR_CORRECT_M,
                    box_size=10,
                    image_factory=SvgPathImage) \
            .save('out/qrcode_path_%s.svg' % data)

    def svg_qrcode_rects(data='QR Code Symbol'):
        """qrcode SVG rects"""
        qrcode.make(data, error_correction=qrcode.ERROR_CORRECT_M,
                    box_size=10,
                    image_factory=SvgImage) \
            .save('out/qrcode_rects_%s.svg' % data)

    def png_qrcode(data='QR Code Symbol'):
        """qrcode PNG"""
        qrcode.make(data, error_correction=qrcode.ERROR_CORRECT_M,
                    box_size=10) \
            .save('out/qrcode_%s.png' % data)


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
    segno.make_qr(data, error='m').save('out/segno_%s.png' % data, scale=10)


def run_create_tests(which=None, number=500):
    tests = ('create_segno', 'create_pyqrcode', 'create_qrcodegen',
             'create_qrcode')
    if which:
        tests = filter(lambda n: n[len('create_'):] in which, tests)
    _run_tests(tests, number)


def run_svg_tests(which=None, number=500):
    tests = ('svg_segno', 'svg_pyqrcode', 'svg_qrcodegen',
             'svg_qrcode_path', 'svg_qrcode_rects')

    if which:
        tests = filter(lambda n: n[len('svg_'):] in which, tests)
    _run_tests(tests, number)


def run_png_tests(which=None, number=500):
    tests = ('png_segno', 'png_pyqrcode', 'png_qrcode')
    if which:
        tests = filter(lambda n: n[len('png_'):] in which, tests)
    _run_tests(tests, number)


def _run_tests(tests, number):
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
        print '%-35s %s' % (getattr(sys.modules[__name__], test).__doc__, result)


if __name__ == '__main__':
    run_create_tests()
    run_svg_tests()
    run_png_tests()
