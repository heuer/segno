Special QR Code factory functions
=================================

The :py:mod:`segno.helpers` module provides factory functions to create common QR Codes
for encoding WIFI configurations, :doc:`vCards and MeCards <contact-information>`,
:doc:`EPC QR Codes <epc-qrcodes>` or geographic locations.

The created QR Codes use at minimum the error correction level "L". If a better
error correction level is possible without changing the QR Code version, the
better error correction level will be used.


Create a QR Code for a WIFI configuration
-----------------------------------------

.. code-block:: python

    >>> from segno import helpers
    >>> # Create a WIFI config with min. error level "L" or better
    >>> qr = helpers.make_wifi(ssid='My network', password='secret', security='WPA')
    >>> qr.designator
    '3-M'


.. image:: _static/wifi/wifi_default.png
    :alt: 3-M QR Code encoding a WIFI configuration


If you want more control over the creation of the QR Code (i.e. using a specific
version or error correction level, use the :py:func:`segno.helpers.make_wifi_data`
factory function, which returns a string which encodes the WIFI configuration.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> config = helpers.make_wifi_data(ssid='My network', password='secret', security='WPA')
    >>> config
    'WIFI:T:WPA;S:My network;P:secret;;'
    >>> # Create a QR Code with error correction level "L"
    >>> qr = segno.make(config, error='h')
    >>> qr.designator
    '4-H'


.. image:: _static/wifi/wifi_data.png
    :alt: 4-H QR Code encoding a WIFI configuration


Create a QR Code encoding geographic information
------------------------------------------------

.. code-block:: python

    >>> from segno import helpers
    >>> latitude, longitude = 38.8976763,-77.0365297
    >>> qr = helpers.make_geo(latitude, longitude)
    >>> qr.designator
    '2-M'

A factory function for encoding the geographic information as string is also
available.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> latitude, longitude = 38.8976763, -77.0365297
    >>> geo_uri = helpers.make_geo_data(latitude, longitude)
    >>> geo_uri
    'geo:38.8976763,-77.0365297'
    >>> # Use version 4 instead of the minimum version
    >>> qr = segno.make(geo_uri, version=4)
    >>> qr.designator
    '4-H'


