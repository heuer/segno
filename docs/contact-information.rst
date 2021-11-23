Creating a QR Code encoding contact information
===============================================

MeCard
------

The function :py:func:`segno.helpers.make_mecard` returns a QR code which encodes
contact information as MeCard.

.. code-block:: python

    >>> from segno import helpers
    >>> qrcode = helpers.make_mecard(name='Doe,John', email='me@example.org', phone='+1234567')
    >>> qrcode.designator
    '3-L'
    >>> # Some params accept multiple values, like email, phone, url
    >>> qrcode = helpers.make_mecard(name='Doe,John',
    ...                              email=('me@example.org', 'another@example.org'),
    ...                              url=['http://www.example.org', 'https://example.org/~joe'])
    >>> qrcode.save('my-mecard.svg', scale=4)

.. image:: _static/contact/my-mecard.svg
    :alt: qrcode Code encoding a MeCard

A factory function which returns the MeCard as string is available as well.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> mecard = helpers.make_mecard_data(name='Doe,John', email='me@example.org', phone='+1234567')
    >>> mecard
    'MECARD:N:Doe,John;TEL:+1234567;EMAIL:me@example.org;;'
    >>> qrcode = segno.make(mecard, error='H')
    >>> qrcode.designator
    '6-H'


vCard
-----

The function :py:func:`segno.helpers.make_vcard` returns a QR code which encodes
contact information as vCard version 3.0.

.. code-block:: python

    >>> from segno import helpers
    >>> qrcode = helpers.make_vcard(name='Doe;John', displayname='John Doe',
    ...                             email='me@example.org', phone='+1234567')
    >>> qrcode.designator
    '5-L'
    >>> # Some params accept multiple values, like email, phone, url
    >>> qrcode = helpers.make_vcard(name='Doe;John', displayname='John Doe',
    ...                             email=('me@example.org', 'another@example.org'),
    ...                             url=['http://www.example.org', 'https://example.org/~joe'])
    >>> qrcode.save('my-vcard.svg', scale=4)

.. image:: _static/contact/my-vcard.svg
    :alt: QR Code encoding a vCard

A factory function which returns the vCard as string is available as well.

.. code-block:: python

    >>> import segno
    >>> from segno import helpers
    >>> vcard = helpers.make_vcard_data(name='Doe;John', displayname='John Doe',
    ...                                 email='me@example.org', phone='+1234567')
    >>> vcard
    'BEGIN:VCARD\r\nVERSION:3.0\r\nN:Doe;John\r\nFN:John Doe\r\nEMAIL:me@example.org\r\nTEL:+1234567\r\nEND:VCARD\r\n'
    >>> qrcode = segno.make(vcard, error='H')
    >>> qrcode.designator
    '9-H'
