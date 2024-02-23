"""\
Some benchmarks running against QR Code generators
"""
import sys
import os
import csv
import timeit
import segno
try:
    import qrcode
    from qrcode import QRCode, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    from qrcode.image.svg import SvgImage, SvgPathImage
except ImportError:
    qrcode = None
try:
    import qrcodegen
    from qrcodegen import QrCode, QrSegment
    qrcodegen_make_segment = QrSegment.make_segments
    qrcodegen_error_m = QrCode.Ecc.MEDIUM
    qrcodegen_error_q = QrCode.Ecc.QUARTILE
    qrcodegen_error_h = QrCode.Ecc.HIGH
except ImportError:
    qrcodegen = None


_PNG_COMPRESSION_LEVEL = 6  # Default Pillow PNG compression level


if qrcode:
    def create_qrcode(data='QR Code Symbol'):
        """qrcode create 1-M"""
        qr = QRCode(error_correction=ERROR_CORRECT_M)
        qr.add_data(data, optimize=False)
        qr.make()

    def create7q_qrcode(data='QR Code Symbol'):
        """qrcode create 7-Q"""
        qr = QRCode(error_correction=ERROR_CORRECT_Q, version=7)
        qr.add_data(data, optimize=False)
        qr.make()

    def create30h_qrcode(data='QR Code Symbol'):
        """qrcode create 30-H"""
        qr = QRCode(error_correction=ERROR_CORRECT_H, version=30)
        qr.add_data(data, optimize=False)
        qr.make()

    def svg_qrcode_path(data='QR Code Symbol'):
        """qrcode SVG path"""
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=10,
                    image_factory=SvgPathImage)
        qr.add_data(data, optimize=False)
        qr.make_image().save(os.path.join(_output_dir(), 'qrcode_path_%s.svg' % data))

    def svg_qrcode_rects(data='QR Code Symbol'):
        """qrcode SVG rects"""
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=10,
                    image_factory=SvgImage)
        qr.add_data(data, optimize=False)
        qr.make_image().save(os.path.join(_output_dir(), 'qrcode_rects_%s.svg' % data))

    def png_qrcode(data='QR Code Symbol'):
        """qrcode PNG 1-M"""
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=10)
        qr.add_data(data, optimize=False)
        qr.make_image().save(os.path.join(_output_dir(), 'qrcode_%s.png' % data),
                             compress_level=_PNG_COMPRESSION_LEVEL)

if qrcodegen:
    def create_qrcodegen(data='QR Code Symbol'):
        """qrcodegen create 1-M"""
        QrCode.encode_segments(qrcodegen_make_segment(data),
                               ecl=qrcodegen_error_m,
                               boostecl=False)

    def create7q_qrcodegen(data='QR Code Symbol'):
        """qrcodegen create 7-Q"""
        QrCode.encode_segments(qrcodegen_make_segment(data),
                               ecl=qrcodegen_error_q,
                               minversion=7,
                               maxversion=7,
                               boostecl=False)

    def create30h_qrcodegen(data='QR Code Symbol'):
        """qrcodegen create 30-H"""
        QrCode.encode_segments(qrcodegen_make_segment(data),
                               ecl=qrcodegen_error_h,
                               minversion=30,
                               maxversion=30,
                               boostecl=False)


def _output_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'out')


def create_segno(data='QR Code Symbol'):
    """Segno create 1-M"""
    segno.make_qr(data, error='m', boost_error=False)


def create7q_segno(data='QR Code Symbol'):
    """Segno create 7-Q"""
    segno.make_qr(data, error='q', version=7, boost_error=False)


def create30h_segno(data='QR Code Symbol'):
    """Segno create 30-H"""
    segno.make_qr(data, error='h', version=30, boost_error=False)


def svg_segno(data='QR Code Symbol'):
    """Segno SVG"""
    segno.make_qr(data, error='m', boost_error=False).save(os.path.join(_output_dir(), 'segno_%s.svg' % data), scale=10)


def png_segno(data='QR Code Symbol'):
    """Segno PNG 1-M"""
    segno.make_qr(data, error='m', boost_error=False).save(os.path.join(_output_dir(), 'segno_%s.png' % data), scale=10,
                                                           compresslevel=_PNG_COMPRESSION_LEVEL)


def run_create_tests(which=None, number=200, table=None):
    tests = ('create_qrcodegen',
             'create_qrcode',
             'create_segno',)
    if which:
        tests = filter(lambda n: n[len('create_'):] in which, tests)
    _run_tests(tests, number, table)


# def run_create7q_tests(which=None, number=200, table=None):
#     tests = ('create7q_qrcodegen',
#              'create7q_qrcode',
#              'create7q_segno',)
#     if which:
#         tests = filter(lambda n: n[len('create7q_'):] in which, tests)
#     _run_tests(tests, number, table)


# def run_create30h_tests(which=None, number=200, table=None):
#     tests = ('create30h_qrcodegen',
#              'create30h_qrcode',
#              'create30h_segno',)
#     if which:
#         tests = filter(lambda n: n[len('createbig_'):] in which, tests)
#     _run_tests(tests, number, table)


# def run_svg_tests(which=None, number=200, table=None):
#     tests = ('svg_qrcode_path', 'svg_qrcode_rects',
#              'svg_segno',)

#     if which:
#         tests = filter(lambda n: n[len('svg_'):] in which, tests)
#     _run_tests(tests, number, table)


def run_png_tests(which=None, number=200, table=None):
    tests = ('png_qrcode',
             'png_segno',)
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
    table = []
    run_create_tests(table=table)
    #run_create7q_tests(table=table)
    #run_create30h_tests(table=table)
    #run_svg_tests(table=table)
    run_png_tests(table=table)
    with open(os.path.join(_output_dir(), 'results.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)
