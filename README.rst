.. image:: https://app.travis-ci.com/heuer/segno.svg?branch=master
    :target: https://app.travis-ci.com/heuer/segno

QR Code encoder and Micro QR Code encoder
=========================================

Pure Python QR Code generator with no dependencies.

This package implements ISO/IEC 18004:2015(E) "QR Code bar code symbology
specification" and produces QR Codes and Micro QR Codes with nearly no effort.
It supports the `Structured Append mode <https://segno.readthedocs.io/en/stable/structured-append.html>`_
which splits a message across several QR codes.

Segno (Italian for "sign" / "symbol") provides several serialization formats
like Scalable Vector Graphics (SVG), Encapsulated PostScript (EPS),
Portable Network Graphics (PNG), Portable Document Format (PDF), Netpbm (PAM, PBM, PPM),
LaTeX (PGF/TikZ), X PixMap (XBM), and X Bitmap (XPM) etc.
None of these serializers require an external lib.
Further, it provides several high level functions to create QR Codes which encode
`contact data (vCard, MeCard) <https://segno.readthedocs.io/en/stable/contact-information.html>`_,
`EPC QR Codes <https://segno.readthedocs.io/en/stable/epc-qrcodes.html>`_,
or `WIFI QR Codes <https://segno.readthedocs.io/en/stable/special-qrcode-factories.html#create-a-qr-code-for-a-wifi-configuration>`_.

The project provides more than 1500 test cases (coverage >= 98%) to verify a
standard conform QR Code and Micro QR Code generation acc. to ISO/IEC 18004:2015(E).


Unique features
---------------
* Pure Python QR Code generator (supports 2.7, 3.5+, PyPy2 and PyPy3)
* No dependencies
* A lot of `serialization formats <https://segno.readthedocs.io/en/stable/serializers.html#available-serializers>`_ (SVG, PNG, EPS, PDF, ...)
* `Fastest (pure Python) QR Code encoder <https://segno.readthedocs.io/en/stable/comparison-qrcode-libs.html#performance>`_
* Micro QR Codes
* `Structured Append mode <https://segno.readthedocs.io/en/stable/structured-append.html>`_
* `Hanzi mode <https://segno.readthedocs.io/en/stable/qrcode-modes.html#hanzi-mode>`_
* `Command line interface <https://segno.readthedocs.io/en/stable/command-line.html>`_
* `Simple, user-friendly API <https://segno.readthedocs.io/en/stable/make.html>`_

.. code-block:: python

    import segno
    qrcode = segno.make('Yellow Submarine')
    qrcode.save('yellow-submarine.png')

* `Colorful QR codes <https://segno.readthedocs.io/en/stable/colorful-qrcodes.html>`_

  .. image:: https://github.com/heuer/segno/raw/master/docs/_static/colorful/qrcode_yellow-submarine.png
    :alt: Colorful 7-H QR code encoding "Yellow Submarine"

  ... works also with Micro QR codes

  .. image:: https://github.com/heuer/segno/raw/master/docs/_static/colorful/micro_qrcode_rain.png
    :alt: Colorful M4-Q Micro QR code encoding "Rain"

* `Artistic QR Codes <https://segno.readthedocs.io/en/stable/artistic-qrcodes.html>`_
  (requires the `qrcode-artistic <https://github.com/heuer/qrcode-artistic>`_ plug-in)

  .. image:: https://github.com/heuer/segno/raw/master/docs/_static/artistic/letitbe.jpg
    :alt: Animated 3-H QR code encoding "The Beatles -- Let It Be"

  ... animated QR codes are supported as well

  .. image:: https://github.com/heuer/segno/raw/master/docs/_static/artistic/abbey-road.webp
    :alt: Animated 4-H QR code encoding "The Beatles -- Abbey Road"


Installation
------------

Use ``pip`` to install segno from PyPI::

    $ pip install segno


MacPorts
^^^^^^^^

Segno is also available at `MacPorts <https://www.macports.org/>`_
(`MacPorts project page <https://ports.macports.org/port/py-segno/>`_)::

    $ sudo port install py-segno


conda-forge
^^^^^^^^^^^

The library is also available at `conda-forge <https://conda-forge.org/>`_
(`conda-forge project page <https://anaconda.org/conda-forge/segno>`_)::

    $ conda install -c conda-forge segno


Debian 11 / Bullseye
^^^^^^^^^^^^^^^^^^^^

::

    $ apt-get install python3-segno


Debian 10 / Buster (backports)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ apt-get -t buster-backports install python3-segno


Arch Linux
^^^^^^^^^^

::

    $ pacman -S python-segno



Usage
-----

Command line
^^^^^^^^^^^^

The command line script prints a QR code to the terminal::

    $ segno "Comfortably Numb"


To serialize a QR code, use the "output" argument::

    $ segno -o=raincoat.svg "Famous Blue Raincoat"
    $ segno --scale 10 --dark darkblue --border 0 --output=fire.svg "Who by Fire"
    $ segno --scale 10 --light transparent --output=miracle.png "Waiting for the Miracle"



Library
^^^^^^^

.. code-block:: python

    >>> import segno
    >>> # Let Segno choose the minimal version and an optimal (maximal) error
    >>> # level without changing the minimal version
    >>> qrcode = segno.make('Up Jumped the Devil')
    >>> qrcode.designator  # Returns the QR code version and the error correction level
    '2-Q'
    >>> qrcode.save('up-jumped-the-devil.png')  # Save as PNG
    >>> qrcode.save('up-jumped-the-devil-2.png', scale=10)  # Scaling factor 10
    >>> qrcode.save('up-jumped-the-devil-3.png', light=None)  # Transparent light modules
    >>> qrcode.save('up-jumped-the-devil.pdf', scale=10)  # Save as PDF
    >>> # SVG drawing the dark modules in "dark blue"
    >>> qrcode.save('up-jumped-the-devil.svg', scale=10, dark='darkblue')


If the content to encode is small enough, a Micro QR code is generated:

.. code-block:: python

    >>> import segno
    >>> qrcode = segno.make('RAIN')
    >>> qrcode.is_micro
    True
    >>> qrcode.designator
    'M2-M'


If this behaviour is not desired, the user may set ``micro`` to ``False``

.. code-block:: python

    >>> import segno
    >>> qrcode = segno.make('RAIN', micro=False)
    >>> qrcode.is_micro
    False
    >>> qrcode.designator
    '1-H'


Or use the factory functions ``segno.make_qr()`` which generates always QR codes
(never Micro QR codes) or ``segno.make_micro()`` which returns always
Micro QR codes (or raises an error if the content is too large for a Micro QR code).

.. code-block:: python

    >>> import segno
    >>> qrcode_micro = segno.make_micro('THE BEATLES')
    >>> qrcode_micro.designator
    'M3-M'
    >>> qrcode = segno.make_qr('THE BEATLES')  # Same content but enforce a QR Code
    >>> qrcode.designator
    '1-Q'
    >>> # This won't work since the data does not fit into a Micro QR Code M1 - M4
    >>> micro_qrcode = segno.make_micro('Nick Cave and the Bad Seeds')
    Traceback (most recent call last):
        ...
    DataOverflowError: Data too large. No Micro QR Code can handle the provided data


All factory functions use the same parameters to specify the desired error
level, version, data mask etc., see `Segno's documentation`_ for details.


Documentation
-------------
Read the online documentation at <https://segno.readthedocs.io/>


Trademark
---------
"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.


.. _Segno's documentation: https://segno.readthedocs.io/
