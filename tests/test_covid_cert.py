#
# Copyright (c) 2016 - 2024 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tests if Segno produces the correct Covid certificate QR Code

See
* <https://github.com/Digitaler-Impfnachweis/covpass-android/issues/93>
* <https://github.com/lincolnloop/python-qrcode/issues/244>
"""
import segno
try:
    from .tutils import read_matrix
# Attempted relative import in non-package
except (ValueError, SystemError, ImportError):
    from tutils import read_matrix


def test_covid_cert():
    cert_raw = "HC1:6BFOXN*TS0BI$ZD8UH76PCM7ZJ7GZ20II/P3 43JUB/EBUMIU/3%$C2L9KST--M:UC*GPXS40 LHZA KEW%G%9DJ6K1AD1WMN" \
               "+I0JK1WLB4DCHGLII3LN25OVLNF7LHCIZ09.9DM*GC9M$7JE9MZIIDOM1JAF.7IFNDXI03L9ZI4Q5%H0AN8EH06YB-TIP+P6OIB.V" \
               "T*QNC2BFUF$SU%BO*N5PIBPIAOI-+R2YBV44PZB6H0CJ0QCK0YQK*R3T3+7A.N88J4R$F/MAITH6QS03L0QIRR97I2HOAXL92L0. " \
               "KOKGTM8$M8SNCT64RR7+V4YC5/HQRPOHCR6W9.DPEA7IB65C94JB+ONS.CUIA7LE9JAF+B**O3-SY$NRUEG1AK/4C6DM.SY$NWYMG" \
               "3GUBRCEIFRMLNKNM8POCJPG8/0NOLZGIZCUOY55*LTUJS1D7.J9$7$.IWQOMJV$6M53AA:6Z2S./BXPHRKGJUHB1WN5LH/M0:3P+E" \
               "$$BWWNB8V5ZRF9JMKAX AAOL3H02YF*OF"
    # Don't use another error correction mode than "M", not sure if this is a requirement, though
    qr = segno.make(cert_raw, error='m', boost_error=False)
    assert 'M' == qr.error
    assert 15 == qr.version
    ref_matrix = read_matrix('covid-cert')[0]
    assert ref_matrix
    assert ref_matrix == qr.matrix


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
