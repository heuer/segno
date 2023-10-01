# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2023 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests plugin loading.
"""
from __future__ import absolute_import, unicode_literals
import os
import pkg_resources
import pytest
import segno


def test_noplugin():
    qr = segno.make('The Beatles')
    with pytest.raises(AttributeError):
        qr.to_unknown_plugin()


def an_example_plugin(qrcode):
    """\
    This is a Segno converter plugin used by the next test case.
    """
    assert qrcode
    return 'works'


def test_plugin():
    distribution = pkg_resources.Distribution(os.path.dirname(__file__))
    entry_point = pkg_resources.EntryPoint.parse('test = test_plugin:an_example_plugin', dist=distribution)
    distribution._ep_map = {'segno.plugin.converter': {'test': entry_point}}
    pkg_resources.working_set.add(distribution)

    qr = segno.make('The Beatles')
    assert 'works' == qr.to_test()


if __name__ == '__main__':
    pytest.main([__file__])
