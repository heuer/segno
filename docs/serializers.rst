QR Code and Micro QR Code serialization
=======================================

A QR Code or Micro QR Code is independent of its output, it's just a matrix.
To save a QR Code or Micro QR Code, Segno provides several output formats.

The simpliest way to generate and save a QR Code or Micro QR Code is calling

.. code-block:: python

    >>> import segno
    >>> # Save as SVG
    >>> segno.make('Polly').save('polly.svg')
    >>> # Save as PNG
    >>> segno.make('Polly').save('polly.png')


The above statement are equivalent to

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Polly')
    >>> qr.save('polly.svg')
    >>> qr.save('polly.png')


All serializers accept a ``border`` parameter which indicates the "quiet zone"
of a (Micro) QR Code. If ``border`` is ``None``, the default border (quiet zone)
size will be used. If the resulting (Micro) QR Code should have no border or
a custom border, you may specify the border

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Vampire Blues')
    >>> qr.save('vampire-blues.svg', border=0)  # No border
    >>> qr.save('vampire-blues.png', border=10)  # Bigger border


Most serializers accept a ``scale`` parameter which indicates the scaling
factor of the serialization. By default, the scale is ``1`` which means that
the dark / light modules of a (Micro) QR Code is interpreted as 1 unit in the
specific user space (i.e. 1 pixel for the PNG serializer or 1 point (1/72 of an
inch) in EPS). Some serializers (like PNG) accept only an integer value or
convert the provided scaling factor to an integer. Other, like SVG and EPS
accept float values and do not "downgrade" it to integer.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make_qr('The Beatles')
    >>> qr.save('the-beatles.png', scale=1.2)   # No scaling at all since int(1.2) is 1
    >>> qr.save('the-beatles-2.png', scale=10)  # 1 module == 10 pixels
    >>> qr.save('the-beatles.svg', scale=1.2)   # SVG accepts float values
    >>> # The SVG serializer provides the "unit" parameter to specify
    >>> # how to interpret the values
    >>> qr.save('the-beatles-2.svg', scale=10, unit='mm')  # 1 unit = 1 mm
    >>> qr.save('the-beatles-2.svg', unit='cm')  # 1 unit = 1 cm, result as above


Many serializers accept the parameters ``color`` and ``background`` to specify
the color of the dark modules and light modules (background). If accepted,
``None`` is interpreted as "transparent". Colors may be specified as HTML color
names, as hexadecimal value (``#RGB`` or ``#RRGGBB``), or (if supported, as
hexadecimal value with an alpha channel (``#RGBA`` or ``#RRGGBBAA``).

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Neil Young')
    >>> qr.save('neil-young.svg', color='darkblue', background='yellow')
    >>> qr.save('neil-young.png', color='#ccc')
    >>> qr.save('neil-young-2.png', background=None)  # Transparent background
    >>> # Dark modules = transparent, light modules = black
    >>> qr.save('neil-young-3.png', color=None, background='black')
    >>> # Dark modules with alpha transparency
    >>> qr.save('neil-young-4.png', color='#0000ffcc', background=None)
    >>> qr.save('neil-young-4.svg', color='#00fc')  # Same as above but SVG


See :py:class:`segno.QRCode` for a complete reference which parameters are
accepted by the specific serializers.
