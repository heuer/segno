#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Terminal output related tests.
"""
import io
import re
import pytest
import segno


def test_terminal():
    # Test with default options
    qr = segno.make_qr('test')
    # Upper left finder pattern: 7 dark modules + 1 light module
    expected = '\033[49m' + '  ' * 7 + '\033[0m\033[7m '
    out = io.StringIO()
    qr.terminal(out, border=0)
    val = out.getvalue()
    assert expected == val[:len(expected)]


def test_terminal_compact():
    # Test compact half-block terminal QR.
    qr = segno.make_qr('test')
    out = io.StringIO()
    qr.terminal(out, border=0, compact=True)
    val = out.getvalue()
    expected = """\
 ▄▄▄▄▄ █ ▀ ▀▀█ ▄▄▄▄▄ 
 █   █ █▄██  █ █   █ 
 █▄▄▄█ █▀ ▀███ █▄▄▄█ 
▄▄▄▄▄▄▄█ ▀ █ █▄▄▄▄▄▄▄
▀▀▄  ▀▄▀ ▀█▄▄ ▄▄█▀ ▄ 
█ ▄▄ █▄ ▀▀ ▀▄█ ▄█  ▄█
▄▄██▄█▄█▀▀ ▄██▀ █▄▀ ▀
 ▄▄▄▄▄ ██ ▀▄ █▀▀  ▀▄█
 █   █ █ ▀   ▀▀▀▄ ▀▄█
 █▄▄▄█ █▄█▄▄ █▄ ██ ██
       ▀▀ ▀▀  ▀ ▀▀  ▀
"""  # noqa: W291
    assert expected == val


def terminal_as_matrix(buff, border):
    """\
    Returns the text QR code as list of [0,1] lists.
    """
    color_pattern = re.compile(r'(\033\[\d+m)(\s+)\033\[0m')
    res = []
    colors = ('\033[7m', '\033[49m')
    code = buff.getvalue().splitlines()
    for line in code[border:len(code) - border]:
        row = []
        for m in color_pattern.finditer(line):
            bit = colors.index(m.group(1))
            bit_count = len(m.group(2)) // 2  # 2 chars for 1 module!
            if m.start() == 0 or m.end() == len(line):
                bit_count -= border
            row.extend([bit] * bit_count)
        res.append(row)
    return res


if __name__ == '__main__':
    pytest.main([__file__])
