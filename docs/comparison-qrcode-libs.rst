Comparison of Python QR Code libraries
======================================

Features
--------

============================================    ==================    ===================    ==================    ========
Description                                     `qrcode`_             `PyQRCode`_            `qrcodegen`_          `Segno`_
============================================    ==================    ===================    ==================    ========
Library license                                 `BSD`_                  `BSD`_               `MIT`_                `BSD`_
Library version                                 5.3                   1.2.1                  1.0.0                 0.1.7
Mode Numeric                                    Yes                   Yes                    Yes                   Yes
Mode Alphanumeric                               Yes                   Yes                    Yes                   Yes
Mode Byte                                       Yes                   Yes                    Yes                   Yes
Mode Kanji                                      No                    Yes                    No                    Yes
Mode ECI                                        No                    No                     Yes                   Yes
Mode FNC1                                       No                    No                     No                    No
Mode Structured Append                          No                    No                     No                    No
Mixing modes                                    Yes                   No                     Yes                   Yes
QR Codes version 1 - 40                         Yes                   Yes                    Yes                   Yes
Micro QR Codes version M1 - M4                  No                    No                     No                    Yes
Output acc. to ISO/IEC 18004:2015(E) Fig. 1     No                    No                     No                    Yes
Output acc. to ISO/IEC 18004:2015(E) I.3.       No (not available)    No (not available)     No (not available)    Yes
Find best error correction level                No                    No                     Yes                   Yes
`PNG`_ output                                   Yes                   Yes                    No                    Yes
`SVG`_ output                                   Yes                   Yes                    Yes                   Yes
`EPS`_ output                                   Yes                   Yes                    No                    Yes
`PDF`_ output                                   Yes                   No                     No                    Yes
`XPM`_ output                                   No                    Yes                    No                    No
PNG `data URI`_                                 No                    kind of (not a URI)    No                    Yes
SVG data URI                                    No                    No                     No                    Yes
Text output                                     Yes                   Yes                    No                    Yes
`ANSI`_ escape code output                      Yes                   Yes                    No                    Yes
Other output formats (i.e. `JPEG`_)             Yes                   No                     No                    No, but via `PIL plugin`_
Black and white QR Codes                        Yes                   Yes                    Yes                   Yes
Colored QR Codes                                No                    Yes                    No                    Yes
Changing size of modules (scaling factor)       Yes                   Yes                    No                    Yes
Command line script                             Yes                   No                     No                    Yes
Plugins                                         No                    No                     No                    Yes
Default encoding in Byte mode                   UTF-8                 ISO/IEC 8859-1         UTF-8                 ISO/IEC 8859-1
                                                                      or UTF-8                                     or UTF-8
3rd party dependencies                          `six`_,               `PyPNG`_               -                     -
                                                `Pillow`_ or
                                                `Pymaging`_ and
                                                `Pymaging-PNG`_
                                                (Windows:
                                                `colorama`_)
============================================    ==================    ===================    ==================    ========


Performance
-----------

Some performance indicators. The script `benchmark.py`_ ran on a
MacBook Air 2,13 Core2 Duo using CPython 2.7.10. Each SVG / PNG image uses a
scaling factor of 10 (aside from qrcodegen which does not support any scaling).


Create a QR Code
^^^^^^^^^^^^^^^^

Create a 1-M QR Code "QR Code Symbol".

.. image:: _static/chart_create.svg
    :alt: Chart showing the results of creating a 1-M QR Code.


Create a QR Code and serialize it as SVG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a QR Code 1-M "QR Code Symbol" and serialize it as SVG document.


.. image:: _static/chart_svg.svg
    :alt: Chart showing the results of creating a 1-M QR Code and export it as SVG image.



Create a QR Code and serialize it as PNG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a QR Code 1-M "QR Code Symbol" and serialize it as PNG image.

.. image:: _static/chart_png.svg
    :alt: Chart showing the results of creating a 1-M QR Code and export it as SVG image.


.. _qrcode: https://pypi.python.org/pypi/qrcode/
.. _PyQRCode: https://pypi.python.org/pypi/PyQRCode/
.. _qrcodegen: https://pypi.python.org/pypi/qrcodegen/
.. _Segno: https://pypi.python.org/pypi/segno/
.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _MIT: http://opensource.org/licenses/MIT
.. _PNG: https://en.wikipedia.org/wiki/Portable_Network_Graphics
.. _SVG: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
.. _EPS: https://en.wikipedia.org/wiki/Encapsulated_PostScript
.. _PDF: https://en.wikipedia.org/wiki/Portable_Document_Format
.. _XPM: https://en.wikipedia.org/wiki/X_PixMap
.. _data URI: https://en.wikipedia.org/wiki/Data_URI_scheme
.. _ANSI: https://en.wikipedia.org/wiki/ANSI_escape_code
.. _JPEG: https://en.wikipedia.org/wiki/JPEG
.. _six: https://pypi.python.org/pypi/six/
.. _PyPNG: https://pypi.python.org/pypi/pypng/
.. _Pymaging: https://github.com/ojii/pymaging
.. _Pymaging-PNG: https://github.com/ojii/pymaging-png
.. _PIL: http://pythonware.com/products/pil/
.. _Pillow: https://python-pillow.github.io/
.. _colorama: https://pypi.python.org/pypi/colorama
.. _PIL plugin: https://github.com/heuer/segno-pil
.. _benchmark.py: https://github.com/heuer/segno/sandbox/benchmark.py
