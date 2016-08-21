# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Different output tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import unicode_literals, absolute_import
import io
import segno
try:
    from .test_eps import eps_as_matrix
    from .test_png import png_as_matrix
    from .test_svg import svg_as_matrix
    from .test_txt import txt_as_matrix
    from .test_pdf import pdf_as_matrix
    from .test_terminal import terminal_as_matrix
except (ValueError, SystemError):  # Attempted relative import in non-package
    from test_eps import eps_as_matrix
    from test_png import png_as_matrix
    from test_svg import svg_as_matrix
    from test_txt import txt_as_matrix
    from test_pdf import pdf_as_matrix
    from test_terminal import terminal_as_matrix


_DATA = (
    # Input string, error level, border
    ('Märchenbuch', 'M', 4),
    (123, 'H', 0),
    ('http:/www.example.org/', 'L', 3),
    ('Hello\nWorld', 'Q', 2),
    ('HELLO WORLD', 'H', 2),
    ('外来語',       'L', 0),
)


def test_data():
    # Creates a QR Code, serializes it and checks if the serialization
    # corresponds to the initial QR Code matrix.
    def check(kind, buffer_factory, to_matrix_func, data, error, border):
        """\
        :param str kind: "kind" parameter to serialize the QR code
        :param buffer_factory: Callable to construct the output buffer.
        :param to_matrix_func: Function to convert the buffer back to a matrix.
        :param data: The input to construct the QR code.
        :param error: ECC level
        :param int border: Border size.
        """
        qr = segno.make_qr(data, error=error)
        out = buffer_factory()
        qr.save(out, kind=kind, border=border)
        matrix = to_matrix_func(out, border)
        assert len(qr.matrix) == len(matrix)
        for i, row in enumerate(qr.matrix):
            assert row == bytearray(matrix[i]), 'Error in row {0}'.format(i)
    for kind, buffer_factory, to_matrix_func in (('eps', io.StringIO, eps_as_matrix),
                                                 ('png', io.BytesIO, png_as_matrix),
                                                 ('svg', io.BytesIO, svg_as_matrix),
                                                 ('txt', io.StringIO, txt_as_matrix),
                                                 ('pdf', io.BytesIO, pdf_as_matrix),
                                                 ('ans', io.StringIO, terminal_as_matrix),):
        for data, error, border in _DATA:
            yield check, kind, buffer_factory, to_matrix_func, data, error, border


if __name__ == '__main__':
    import pytest
    pytest.main(['-x', __file__])

