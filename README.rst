Segno -- Python QR Code and Micro QR Code encoder
=================================================

Segno is a QR Code and Micro QR Code encoder which has no further dependencies.

This package implements main parts of ISO/IEC 18004:2006(E) / ISO/IEC 18004:2015(E)
and produces Micro QR Codes and QR Codes with nearly no effort.

Segno provides several serialization formats like SVG, EPS, PNG, PDF, PBM,
LaTeX (PGF/TikZ) or text output. None of these serializers require an external
lib. Segno could provide more serialization formats via a plugin architecture.
Further, it provides several high level function to create QR Codes which encode
contact data (MeCard) or WIFI configurations.

It requires Python 2.6, 2.7 or Python 3 and works with PyPy.


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

    $ segno "Famous Blue Raincoat" -o=raincoat.svg
    $ segno "Who by Fire" --scale=10 --color=darkblue --border=0 --output=fire.svg
    $ segno "Waiting for the Miracle" --scale=10 --background=transparent --output=miracle.png



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
    'M'
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


Other QR Code generators
------------------------
* <https://pypi.python.org/pypi/PyQRCode/>
* <https://pypi.python.org/pypi/qrcode/>
* <https://pypi.python.org/pypi/qrcodegen/>

.. _Segno's documentation: http://segno.readthedocs.io/en/latest/
