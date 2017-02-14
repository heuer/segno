Structured Append
=================

The Structured Append mode can be used to split a message accross several
QR Codes (it's not available for Micro QR Codes).

Segno provides a special factory function to create a sequence of (up to 16)
QR Codes.


Structured Append by QR Code version
------------------------------------

To create a sequence of QR Codes, the QR Code version must be specified. The
number of symbols is automatically determined by the QR Code version.

.. code-block:: python

    >>> import segno
    >>> seq = segno.make_sequence('I read the news today oh boy', version=1)
    >>> len(seq)
    2
    >>> # Creates "a-day-in-the-life-02-01.svg" and "a-day-in-the-life-02-02.svg"
    >>> seq.save('a-day-in-the-life.svg', scale=10)


If the provided content fits into one QR Code, the sequence behaves like a
:py:class:`segno.QRCode` instance.

.. code-block:: python

    >>> import segno
    >>> seq = segno.make_sequence('I read', version=1)
    >>> len(seq)
    1
    >>> seq.designator
    '1-H'
    >>> # Creates "a-day-in-the-life.svg"
    >>> seq.save('a-day-in-the-life.svg', scale=10)



Structured Append by number of symbols
--------------------------------------

The number of desired QR Code symbols may be specified directly. The utilized
QR Code version is automatically determined by the number of symbols.

.. code-block:: python

    >>> import segno
    >>> seq = segno.make_sequence('Day after day, alone on the hill', symbol_count=4)
    >>> [qr.designator for qr in seq]
    ['1-Q', '1-Q', '1-Q', '1-Q']
    >>> seq = segno.make_sequence('Day after day, alone on the hill', symbol_count=2)
    >>> [qr.designator for qr in seq]
    ['2-Q', '2-Q']
