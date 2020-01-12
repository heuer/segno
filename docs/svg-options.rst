SVG Options
===========

The SVG serializer supports several options to optimize the output.
By default, a minimal, standalone SVG graphic is generated which includes
the XML declaration, the SVG namespace and a trailing newline.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Penny Lane', error='h')
    >>> qr.save('penny-lane.svg', scale=4)


.. image:: _static/svg/penny-lane.svg
    :alt: 2-H QR Code encoding 'Penny Lane'

XML markup:

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="132" height="132" class="segno"><path transform="scale(4)" stroke="#000" class="qrline" d="M4 4h7m3 0h1m1 0h1m1 0h1m3 0h7m-25 1h1m5 0h1m3 0h2m1 0h4m1 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m5 0h1m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m1 0h1m1 0h1m3 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m4 0h3m1 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m2 0h1m2 0h2m2 0h1m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m1 0h4m-15 1h2m2 0h5m3 0h1m1 0h3m1 0h1m-19 1h2m1 0h1m1 0h10m2 0h1m2 0h1m-23 1h2m1 0h5m1 0h1m1 0h1m1 0h1m2 0h1m5 0h1m-23 1h1m1 0h3m2 0h1m2 0h3m1 0h2m1 0h1m2 0h4m-24 1h1m1 0h1m1 0h1m1 0h2m3 0h2m1 0h1m3 0h1m1 0h5m-21 1h1m2 0h4m1 0h3m1 0h2m1 0h6m-24 1h1m1 0h1m1 0h5m1 0h3m1 0h2m6 0h1m-24 1h1m2 0h2m2 0h1m3 0h1m4 0h1m1 0h1m5 0h1m-22 1h1m2 0h2m2 0h1m2 0h11m-16 1h1m2 0h1m1 0h1m1 0h2m3 0h1m2 0h1m-24 1h7m1 0h5m2 0h2m1 0h1m1 0h1m2 0h2m-25 1h1m5 0h1m4 0h1m1 0h2m1 0h1m3 0h1m2 0h2m-25 1h1m1 0h3m1 0h1m6 0h1m2 0h5m3 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m3 0h1m4 0h1m1 0h2m2 0h1m-25 1h1m1 0h3m1 0h1m1 0h7m2 0h1m1 0h2m2 0h1m-24 1h1m5 0h1m2 0h2m2 0h1m2 0h4m1 0h2m-23 1h7m5 0h1m1 0h1m1 0h1m2 0h3m1 0h2"/></svg>


To suppress the XML declaration, use ``xmldecl=False``.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Penny Lane', error='h')
    >>> qr.save('penny-lane.svg', scale=4, xmldecl=False)


XML markup:

.. code-block:: xml

    <svg xmlns="http://www.w3.org/2000/svg" width="132" height="132" class="segno"><path transform="scale(4)" stroke="#000" class="qrline" d="M4 4h7m3 0h1m1 0h1m1 0h1m3 0h7m-25 1h1m5 0h1m3 0h2m1 0h4m1 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m5 0h1m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m1 0h1m1 0h1m3 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m4 0h3m1 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m2 0h1m2 0h2m2 0h1m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m1 0h4m-15 1h2m2 0h5m3 0h1m1 0h3m1 0h1m-19 1h2m1 0h1m1 0h10m2 0h1m2 0h1m-23 1h2m1 0h5m1 0h1m1 0h1m1 0h1m2 0h1m5 0h1m-23 1h1m1 0h3m2 0h1m2 0h3m1 0h2m1 0h1m2 0h4m-24 1h1m1 0h1m1 0h1m1 0h2m3 0h2m1 0h1m3 0h1m1 0h5m-21 1h1m2 0h4m1 0h3m1 0h2m1 0h6m-24 1h1m1 0h1m1 0h5m1 0h3m1 0h2m6 0h1m-24 1h1m2 0h2m2 0h1m3 0h1m4 0h1m1 0h1m5 0h1m-22 1h1m2 0h2m2 0h1m2 0h11m-16 1h1m2 0h1m1 0h1m1 0h2m3 0h1m2 0h1m-24 1h7m1 0h5m2 0h2m1 0h1m1 0h1m2 0h2m-25 1h1m5 0h1m4 0h1m1 0h2m1 0h1m3 0h1m2 0h2m-25 1h1m1 0h3m1 0h1m6 0h1m2 0h5m3 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m3 0h1m4 0h1m1 0h2m2 0h1m-25 1h1m1 0h3m1 0h1m1 0h7m2 0h1m1 0h2m2 0h1m-24 1h1m5 0h1m2 0h2m2 0h1m2 0h4m1 0h2m-23 1h7m5 0h1m1 0h1m1 0h1m2 0h3m1 0h2"/></svg>


