# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue #45.
<https://github.com/heuer/segno/issues/45>
"""
from __future__ import unicode_literals, absolute_import
from segno import cli
import pytest


def test_issue_45_error():
    with pytest.raises(SystemExit) as e:
        cli.main(['--version=M1', '--seq', '"This is a test"'])
        assert 1 == e.exception.code


def test_issue_45_error2(capsys):
    try:
        cli.main(['--version=M1', '--seq', '"This is a test"'])
    except SystemExit as ex:
        assert 1 == ex.code
        assert capsys.readouterr()


def test_issue_45_no_error():
    res = cli.main(['--version=1', '--seq', '"This is a test, test test test test"'])
    assert 0 == res


if __name__ == '__main__':
    pytest.main([__file__])

