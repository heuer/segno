Changes
=======

0.2.3 -- 2016-10-17
-------------------
* Fixed #27: E-mail URI is wrong if CC or BCC is used.
* Fixed #32: Don't add version attribute if SVG >= 2.0
* Deprecated ``writers.get_writable``; use ``writers.writable``
  ``writers.writable`` closes file-like objects automatically (if necessary);
  replace ``writable, must_close = writers.get_writable(filename_or_buffer, mode)``
  with ``with writers.writable(filename_or_buffer, mode) as f``
* Added option to PNG serializer to specify an optional DPI value
  (thanks to Markus Ueberall for support)
* Added PAM (Portable Arbitrary Map) as serialization format (supports colors
  and transparency)


0.2.2 -- 2016-09-21
-------------------
* Command line script reports Segno's version (``--ver``) and the version
  is also mentioned in the help message (``-h``) (#24)
* Support for creating E-mail addresses or complete messages (``segno.helpers``)
* Internal optimizations and more correct minimal version finding (#26)



0.2.1 -- 2016-09-15
-------------------
* Fixed Python packaging (source distribution did not work), again


0.2.0 -- 2016-09-15
-------------------
* Fixed Python packaging


0.1.9 -- 2016-09-15
-------------------
* Added "color" parameter to the LaTeX serializer to define the color of the
  dark modules.
* Fixed serious issue #23: Segno creates invalid QR Codes if boost_error
  is not disabled (enabled by default)


0.1.8 -- 2016-09-14
-------------------
* Removed ``utils.matrix_with_border_iter``
* Fixed #21 (type error while writing to terminal under Windows)
* Added option to serialize QR Codes as LaTeX vector graphic
* Added module ``segno.helpers`` which provides additional factory funcitons
  to create common QR Codes like a WIFI configuration, a geo location or MeCard


0.1.7 -- 2016-09-04
-------------------
* Changed API: Added a feature to increase the error correction level
  if it fits. Disable this feature via ``boost_error=False`` (#16)
* Added ``--no-error-boost`` to the command line script to disable error
  correction level incrementation (#17)
* Command line script: Internal changes and better test coverage
* Added tests for issue #18
* Added PBM (P1 and P4) serialization.
* Deprecated ``utils.matrix_with_border_iter``, use ``utils.matrix_iter``
* ``utils.matrix_with_border_iter`` will be removed in the next release
* API change: ``QRCode.matrix_iter(border)`` -> ``QRCode.matrix_iter(scale=1, border=None)``


0.1.6 -- 2016-08-25
-------------------
* Fixed setup


0.1.5 -- 2016-08-24
-------------------
* Added QRCode.matrix_iter(border) which returns an iterator over the matrix and
  includes the border (as light modules).
* Invalid (empty) SVG identifiers / class names are ignored and do not result
  into an invalid SVG document (issue #8).
* SVG serializer: If ``unit`` was set to ``None``, an invalid SVG document was
  generated (issue #14).
* Better command line support:

  - The command line script recognizes all SVG options (#9)
  - Added ``--mode``/``-m``, renamed ``--mask``/``-m`` to ``--pattern``/``-p``
    (issue #10)
  - The script used an empty string as default value for the data to encode.
    The data to encode has no default value anymore (issue #11)
  - Added ``--no-ad`` to omit the comment ``Software`` in PNG images
    (issue #12)


0.1.4 -- 2016-08-21
-------------------
* Better terminal output
* Fixed issue #5: QRCode.terminal() uses a special output function (if it
  detects Windows) to support MS Windows which may not support ANSI escape codes.


0.1.3 -- 2016-08-20
-------------------
* Added command line script "segno"
* Registered new file extension "ans" which serializes the QR Code as
  ANSI escape code (same output as QRCode.terminal())
* Removed deprecated methods "eps", "svg", "png", "pdf", and "txt" from
  segno.QRCode
* Switched from nose tests to py.test


0.1.2 -- 2016-08-17
-------------------
* Updated docs
* Backwards incompatible change: Deprecated "eps", "svg", "png", "pdf", and
  "txt" methods from QRCode. Use QRCode.save.
  Methods will be removed in 0.1.3
* Fixed issue #3 (M1 and M3 codes may have undefined areas)
* Fixed issue #4 (wrong 'error' default value for encoder.encode(),
  factory function segno.make() wasn't affected)


0.1.1 -- 2016-08-14
-------------------
* Initial release
