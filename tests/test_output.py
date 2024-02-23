#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Different output tests.
"""
import io
import pytest
import segno
try:
    from .test_eps import eps_as_matrix
    from .test_png import png_as_matrix
    from .test_svg import svg_as_matrix
    from .test_txt import txt_as_matrix
    from .test_pdf import pdf_as_matrix
    from .test_terminal import terminal_as_matrix
    from .test_pbm import pbm_p1_as_matrix
    from .test_pam import pam_bw_as_matrix
    from .test_ppm import ppm_bw_as_matrix
    from .test_tex import tex_as_matrix
    from .test_xpm import xpm_as_matrix
# Attempted relative import in non-package
except (ValueError, SystemError, ImportError):
    from test_eps import eps_as_matrix
    from test_png import png_as_matrix
    from test_svg import svg_as_matrix
    from test_txt import txt_as_matrix
    from test_pdf import pdf_as_matrix
    from test_terminal import terminal_as_matrix
    from test_pbm import pbm_p1_as_matrix
    from test_pam import pam_bw_as_matrix
    from test_ppm import ppm_bw_as_matrix
    from test_tex import tex_as_matrix
    from test_xpm import xpm_as_matrix


_DATA = (
    # Input string, error level, border
    ('Märchenbuch', 'M', 4),
    (123, 'H', 0),
    ('http:/www.example.org/', 'L', 3),
    ('Hello\nWorld', 'Q', 2),
    ('HELLO WORLD', 'H', 2),
    ('外来語',       'L', 0),
)


def _make_test_data_input():
    for kind, buffer_factory, to_matrix_func, kw in (
        ('eps', io.StringIO, eps_as_matrix, {}),
        ('png', io.BytesIO, png_as_matrix, {}),
        ('svg', io.BytesIO, svg_as_matrix, {}),
        ('txt', io.StringIO, txt_as_matrix, {}),
        ('pdf', io.BytesIO, pdf_as_matrix, {}),
        ('ans', io.StringIO, terminal_as_matrix, {}),
        ('tex', io.StringIO, tex_as_matrix, {}),
        ('xpm', io.StringIO, xpm_as_matrix, {}),
        ('pam', io.BytesIO, pam_bw_as_matrix, {}),
        ('pbm', io.BytesIO, pbm_p1_as_matrix, dict(plain=True)),
        ('ppm', io.BytesIO, ppm_bw_as_matrix, {}),
    ):
        for data, error, border in _DATA:
            yield kind, buffer_factory, to_matrix_func, data, error, border, kw


@pytest.mark.parametrize('kind, buffer_factory, to_matrix_func, data, error, '
                         'border, kw',
                         _make_test_data_input())
def test_data(kind, buffer_factory, to_matrix_func, data, error, border, kw):
    # Creates a QR Code, serializes it and checks if the serialization
    # corresponds to the initial QR Code matrix.
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
    qr.save(out, kind=kind, border=border, **kw)
    matrix = to_matrix_func(out, border)
    assert len(qr.matrix) == len(matrix)
    for i, row in enumerate(qr.matrix):
        exptected_row = bytearray(matrix[i])
        assert len(row) == len(exptected_row)
        assert exptected_row == row, f'Error in row {i}'


if __name__ == '__main__':
    pytest.main([__file__])
