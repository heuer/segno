Special QR Code factory functions
=================================

The ``helpers`` module provides factory functions to create common QR Codes
for encoding WIFI configurations, MeCards or geographic locations.

The created QR Codes use at minimum the error correction level "M". If a better
error correction level is possible without changing the QR Code version, the
better error correction level will be used.

Create a QR Code for a WIFI configuration
-----------------------------------------

.. code-block:: python

    >>> from segno import helpers
    >>> # Create a WIFI config with min. error level "M" or better
    >>> qr = helpers.make_wifi(ssid='My network', password='secret', security='WPA')
    >>> qr.designator
    '3-Q'


If you want more control over the creation of the QR Code (i.e. using a specific
version or error correction level, use the "make_wifi_data" factory function,
which returns a string which encodes the WIFI configuration.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> config = helpers.make_wifi_data(ssid='My network', password='secret', security='WPA')
    >>> config
    'WIFI:T:WPA;S:My network;P:secret;;'
    >>> # Create a QR Code with error correction level "L"
    >>> qr = segno.make(config, error='l', boost_error=False)
    >>> qr.designator
    '3-L'


Create a QR Code encoding geographic information
------------------------------------------------

.. code-block:: python

    >>> from segno import helpers
    >>> latitude, longitude = 38.8976763,-77.0365297
    >>> qr = helpers.make_geo(latitude, longitude)
    >>> qr.designator
    '2-Q'

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


Creating a QR Code encoding contact information
-----------------------------------------------

MeCard
^^^^^^

The function ``make_mecard`` returns a QR Code which encodes contact information
as MeCard.

.. code-block:: python

    >>> from segno import helpers
    >>> qr = helpers.make_mecard(name='Doe,John', email='me@example.org', phone='+1234567')
    >>> qr.designator
    '4-Q'
    >>> # Some params accept multiple values, like email, phone, url
    >>> qr = helpers.make_mecard(name='Doe,John', email=('me@example.org', 'another@example.org'), url=['http://www.example.org', 'https://example.org/~joe'])
    >>> qr.save('my-mecard.svg')

A factory function which returns the MeCard as string is available as well.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> mecard = helpers.make_mecard_data(name='Doe,John', email='me@example.org', phone='+1234567')
    >>> mecard
    'MECARD:N:Doe,John;TEL:+1234567;EMAIL:me@example.org;;'
    >>> qr = segno.make(mecard, error='H')
    >>> qr.designator
    '6-H'


vCard
^^^^^

The function ``make_vcard`` returns a QR Code which encodes contact information
as vCard version 3.0.

.. code-block:: python

    >>> from segno import helpers
    >>> qr = helpers.make_vcard(name='Doe;John', displayname='John Doe', email='me@example.org', phone='+1234567')
    >>> qr.designator
    '6-M'
    >>> # Some params accept multiple values, like email, phone, url
    >>> qr = helpers.make_vcard(name='Doe;John', displayname='John Doe', email=('me@example.org', 'another@example.org'), url=['http://www.example.org', 'https://example.org/~joe'])
    >>> qr.save('my-vcard.svg')

A factory function which returns the vCard as string is available as well.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> vcard = helpers.make_vcard_data(name='Doe;John', displayname='John Doe', email='me@example.org', phone='+1234567')
    >>> vcard
    'BEGIN:VCARD\r\nVERSION:3.0\r\nN:Doe;John\r\nFN:John Doe\r\nEMAIL:me@example.org\r\nTEL:+1234567\r\nEND:VCARD\r\n'
    >>> qr = segno.make(vcard, error='H')
    >>> qr.designator
    '9-H'