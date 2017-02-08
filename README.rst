Segno -- Python QR Code and Micro QR Code encoder
=================================================

Segno is a QR Code and Micro QR Code encoder which has no further dependencies.

This package implements ISO/IEC 18004:2006(E) / ISO/IEC 18004:2015(E) "QR Code bar
code symbology specification" and produces Micro QR Codes and QR Codes with
nearly no effort.

Segno provides several serialization formats like Scalable Vector Graphics (SVG),
Encapsulated PostScript (EPS), Portable Network Graphics (PNG),
Portable Document Format (PDF), Portable Bitmap (PBM), Portable Arbitrary Map (PAM),
LaTeX (PGF/TikZ), X PixMap (XBM), X Bitmap (XPM) or text output. None of these
serializers require an external lib. Segno could provide more serialization
formats via a plugin architecture.
Further, it provides several high level function to create QR Codes which encode
contact data (MeCard, vCard) or WIFI configurations.


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
    $ segno  --scale=10 --color=darkblue --border=0 --output=fire.svg "Who by Fire"
    $ segno --scale=10 --background=transparent --output=miracle.png "Waiting for the Miracle"



Library
^^^^^^^

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Up Jumped the Devil')  # Let Segno choose the minimal version
    >>> qr.is_micro
    False
    >>> qr.version
    2
    >>> qr.error
    'Q'
    >>> qr.save('up-jumped-the-devil.png')  # Save as PNG
    >>> qr.save('up-jumped-the-devil-2.png', scale=10)  # Scaling factor 10
    >>> qr.save('up-jumped-the-devil-3.png', background=None)  # Transparent background
    >>> qr.save('up-jumped-the-devil.pdf', scale=10)  # Save as PDF
    >>> # SVG drawing the dark modules in "dark blue"
    >>> qr.save('up-jumped-the-devil.svg', scale=10, color='darkblue')


If the content to encode is small enough, a Micro QR Code is generated:

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('RAIN')
    >>> qr.is_micro
    True
    >>> qr.version
    'M2'


If this behaviour is not desired, the user may use the factory functions
``segno.make_qr()`` which generates always QR Codes (never Micro QR Codes) or
``segno.make_micro()`` which generates always Micro QR Codes (or raises an error
if the content is too large for a Micro QR Code).

.. code-block:: python

    >>> import segno
    >>> mqr = segno.make_micro('THE BEATLES')
    >>> mqr.version
    'M3'
    >>> qr = segno.make_qr('THE BEATLES')  # Same content but enforce a QR Code
    >>> qr.version
    1
    >>> # This won't work since the data does not fit into a Micro QR Code M1 - M4
    >>> mqr = segno.make_micro('Nick Cave and the Bad Seeds')
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
