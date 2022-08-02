Comparison of Python QR Code libraries
======================================

Features
--------

.. |br| raw:: html

    <br>

.. table::
    :class: pylib-comparison

    ================================================================    =====================    ======================    ========
    Description                                                         `qrcode`_                `qrcodegen`_              `Segno`_
    ================================================================    =====================    ======================    ========
    Library license                                                     `BSD`_                   `MIT`_                    `BSD`_
    Library version                                                     7.3.1                    1.7.0                     |version|
    Mode Numeric                                                        Yes                      Yes                       Yes
    Mode Alphanumeric                                                   Yes                      Yes                       Yes
    Mode Byte                                                           Yes                      Yes                       Yes
    Mode Kanji                                                          No                       Yes                       Yes
    Mode ECI                                                            No                       Yes                       Yes
    Mode FNC1                                                           No                       No                        No
    Mode Structured Append                                              No                       No                        Yes
    Mode Hanzi [1]_                                                     No                       No                        Yes
    Mixing modes                                                        Yes                      Yes                       Yes
    QR Codes version 1 - 40                                             Yes                      Yes                       Yes
    Micro QR Codes version M1 - M4                                      No                       No                        Yes
    Output acc. to ISO/IEC 18004:2015(E) Fig. 1 [2]_ |br| |ISO 1-M|     No |br| |mask4 1-M|      No |br| |mask4 1-M|       Yes |br| |segno 1-M|
    Output acc. to ISO/IEC 18004:2015(E) Fig. 2 |br| |ISO M2-L|         -                        -                         Yes |br| |segno M2-L|
    Find maximal error correction level                                 No                       Yes                       Yes
    Optimize QR Codes                                                   Yes                      No                        No
    `PNG`_ output                                                       Yes                      No                        Yes
    `SVG`_ output                                                       Yes                      No                        Yes
    `EPS`_ output                                                       Yes                      No                        Yes
    `PDF`_ output                                                       Yes                      No                        Yes
    `PAM`_ output                                                       No                       No                        Yes
    `PBM`_ output                                                       Yes                      No                        Yes
    `PPM`_ output                                                       Yes                      No                        Yes
    `LaTeX`_ support                                                    No                       No                        Yes
    `XBM`_ output                                                       Yes                      No                        Yes
    `XPM`_ output                                                       No                       No                        Yes
    PNG `data URI`_                                                     No                       No                        Yes
    SVG data URI                                                        No                       No                        Yes
    Text output                                                         Yes                      No                        Yes
    `ANSI`_ escape code output                                          Yes                      No                        Yes
    Other output formats (i.e. `JPEG`_)                                 Yes                      No                        Yes via `plugin`_
    Black and white QR Codes                                            Yes                      Yes                       Yes
    Colored QR Codes                                                    Yes                      No                        Yes
    Animated QR Codes (`GIF`_, `APNG`_, `WebP`_)                        No                       No                        Yes via `plugin`_
    Changing size of modules (scaling factor)                           Yes                      No                        Yes
    Command line script                                                 Yes                      No                        Yes
    Plugins                                                             No                       No                        Yes
    Default encoding in Byte mode                                       ISO/IEC 8859-1           ISO/IEC 8859-1            ISO/IEC 8859-1
                                                                        or UTF-8                 or UTF-8                  or UTF-8
    3rd party dependencies                                              `Pillow`_ or             -                         -
                                                                        `Pymaging`_ and
                                                                        `Pymaging-PNG`_
                                                                        (Windows:
                                                                        `colorama`_)
    ================================================================    =====================    ======================    ========

.. [1] The Hanzi mode is not part of ISO/IEC 18004 and may not be supported by all QR Code decoders.
       Segno uses the Hanzi mode if the user enables it explicitly, see :ref:`hanzi-mode` for details

.. [2] Even if all libs generate the same byte output (``40 e5 15 22 04 36 f6 46 52 05 37 96 d6 26 f6 c0``)
       for the input "QR Code Symbol", the generated QR code may look different because they choose a different
       mask pattern.
       ISO/IEC 18004:2015(E) (cf. page 7) uses mask 5, while qrcode and qrcodegen use mask 4.
       All these QR codes can be read by common QR Code readers.


Performance
-----------

Some performance indicators. The script `benchmarks.py`_ ran on
Intel i7-8559U / CPython 3.7. Each SVG / PNG image uses a
scaling factor of 10 (aside from qrcodegen which does not support any scaling).


