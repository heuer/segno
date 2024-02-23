#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Issue <https://github.com/heuer/segno/issues/128>

Don't include blank vcard/mecard fields.
"""
import pytest
from segno import helpers


def test_mecard_data():
    mecard = helpers.make_mecard_data(name='Mustermann,Max', phone=[])
    assert 'MECARD:N:Mustermann,Max;;' == mecard
    mecard = helpers.make_mecard_data(name='Mustermann,Max', email="")
    assert 'MECARD:N:Mustermann,Max;;' == mecard


def test_vcard_data():
    res = 'BEGIN:VCARD\r\n' \
          'VERSION:3.0\r\n' \
          'N:Mustermann;Max\r\n' \
          'FN:Max Mustermann\r\n' \
          'END:VCARD\r\n'
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann', phone="")
    assert res == vcard
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann', email="")
    assert res == vcard
    vcard = helpers.make_vcard_data('Mustermann;Max', 'Max Mustermann', fax="")
    assert res == vcard


if __name__ == '__main__':
    pytest.main([__file__])
