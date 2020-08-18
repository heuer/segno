Artistic QR Codes
=================

Segno focuses on creating (Micro) QR codes and offers many
:ref:`output formats <serializers>` without additional dependencies on other
libraries.

Advanced graphic operations require the `qrcode-artistic <https://pypi.org/project/qrcode-artistic/>`_
plug-in, which in turn depends on the `Pillow <https://pypi.org/project/Pillow/>`_ library.

The plugin can be used to create animated QR codes or static QR codes with a
background image.

To install the plugin, use::

    pip install qrcode-artistic

After that, every QR code created with :py:func:`segno.make` has two additional
methods "to_pil" and "to_artistic".

The former returns a Pillow `Image <https://pillow.readthedocs.io/en/stable/reference/Image.html>`_
instance, which can be used for further manipulations (e.g. rotating the QR code).

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Yellow Submarine', error='h')
    >>> img = qr.to_pil(scale=3).rotate(45, expand=True)
    >>> img.save('yellow-submarine-rotated.png')

.. image:: _static/artistic/yellow-submarine-rotated.png
    :alt: Colorful 3-H QR code encoding "Yellow Submarine" rotated by 45°

The "to_pil" method provides all options of :doc:`colorful-qrcodes`.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Yellow Submarine', error='h')
    >>> img = qr.to_pil(scale=4, dark='darkred', data_dark='darkorange',
                        data_light='yellow')
    >>> img.save('yellow-submarine.png')

.. image:: _static/artistic/yellow-submarine.png
    :alt: Colorful 3-H QR code encoding "Yellow Submarine"


The "to_artistic" method can create animated or static QR codes.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('The Beatles -- Albums', error='h')
    >>> qr.to_artistic(background='src/albums.gif'), target='albums.gif' scale=8)

.. image:: _static/artistic/albums.gif
    :alt: 3-H QR code encoding "The Beatles -- Albums" (animated)


If the Pillow installation supports animated WebP images the plugin can
save animated WebP images as well.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('The Beatles -- Abbey Road', error='h')
    >>> qr.to_artistic(background='src/abbey-road-walking.gif', target='abbey-road.webp' scale=4)

.. image:: _static/artistic/abbey-road.webp
    :alt: 4-H QR code encoding "The Beatles -- Abbey Road" (animated)


The plugin also supports static backgrounds

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('The Beatles -- Let It Be', error='h')
    >>> qr.to_artistic(background='src/letitbe.jpg', target='letitbe.jpg' scale=5)

.. image:: _static/artistic/letitbe.jpg
    :alt: 3-H QR code encoding "The Beatles -- Let It Be" with a background image

