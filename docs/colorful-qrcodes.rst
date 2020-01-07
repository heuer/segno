Colorful QR Codes
=================

The PNG serializer supports more than two colors, every module type may have
its own color.

.. code-block:: python

    >>> import segno
    >>> # Force version 7 since smaller versions don't carry any version information (see below)
    >>> qr = segno.make('Yellow Submarine', version=7, error='h')
    >>> qr.save('yellow-submarine.png', scale=4, dark='darkred', data_dark='darkorange',
                data_light='yellow')

.. image:: _static/colorful/yellow-submarine.png
    :alt: Colorful 7-H QR Code encoding "Yellow Submarine"


Color names
-----------

dark
~~~~

Sets the (default) color of dark modules.

.. image:: _static/colorful/dark.png
    :alt: Picture showing the dark modules


light
~~~~~

Sets the (default) color of light modules.

.. image:: _static/colorful/light.png
    :alt: Picture showing the light modules


alignment_dark
~~~~~~~~~~~~~~

Sets the color of the dark alignment pattern modules.

.. image:: _static/colorful/alignment_dark.png
    :alt: Picture showing the dark alignment modules


alignment_light
~~~~~~~~~~~~~~~

Sets the color of the light alignment pattern modules.

.. image:: _static/colorful/alignment_light.png
    :alt: Picture showing the light alignment modules


dark_module
~~~~~~~~~~~

Sets the color of the dark module.

.. image:: _static/colorful/dark_module.png
    :alt: Picture showing the dark module


data_dark
~~~~~~~~~

Sets the color of the dark data modules.

.. image:: _static/colorful/data_dark.png
    :alt: Picture showing the dark data modules


data_light
~~~~~~~~~~

Sets the color of the light data modules.

.. image:: _static/colorful/data_light.png
    :alt: Picture showing the light modules


finder_dark
~~~~~~~~~~~

Sets the color of the dark modules of the finder pattern.

.. image:: _static/colorful/finder_dark.png
    :alt: Picture showing the dark finder modules


finder_light
~~~~~~~~~~~~

Sets the color of the light modules of the finder pattern.

.. image:: _static/colorful/finder_light.png
    :alt: Picture showing the light finder modules


format_dark
~~~~~~~~~~~

Sets the color of the dark modules of the format information.

.. image:: _static/colorful/format_dark.png
    :alt: Picture showing the dark format information modules


format_light
~~~~~~~~~~~~

Sets the color of the light modules of the format information.

.. image:: _static/colorful/format_light.png
    :alt: Picture showing the light format information modules


quiet_zone
~~~~~~~~~~

Sets the color of the quiet zone.

.. image:: _static/colorful/quiet_zone.png
    :alt: Picture showing the quiet zone


separator
~~~~~~~~~

Sets the color of the separator.

.. image:: _static/colorful/separator.png
    :alt: Picture showing the separator


timing_dark
~~~~~~~~~~~

Sets the color of the dark modules of the timing pattern.

.. image:: _static/colorful/timing_dark.png
    :alt: Picture showing the dark timing pattern modules


timing_light
~~~~~~~~~~~~

Sets the color of the light modules of the timing pattern.

.. image:: _static/colorful/timing_light.png
    :alt: Picture showing the light timing pattern modules


version_dark
~~~~~~~~~~~~

Sets the color of the dark modules of the version information.

.. image:: _static/colorful/version_dark.png
    :alt: Picture showing the dark version modules


version_light
~~~~~~~~~~~~~

Sets the color of the light modules of the version information.

.. image:: _static/colorful/version_light.png
    :alt: Picture showing the light version modules
