Segno's low level API
=====================

:py:func:`segno.make`, :py:func:`segno.make_qr`, and :py:func:`segno.make_micro`
return a :py:class:`segno.QRCode` which implements almost no logic but uses the
result of :py:func:`segno.encoder.encode` glued together with the functionality
of :py:mod:`segno.writers` to provide a simple (supposed to be user-friendly)
API.

A completely different API is possible by utilizing
:py:func:`segno.encoder.encode` which returns just a tuple:
``(matrix, version, error, mask, segments)``. The module
:py:mod:`segno.writers` is independent of the :py:mod:`segno.encoder`
module and vice versa.


segno.encoder
-------------

.. automodule:: segno.encoder
    :members:


segno.writers
-------------

.. automodule:: segno.writers
    :members:
