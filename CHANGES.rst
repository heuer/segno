Changes
=======

0.3.8 -- 2020-01-15
-------------------
* Added support for multiple (more than two) colors to SVG (fixes #64)
* Fixed several test cases
* Removed ``QRCodeError`` and all derived exceptions from public API (still
  available but not thrown and they will be removed in 0.4.0)
* Documentation improvements


0.3.7 -- 2020-01-09
-------------------
* Documentation improvements: Added several examples, fixed docs
* Fixed #62: PNG serializer adds only those colors to the PLTE which are
  actually needed for the given (Micro) QR Code.
* Minor performance improvements


0.3.6 -- 2020-01-06
-------------------
* Backwards incompatibility change: QRCode.show() uses "dark" instead of
  "color" and "light" instead of "background" to define the color of
  the dark / light modules
* Backwards incompatibility change: All ``segno.writers`` use "dark" instead of
  "color" and "light" instead of "background". This does not affect normal users,
  but only users of the low level API.
* Changed the keyword for setting the color of the dark modules from
  "color" to "dark" and for setting the light modules from "background"
  to "light"
  The former keywords are still supported. Their usage will issue a
  DeprecationWarning in the future.
* Added ``--dark`` and ``--light`` to the command line interface, see point
  above. ```--color``` and ``--background`` are still supported.
* Fixed typos, improved documentation
* Deprecated ``segno.moduletypes`` (will be removed in release 0.4.0),
  moved all constants to ``segno.consts``
* Deprecated usage of parameter "colormap" (introduced in 0.3.4). It still
  works but a deprecation warning is issued.
  Instead of::

      colormap = {mt.TYPE_FINDER_PATTERN_DARK: 'darkred',
                  mt.TYPE_ALIGNMENT_PATTERN_DARK: 'darkred',
                  mt.TYPE_TIMING_DARK: 'darkred',
                  mt.TYPE_DARKMODULE: 'darkred',
                  mt.TYPE_DATA_DARK: 'darkorange',
                  mt.TYPE_DATA_LIGHT: 'yellow',
                  mt.TYPE_FORMAT_DARK: 'darkred'}

      qr.save('qrcode.png', scale=5, colormap=colormap)

  use::

      qr.save('qrcode.png', scale=5, dark='darkred', data_dark='darkorange',
              data_light='yellow')

  See `Colorful QR Codes <https://segno.readthedocs.io/en/stable/colorful-qrcodes.html>`_
  for a description of available module names.


0.3.5 -- 2020-01-03
-------------------
* Added support for colorful (more than two colors) QR Codes to the CLI script
  (fixes #58).
* Fixed Read the Docs build
* Improved documentation
* Minor performance and code improvements.


0.3.4 -- 2020-01-02
-------------------
* Fixed issue #54: After last change (see 0.3.3), white background with transparent
  QR Code did not work. Enhanced test suite to cover all possible inputs
  for PNG grayscale mode
* Removed interpretation of ``addad`` from PNG serializer.
  Contradicts the claim to create small images by default.
  It still belongs to the function signature but will be removed in release 0.4.0
* The option ``--no-ad`` (CLI) is still available but ignored and will be removed
  in release 0.4.0. Removed the option from man page.
* Added option to PNG serializer to provide more than two colors. Each module
  type may have its own color.
* Added support for EPC QR Codes.
* Fixed bug in ``helpers.make_vcard_data`` function (the "source" URL was not
  used, but the usual URL was added to the SOURCE field)
* Better test coverage for the ``segno.helpers`` module


0.3.3 -- 2019-12-29
-------------------
* Fixed issue #54: PNGs with white color and transparent background were rendered
  as transparent PNG with a *black* QR Code.
* Removed test environments CPython 3.4 and 3.6 from tox
* Improved documentation
* Refactored source code
* Added test cases
* Fixed bugs in ``helpers.make_vcard_data`` function
  (superfluous semicolon in birthday line, check geo coordinates)
* Renamed ``utils.matrix_iter_detail`` into ``utils.matrix_iter_verbose``.
  Kept ``matrix_iter_detail`` for backwards compatibility (deprecated, will be
  removed in release 0.4.0)
* Moved module constants from ``segno.utils`` into ``segno.moduletypes``,
  Constants from ``segno.utils`` will be removed in release 0.4.0.
* Added option ``verbose`` (default: ``False``) to ``segno.QRCode.matrix_iter()``
  which returns an iterator which provides information about the module type
  (i.e. quiet zone, dark data module, light data module).


0.3.2 -- 2019-07-15
-------------------
* Performance improvements
* Added man page for the CLI (fixes #41)
* Added more documentation and examples
* Fixed missing charts of <https://segno.readthedocs.io/en/stable/comparison-qrcode-libs.html>
* Added PyQRCodeNG <https://pypi.org/project/PyQRCodeNG/> to comparison table
* Updated CSS for a better layout of tables with a lot of content
* Removed deprecated functions ``encoder.score_n1``, ``encoder.score_n2``,
  ``encoder.score_n3``, and ``encoder.score_n4`` (they didn't belong to the
  public API anyway)
* Fixed Read the Docs build


0.3.1 -- 2019-07-15
-------------------
* See 0.3.2


0.3.0 -- 2019-06-25
-------------------
* Performance improvements (evaluation of mask scores)
* Faster PNG output
* Faster ``utils.matrix_iter`` (which improves several writers, i.e. PNG)
* Deprecation of ``encoder.score_n1``, ``encoder.score_n2``, ``encoder.score_n3``,
  and ``encoder.score_n4``.
  Use ``encoder.mask_scores`` or ``encoder.evaluate_mask``.


0.2.9 -- 2019-04-24
-------------------
* Fixed typos
* PDF serializer: Added support for stroke and background color,
  initial code contributed by Serge Morel (pr #52).


0.2.8 -- 2018-10-17
-------------------
* Fixed #45: CLI does not raise exceptions but indicates errors with return code 1 and
  writes the error message to ``sys.stderr``
* Added experimental ``utils.matrix_iter_detail()`` function which returns an iterator over
  the matrix to distinguish different dark and light modules by their function (i.e. separator,
  finder pattern etc.)
* Minor performance improvements
* Removed Python 2.6 from test environment
* Added support for vCard TITLE attribute, contributed by Stefano Borini
* Added support for vCard PHOTO URI attribute, suggested by Arthur Reinhart


0.2.7 -- 2018-02-18
-------------------
* Fixed dist package


0.2.6 -- 2018-02-18
-------------------
* Updated and fixed docs
* Added PyPy 3 to test environment


0.2.5 -- 2017-02-14
-------------------
* Added experimental support for Structured Append (divide content into max.
  16 QR Code symbols)
* Internal refactoring (i.e. segno/scripts/cmd.py -> segno/cli.py)
* Added ``-s`` shortcut to Segno's command line interface to provide the scaling factor
* Added ``-b`` shortcut to Segno's command line interface to provide the border / quiet zone
* CLI accepts unquoted, whitespace separated content:
  ``segno "Comfortably Numb"`` can be written as ``segno Comfortably Numb``


0.2.4 -- 2017-01-31
-------------------
* Fixed #33: Some Micro QR Codes may be unreadable due to wrong
  format information. Further, M1 and M3 codes may be wrong due to wrong
  encoding of final data symbol character (8 bits instead of (correct) 4 bits).
  Thanks to Nicolas Boullis for the bug report, initial fix, tests and patience.
* Fixed #34: Change default error level from "M" to "L" to avoid surprises that
  the content does not fit into the provided version. This change is somewhat
  backwards incompatible.
* Fixed #35: Check of user supplied mask pattern index was wrong.
* Fixed #36: Wrong placement of codeword in M1 and M3 symbols.
* Fixed #37: Generation of M1 / M3 symbols fail if the data modules are
  completely filled.
* Fixed #38: Optimized mask pattern choosing algorithm: If the user supplied
  a preferred mask, the mask evaluation step is skipped and the preferred mask
  is chosen
* Added more internal checks to ensure correct (Micro) QR Codes; provided
  helpful exceptions
* Removed ``writers.get_writable`` (replaced by ``writers.writable``)
* Added support for serializing QR Codes as XBM (X BitMap) (supports
  black / white images)
* Added support for serializing QR Codes as XPM (X PixMap) (supports colors and
  transparency)
* Added support for encoding contact information as vCard version 3.0
  (``segno.helpers``)
* Added -V shortcut to Segno's command line script to show version information
* Better test coverage for command line script
* Better test coverage for M1 and M3 symbols


0.2.3 -- 2016-10-17
-------------------
* Fixed #27: Email URI is wrong if CC or BCC is used.
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
* Support for creating email addresses or complete messages (``segno.helpers``)
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