If the SVG graphic should be embedded into a HTML 5 context, the namespace
declaration is superfluous, omit it via ``svgns=False``.


.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Penny Lane', error='h')
    >>> qr.save('penny-lane.svg', scale=4, xmldecl=False, svgns=False)

XML markup:

.. code-block:: xml

    <svg width="132" height="132" class="segno"><path transform="scale(4)" stroke="#000" class="qrline" d="M4 4h7m3 0h1m1 0h1m1 0h1m3 0h7m-25 1h1m5 0h1m3 0h2m1 0h4m1 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m5 0h1m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m1 0h1m1 0h1m3 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m4 0h3m1 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m2 0h1m2 0h2m2 0h1m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m1 0h4m-15 1h2m2 0h5m3 0h1m1 0h3m1 0h1m-19 1h2m1 0h1m1 0h10m2 0h1m2 0h1m-23 1h2m1 0h5m1 0h1m1 0h1m1 0h1m2 0h1m5 0h1m-23 1h1m1 0h3m2 0h1m2 0h3m1 0h2m1 0h1m2 0h4m-24 1h1m1 0h1m1 0h1m1 0h2m3 0h2m1 0h1m3 0h1m1 0h5m-21 1h1m2 0h4m1 0h3m1 0h2m1 0h6m-24 1h1m1 0h1m1 0h5m1 0h3m1 0h2m6 0h1m-24 1h1m2 0h2m2 0h1m3 0h1m4 0h1m1 0h1m5 0h1m-22 1h1m2 0h2m2 0h1m2 0h11m-16 1h1m2 0h1m1 0h1m1 0h2m3 0h1m2 0h1m-24 1h7m1 0h5m2 0h2m1 0h1m1 0h1m2 0h2m-25 1h1m5 0h1m4 0h1m1 0h2m1 0h1m3 0h1m2 0h2m-25 1h1m1 0h3m1 0h1m6 0h1m2 0h5m3 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m3 0h1m4 0h1m1 0h2m2 0h1m-25 1h1m1 0h3m1 0h1m1 0h7m2 0h1m1 0h2m2 0h1m-24 1h1m5 0h1m2 0h2m2 0h1m2 0h4m1 0h2m-23 1h7m5 0h1m1 0h1m1 0h1m2 0h3m1 0h2"/></svg>

By default, Segno adds a ``class`` attribute to the ``svg`` element, further, it
adds a ``class`` attribute to all paths. To omit the ``class`` attribute of the
``svg`` element, use ``svgclass=None``. To omit the ``class`` attribute of the
paths, use ``lineclass=None``.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Penny Lane', error='h')
    >>> qr.save('penny-lane.svg', scale=4, xmldecl=False, svgns=False, svgclass=None, lineclass=None)

.. code-block:: xml

    <svg width="132" height="132"><path transform="scale(4)" stroke="#000" d="M4 4h7m3 0h1m1 0h1m1 0h1m3 0h7m-25 1h1m5 0h1m3 0h2m1 0h4m1 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m5 0h1m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m1 0h1m1 0h1m3 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m4 0h3m1 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m2 0h1m2 0h2m2 0h1m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m1 0h4m-15 1h2m2 0h5m3 0h1m1 0h3m1 0h1m-19 1h2m1 0h1m1 0h10m2 0h1m2 0h1m-23 1h2m1 0h5m1 0h1m1 0h1m1 0h1m2 0h1m5 0h1m-23 1h1m1 0h3m2 0h1m2 0h3m1 0h2m1 0h1m2 0h4m-24 1h1m1 0h1m1 0h1m1 0h2m3 0h2m1 0h1m3 0h1m1 0h5m-21 1h1m2 0h4m1 0h3m1 0h2m1 0h6m-24 1h1m1 0h1m1 0h5m1 0h3m1 0h2m6 0h1m-24 1h1m2 0h2m2 0h1m3 0h1m4 0h1m1 0h1m5 0h1m-22 1h1m2 0h2m2 0h1m2 0h11m-16 1h1m2 0h1m1 0h1m1 0h2m3 0h1m2 0h1m-24 1h7m1 0h5m2 0h2m1 0h1m1 0h1m2 0h2m-25 1h1m5 0h1m4 0h1m1 0h2m1 0h1m3 0h1m2 0h2m-25 1h1m1 0h3m1 0h1m6 0h1m2 0h5m3 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m3 0h1m4 0h1m1 0h2m2 0h1m-25 1h1m1 0h3m1 0h1m1 0h7m2 0h1m1 0h2m2 0h1m-24 1h1m5 0h1m2 0h2m2 0h1m2 0h4m1 0h2m-23 1h7m5 0h1m1 0h1m1 0h1m2 0h3m1 0h2"/></svg>

