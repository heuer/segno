Structured Append
=================

The Structured Append mode can be used to split a message across several
QR Codes (it's not available for Micro QR Codes).

Example: The 2-L QR Code encodes the same information ("I read the news today oh boy")
as the following 1-L QR Codes which are using Structured Append:

.. image:: _static/structured_append_2_l.svg
    :alt: 2-L QR Code encoding 'I read the news today oh boy'

With Structured Append (version 1):

.. image:: _static/structured_append_1_l-02-01.svg
    :alt: 1-L QR Code encoding 'I read the news today oh boy' part 1

.. image:: _static/structured_append_1_l-02-02.svg
    :alt: 1-L QR Code encoding 'I read the news today oh boy' part 2


Segno provides a special factory function, :py:func:`segno.make_sequence`, to
create a sequence of (up to 16) QR Codes. The function returns instances of
:py:class:`segno.QRCodeSequence`.


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
    >>> seq = segno.make_sequence('Day after day, alone on the hill', symbol_count=6)
    >>> [qr.designator for qr in seq]
    ['1-Q', '1-Q', '1-H', '1-H', '1-H', '1-H']


Example: The 6-L QR Code encodes the same information (first verse of the song "Yesterday")
as the four 2-L QR Codes.

.. image:: _static/structured_append_example_2_6-L.svg
    :alt: 6-L QR Code encoding 'Yesterday...'

The following 2-L QR Codes were created by specifying that 4 codes should be generated
(``symbol_count=4``). The result would be the same if the user specifies that a sequence
of QR Codes with version 2 should be created.

.. image:: _static/structured_append_example_2_2-L-04-01.svg
    :alt: 2-L QR Code encoding first verse of 'Yesterday' part 1

.. image:: _static/structured_append_example_2_2-L-04-02.svg
    :alt: 2-L QR Code encoding first verse of 'Yesterday' part 2

.. image:: _static/structured_append_example_2_2-L-04-03.svg
    :alt: 2-L QR Code encoding first verse of 'Yesterday' part 3

.. image:: _static/structured_append_example_2_2-L-04-04.svg
    :alt: 2-L QR Code encoding first verse of 'Yesterday' part 4