Create a 1-M QR code
~~~~~~~~~~~~~~~~~~~~

1-M QR code encoding "QR Code Symbol"

.. image:: _static/chart_create_1m.svg
    :alt: Chart showing the results of creating a 1-M QR code.


Create a 7-Q QR code
~~~~~~~~~~~~~~~~~~~~

7-Q QR code encoding "QR Code Symbol"

.. image:: _static/chart_create_7q.svg
    :alt: Chart showing the results of creating a 7-Q QR code.


Create a 30-H QR code
~~~~~~~~~~~~~~~~~~~~~

30-H QR code encoding "QR Code Symbol"

.. image:: _static/chart_create_30h.svg
    :alt: Chart showing the results of creating a 30-H QR code.


Create a QR code and serialize it as SVG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a QR code 1-M "QR Code Symbol" and serialize it as SVG document.


.. image:: _static/chart_svg.svg
    :alt: Chart showing the results of creating a 1-M QR code and export it as SVG image.


Create a QR code and serialize it as PNG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a QR code 1-M "QR Code Symbol" and serialize it as PNG image.

.. image:: _static/chart_png.svg
    :alt: Chart showing the results of creating a 1-M QR code and export it as SVG image.


.. |ISO 1-M| image:: _static/iso_fig1_1m.png
    :alt: 1-M QR code encoding 'QR Code Symbol'
    :width: 87
    :height: 87

.. |ISO M2-L| image:: _static/iso_fig2_m2l.png
    :alt: M2-L Micro QR code encoding '01234567'
    :width: 51
    :height: 51

.. |mask4 1-M| image:: _static/iso_fig1_1m_mask4.png
    :alt: 1-M QR code encoding 'QR Code Symbol' using mask 4
    :width: 87
    :height: 87

.. |segno 1-M| image:: _static/iso_fig1_1m_segno.png
    :alt: 1-M QR code encoding 'QR Code Symbol' using mask 5
    :width: 87
    :height: 87

.. |segno M2-L| image:: _static/iso_fig2_m2l_segno.png
    :alt: M2-L Micro QR code encoding '01234567'
    :width: 51
    :height: 51


The comparison included PyQRCode in all years before 2022. In the meantime, six
years have passed without any updates and PyQRCode has lost its connection in
many aspects.

Although popular, it lost all feature and performance comparisons, therefore it
is no longer part of this comparison.


.. _qrcode: https://pypi.org/project/qrcode/
.. _qrcodegen: https://pypi.org/project/qrcodegen/
.. _Segno: https://pypi.org/project/segno/
.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _MIT: http://opensource.org/licenses/MIT
.. _PNG: https://en.wikipedia.org/wiki/Portable_Network_Graphics
.. _SVG: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
.. _EPS: https://en.wikipedia.org/wiki/Encapsulated_PostScript
.. _PDF: https://en.wikipedia.org/wiki/Portable_Document_Format
.. _XBM: https://en.wikipedia.org/wiki/X_BitMap
.. _XPM: https://de.wikipedia.org/wiki/X_PixMap
.. _PAM: http://netpbm.sourceforge.net/doc/pam.html
.. _PBM: http://netpbm.sourceforge.net/doc/pbm.html
.. _PPM: http://netpbm.sourceforge.net/doc/ppm.html
.. _LaTeX: https://en.wikipedia.org/wiki/LaTeX
.. _data URI: https://en.wikipedia.org/wiki/Data_URI_scheme
.. _ANSI: https://en.wikipedia.org/wiki/ANSI_escape_code
.. _JPEG: https://en.wikipedia.org/wiki/JPEG
.. _six: https://pypi.org/project/six/
.. _PyPNG: https://pypi.org/project/pypng/
.. _Pymaging: https://github.com/ojii/pymaging
.. _Pymaging-PNG: https://github.com/ojii/pymaging-png
.. _PIL: https://pypi.org/project/PIL/
.. _Pillow: https://pypi.org/project/Pillow/
.. _colorama: https://pypi.org/project/colorama/
.. _plugin: https://github.com/heuer/qrcode-artistic
.. _benchmarks.py: https://github.com/heuer/segno/blob/master/sandbox/benchmarks.py
.. _GIF: https://en.wikipedia.org/wiki/GIF#Animated_GIF
.. _APNG: https://en.wikipedia.org/wiki/Animated_Portable_Network_Graphics
.. _WebP: https://en.wikipedia.org/wiki/WebP