To replace the ``width`` and ``height`` parameters, use ``omitsize=True``.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Penny Lane', error='h')
    >>> qr.save('penny-lane.svg', scale=4, xmldecl=False, svgns=False, svgclass=None, lineclass=None, omitsize=True)


XML markup.


.. code-block:: xml

    <svg viewBox="0 0 132 132"><path transform="scale(4)" stroke="#000" d="M4 4h7m3 0h1m1 0h1m1 0h1m3 0h7m-25 1h1m5 0h1m3 0h2m1 0h4m1 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m5 0h1m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m1 0h1m1 0h1m3 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m4 0h3m1 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m2 0h1m2 0h2m2 0h1m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m1 0h4m-15 1h2m2 0h5m3 0h1m1 0h3m1 0h1m-19 1h2m1 0h1m1 0h10m2 0h1m2 0h1m-23 1h2m1 0h5m1 0h1m1 0h1m1 0h1m2 0h1m5 0h1m-23 1h1m1 0h3m2 0h1m2 0h3m1 0h2m1 0h1m2 0h4m-24 1h1m1 0h1m1 0h1m1 0h2m3 0h2m1 0h1m3 0h1m1 0h5m-21 1h1m2 0h4m1 0h3m1 0h2m1 0h6m-24 1h1m1 0h1m1 0h5m1 0h3m1 0h2m6 0h1m-24 1h1m2 0h2m2 0h1m3 0h1m4 0h1m1 0h1m5 0h1m-22 1h1m2 0h2m2 0h1m2 0h11m-16 1h1m2 0h1m1 0h1m1 0h2m3 0h1m2 0h1m-24 1h7m1 0h5m2 0h2m1 0h1m1 0h1m2 0h2m-25 1h1m5 0h1m4 0h1m1 0h2m1 0h1m3 0h1m2 0h2m-25 1h1m1 0h3m1 0h1m6 0h1m2 0h5m3 0h1m-25 1h1m1 0h3m1 0h1m1 0h2m3 0h1m4 0h1m1 0h2m2 0h1m-25 1h1m1 0h3m1 0h1m1 0h7m2 0h1m1 0h2m2 0h1m-24 1h1m5 0h1m2 0h2m2 0h1m2 0h4m1 0h2m-23 1h7m5 0h1m1 0h1m1 0h1m2 0h3m1 0h2"/></svg>



Too squeeze the file size futher, omit the trailing newline character via ``nl=False``.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Penny Lane', error='h')
    >>> qr.save('penny-lane.svg', scale=4, xmldecl=False, svgns=False, svgclass=None, lineclass=None, omitsize=True, nl=False)


The result is allmost he same, but you've saved a few (abt. 107) bytes

.. raw:: html
    :file: _static/svg/penny-lane-optimized.svg


Options
-------


xmldecl
~~~~~~~
Boolean to enable (default) or omit the XML declaration


svgns
~~~~~
Boolean to enable (default) or omit the SVG namespace declaration.


svgid
~~~~~
String (default: ``None``).
CSS identifier of the ``svg`` element.


svgclass
~~~~~~~~
String (default: "segno").
CSS class of the ``svg`` element. Use ``None`` to omit it.


lineclass
~~~~~~~~~
String (default: "qrline").
CSS class of all paths. Use ``None`` to omit it.
