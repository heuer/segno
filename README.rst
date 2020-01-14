Segno -- Python QR Code and Micro QR Code encoder
=================================================

Segno is a QR Code and Micro QR Code encoder which has no further dependencies.

This package implements ISO/IEC 18004:2015(E) "QR Code bar code symbology
specification" and produces Micro QR Codes and QR Codes with nearly no effort.
It supports the Structured Append mode which splits a message across several
QR Codes.

Segno provides several serialization formats like Scalable Vector Graphics (SVG),
Encapsulated PostScript (EPS), Portable Network Graphics (PNG),
Portable Document Format (PDF), Portable Bitmap (PBM),
LaTeX (PGF/TikZ), X PixMap (XBM), X Bitmap (XPM) etc. None of these
serializers require an external lib.
Further, it provides several high level functions to create QR Codes which encode
`contact data (vCard, MeCard) <https://segno.readthedocs.io/en/stable/contact-information.html>`_,
`EPC QR Codes <https://segno.readthedocs.io/en/stable/epc-qrcodes.html>`_,
or `WIFI configurations <https://segno.readthedocs.io/en/stable/special-qrcode-factories.html#create-a-qr-code-for-a-wifi-configuration>`_.

The project provides more than 1400 test cases (coverage >= 98%) to verify a
standard conform QR Code and Micro QR Code generation acc. to ISO/IEC 18004:2015(E).


Unique features
---------------
* Pure Python (supports 2.7, 3.7+, PyPy2 and PyPy3)
* No dependencies
* A lot of `serialization formats <https://segno.readthedocs.io/en/stable/serializers.html#available-serializers>`_ (SVG, PNG, EPS, PDF, ...)
* `Fastest (pure Python) QR Code encoder <https://segno.readthedocs.io/en/stable/comparison-qrcode-libs.html#performance>`_
* Micro QR Codes
* `Colorful QR Codes <https://segno.readthedocs.io/en/stable/colorful-qrcodes.html>`_

  .. image:: https://github.com/heuer/segno/raw/develop/docs/_static/yellow-submarine.png
    :alt: Colorful 3-H QR Code encoding "Yellow Submarine"

  ... works also with Micro QR Codes

  .. image:: https://github.com/heuer/segno/raw/develop/docs/_static/colorful/rain.png
    :alt: Colorful M4-Q Micro QR Code encoding "Rain"
* `Structured Append mode <https://segno.readthedocs.io/en/stable/structured-append.html>`_
* `Simple, user-friendly API <https://segno.readthedocs.io/en/stable/api.html>`_
  ::

    import segno
    qr = segno.make('Yellow Submarine')
    qr.save('yellow-submarine.png')



Installation
------------

Use ``pip`` to install segno from PyPI::

    $ pip install segno


Usage
-----

Command line
^^^^^^^^^^^^

The command line script prints the QR Code to the terminal::

    $ segno "Comfortably Numb"


To serialize the QR Code, use the "output" argument::

    $ segno -o=raincoat.svg "Famous Blue Raincoat"
    $ segno --scale 10 --dark darkblue --border 0 --output=fire.svg "Who by Fire"
    $ segno --scale 10 --light transparent --output=miracle.png "Waiting for the Miracle"



Library
^^^^^^^

.. code-block:: python

    >>> import segno
    >>> # Let Segno choose the minimal version and an optimal (maximal) error
    >>> # level without changing the minimal version
    >>> qr = segno.make('Up Jumped the Devil')
    >>> qr.designator  # Returns the QR Code version and the error correction level
    '2-Q'
    >>> qr.save('up-jumped-the-devil.png')  # Save as PNG
    >>> qr.save('up-jumped-the-devil-2.png', scale=10)  # Scaling factor 10
    >>> qr.save('up-jumped-the-devil-3.png', light=None)  # Transparent light modules
    >>> qr.save('up-jumped-the-devil.pdf', scale=10)  # Save as PDF
    >>> # SVG drawing the dark modules in "dark blue"
    >>> qr.save('up-jumped-the-devil.svg', scale=10, color='darkblue')


If the content to encode is small enough, a Micro QR Code is generated:

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('RAIN')
    >>> qr.is_micro
    True
    >>> qr.designator
    'M2-M'


If this behaviour is not desired, the user may set ``micro`` to ``False``

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('RAIN', micro=False)
    >>> qr.is_micro
    False
    >>> qr.designator
    '1-H'


Or use the factory functions ``segno.make_qr()`` which generates always QR Codes
(never Micro QR Codes) or ``segno.make_micro()`` which returns always
Micro QR Codes (or raises an error if the content is too large for a Micro QR Code).

.. code-block:: python

    >>> import segno
    >>> mqr = segno.make_micro('THE BEATLES')
    >>> mqr.designator
    'M3-M'
    >>> qr = segno.make_qr('THE BEATLES')  # Same content but enforce a QR Code
    >>> qr.designator
    '1-Q'
    >>> # This won't work since the data does not fit into a Micro QR Code M1 - M4
    >>> mqr = segno.make_micro('Nick Cave and the Bad Seeds')
    Traceback (most recent call last):
        ...
    ValueError: Data too large. No Micro QR Code can handle the provided data


All factory functions use the same parameters to specify the desired error
level, version, data mask etc., see `Segno's documentation`_ for details.


Documentation
-------------
Read the online documentation at <https://segno.readthedocs.io/>


Trademark
---------
"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.


.. _Segno's documentation: https://segno.readthedocs.io/
