Creating a QR Code encoding contact information
===============================================

MeCard
------

The function :py:func:`segno.helpers.make_mecard` returns a QR code which encodes
contact information as MeCard.

.. code-block:: python

    >>> from segno import helpers
    >>> qr = helpers.make_mecard(name='Doe,John', email='me@example.org', phone='+1234567')
    >>> qr.designator
    '3-L'
    >>> # Some params accept multiple values, like email, phone, url
    >>> qr = helpers.make_mecard(name='Doe,John', email=('me@example.org', 'another@example.org'), url=['http://www.example.org', 'https://example.org/~joe'])
    >>> qr.save('my-mecard.svg', scale=4)

.. image:: _static/contact/my-mecard.svg
    :alt: QR Code encoding a MeCard

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
-----

The function :py:func:`segno.helpers.make_vcard` returns a QR code which encodes
contact information as vCard version 3.0.

.. code-block:: python

    >>> from segno import helpers
    >>> qr = helpers.make_vcard(name='Doe;John', displayname='John Doe', email='me@example.org', phone='+1234567')
    >>> qr.designator
    '5-L'
    >>> # Some params accept multiple values, like email, phone, url
    >>> qr = helpers.make_vcard(name='Doe;John', displayname='John Doe', email=('me@example.org', 'another@example.org'), url=['http://www.example.org', 'https://example.org/~joe'])
    >>> qr.save('my-vcard.svg', scale=4)

.. image:: _static/contact/my-vcard.svg
    :alt: QR Code encoding a vCard

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
