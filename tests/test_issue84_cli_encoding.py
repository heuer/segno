#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue #84.
<https://github.com/heuer/segno/issues/84>
"""
import os
import tempfile
from segno import cli
import pytest


def test_issue_84_default_encoding():
    with open(os.path.join(os.path.dirname(__file__), 'issue-84',
                           'issue-84-iso-8859-1.txt')) as f:
        expected = f.read()
    f = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False)
    f.close()
    try:
        cli.main(['-o', f.name, 'Müller'])
        with open(f.name) as f:
            result = f.read()
        assert expected == result
        # Explicit but default encoding
        cli.main(['-o', f.name, '--encoding', 'iso-8859-1', 'Müller'])
        with open(f.name) as f:
            result = f.read()
        assert expected == result
        # Explicit but default encoding
        cli.main(['-o', f.name, '--encoding', 'latin1', 'Müller'])
        with open(f.name) as f:
            result = f.read()
        assert expected == result
    finally:
        os.unlink(f.name)


def test_issue_84_utf8():
    with open(os.path.join(os.path.dirname(__file__), 'issue-84',
                           'issue-84-utf-8.txt')) as f:
        expected = f.read()
    f = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False)
    f.close()
    try:
        cli.main(['-o', f.name, '--encoding', 'utf-8', 'Müller'])
        with open(f.name) as f:
            result = f.read()
        assert expected == result
        cli.main(['-o', f.name, '--encoding', 'UTf-8', 'Müller'])
        with open(f.name) as f:
            result = f.read()
        assert expected == result
    finally:
        os.unlink(f.name)


if __name__ == '__main__':
    pytest.main([__file__])
