#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against issue 35
<https://github.com/heuer/segno/issues/35>
"""
import pytest
from segno import consts
from segno import encoder


@pytest.mark.parametrize('version, mask', [(consts.VERSION_M1, 4),
                                           (1, 8),
                                           (1, -1),
                                           (consts.VERSION_M2, -1)])
def test_normalize_mask_illegal(version, mask):
    with pytest.raises(ValueError) as ex:
        encoder.normalize_mask(mask, version < 1)
    assert 'Invalid data mask' in str(ex.value)


@pytest.mark.parametrize('version, mask', [(consts.VERSION_M1, 'A'),
                                           (1, 'B')])
def test_normalize_mask_not_int(version, mask):
    with pytest.raises(ValueError) as ex:
        encoder.normalize_mask(mask, version < 1)
    assert 'Invalid data mask' in str(ex.value)


if __name__ == '__main__':
    pytest.main([__file__])
