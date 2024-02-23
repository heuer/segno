#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 39
<https://github.com/heuer/segno/issues/39>
"""
import os
import io
import tempfile
import pytest
import segno
from segno import cli


def test_output():
    out = io.BytesIO()
    segno.make_qr('Good Times', error='M').save(out, kind='png', scale=10,
                                                dark='red')
    f = tempfile.NamedTemporaryFile('w', suffix='.png', delete=False)
    f.close()
    cli.main(['-e=M', '--scale=10', '--dark=red', f'--output={f.name}',
              'Good Times'])
    f = open(f.name, 'rb')
    content = f.read()
    f.close()
    os.unlink(f.name)
    assert out.getvalue() == content


def test_output2():
    out = io.BytesIO()
    segno.make_qr('Good Times', error='M').save(out, kind='png', scale=10,
                                                dark='red')
    f = tempfile.NamedTemporaryFile('w', suffix='.png', delete=False)
    f.close()
    cli.main(['-e=M', '--scale=10', '--dark=red', f'--output={f.name}',
              'Good', 'Times'])
    f = open(f.name, 'rb')
    content = f.read()
    f.close()
    os.unlink(f.name)
    assert out.getvalue() == content


if __name__ == '__main__':
    pytest.main([__file__])
