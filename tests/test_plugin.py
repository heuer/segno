#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests plugin loading.
"""
import pytest
import segno


def test_noplugin():
    qr = segno.make('The Beatles')
    with pytest.raises(AttributeError):
        qr.to_unknown_plugin()


def test_plugin():
    qr = segno.make('The Beatles')
    assert qr.to_pil() is not None


if __name__ == '__main__':
    pytest.main([__file__])
