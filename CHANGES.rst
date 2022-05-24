Changes
=======

1.5.2 -- 2022-05-25
-------------------
* Added support for `PEP 517 <https://www.python.org/dev/peps/pep-0517/>`_
* Removed PyQRCode from comparison / benchmarks since it adds no value anymore
* Added more properties for vCard
  see `PR #106 <https://github.com/heuer/segno/pull/106>`_ contributed by
  `Tobias Udtke <https://github.com/DerBiasto>`_:

  - cellphone (TEL;TYPE=CELL)
  - homephone (TEL;TYPE=HOME)
  - workphone (TEL;TYPE=WORK)

  Signatures of `segno.helpers.make_vcard <https://segno.readthedocs.io/en/latest/api.html#segno.helpers.make_vcard>`_
  and `segno.helpers.make_vcard_data <https://segno.readthedocs.io/en/latest/api.html#segno.helpers.make_vcard_data>`_
  changed, but in a backwards compatible way.
* Changed default Python test version to 3.10 (2.7 and above are still supported)


1.5.1 -- 2022-05-05-24
----------------------
* Unreleased

1.5.0 -- 2022-05-05-24
----------------------
* Unreleased

1.4.1 -- 2021-11-25
-------------------
* Fixed Python type hints
* XPM serializer accepts ``None`` (transparent) for dark modules
* Better docs


1.4.0 -- 2021-11-06
-------------------
* Added option to print QR codes in a more compact manner to the terminal.
  `PR #97 <https://github.com/heuer/segno/pull/97>`_ implemented by
  `Christian Oudard <https://github.com/christian-oudard>`_.
* Minor doc changes
* Added more test cases
* Updated benchmark results


1.3.3 -- 2021-03-23
-------------------
* Fixed `#95 <https://github.com/heuer/segno/issues/95>`_:
  ``helpers.make_wifi`` and ``helpers.make_wifi_data`` may return
  invalid data if any input contains characters which can be
  interpreted as an integer.
* Updated ``helpers.make_wifi`` and ``helpers.make_wifi_data``
  signature and doc strings to match the stub / type hints.


1.3.2 -- 2021-03-22
-------------------
* Not released due to twine issues (markup errors in README.rst)


1.3.1 -- 2020-09-01
-------------------
* Fixed: Stub files (type hints) were missing from the source distribution.


1.3.0 -- 2020-08-31
-------------------
* Fixed `#84 <https://github.com/heuer/segno/issues/84>`_:
  CLI ``--encoding`` was used for the encoding of SVG documents and not
  for the encoding of the QR code.
  Added ``--svgencoding`` to specify the encoding of SVG documents.


1.2.1 -- 2020-08-27
-------------------
* Improved API docs
* Added support for type hints for the public API (stub files)


1.2.0 -- 2020-08-18
-------------------
* Added ``QRCode.svg_inline`` method which returns a string which
  can be used to embed the SVG directly in HTML pages.
* Improved documentation <https://segno.readthedocs.org/>
* Improved code quality
* Switched from `tox <https://pypi.org/project/tox/>`_ to
  `nox <https://pypi.org/project/nox/>`_
* Utilize `flake8 <https://pypi.org/project/flake8/>`_
* Moved metadata from setup.py to setup.cfg


1.1.0 -- 2020-08-05
-------------------
* Support for `Hanzi <https://en.wikipedia.org/wiki/Chinese_characters>`_ mode,
  implemented by `Shi Yan <https://github.com/neycyanshi>`_
* Fixed `#81 <https://github.com/heuer/segno/issues/81>`_:
  Wrong character count in Kanji mode if the user provided the QR code data
  as bytes.
* Improved documentation <https://segno.readthedocs.org/>
* Improved API docs


1.0.2 -- 2020-07-30
-------------------
* Fixed error in Kanji encoding: Data was incomplete.
  Again, discovered by `Shi Yan <https://github.com/neycyanshi>`_
* Better test coverage for Kanji encoding


1.0.1 -- 2020-07-28
-------------------
* Fixed wrong information about character count in Kanji mode
  (discovered and fixed by `Shi Yan <https://github.com/neycyanshi>`_)
* Fixed `#72 <https://github.com/heuer/segno/issues/72>`_:
  Encodings for ``helpers.make_epc_qr`` may be specified by name or
  by a numeric constant.
* Added support for `Netpbm PPM <http://netpbm.sourceforge.net/doc/ppm.html>`_ images.
* Documentation improvements (also thanks to `James Addison <https://github.com/jayaddison>`_
  for pr `#73 <https://github.com/heuer/segno/pull/73>`_)
* Removed "version" parameter from ``encoder.prepare_data`` (does not belong to
  the public API anyway)


1.0.0 -- 2020-02-14
-------------------
* Removed support for ``color`` / ``background`` keywords (deprecated in 0.4.0).
  Use ``dark`` and ``light``.
* Reintroduced ``segno.DataOverflowError`` (inherited from ``ValueError``) to
  indicate that the provided data does not fit into the provided (Micro) QR Code
  parameters.
* Documentation improvements
* Although this lib made backwards incompatible changes since version 0.1.0,
  the changes should be clear since almost all changes were made
  very conservative with backwards compatibility in mind.
  Even early adopters should find a clear update path.
  This version marks a stable API acc. to `Semantic Versioning <https://semver.org/>`_.
* The initial stable release after nearly four years of development. Happy
  valentine ;)


0.4.0 -- 2020-01-21
-------------------
* Removed deprecated functions, modules etc. See `#56 <https://github.com/heuer/segno/issues/56>`_,
  `#57 <https://github.com/heuer/segno/issues/57>`_, `#59 <https://github.com/heuer/segno/issues/59>`_,
  `#61 <https://github.com/heuer/segno/issues/61>`_, `#67 <https://github.com/heuer/segno/issues/67>`_.
* Deprecated usage of keywords "color" and "background". Replacements: "dark"
  and "light". See `#60 <https://github.com/heuer/segno/issues/60>`_. The deprecated keywords will be removed in 1.0.0.
* Minor performance improvements for writing SVG (at least for Py 3.7, YMMV).
* Documentation improvements


0.3.9 -- 2020-01-19
-------------------
* Fixed `#71 <https://github.com/heuer/segno/issues/71>`_: Dark / light
  modules of the finder pattern may be interpreted wrong if set to ``None``
* Removed segno.encoder, segno.writers and segno.utils from public API (fixes
  `#69 <https://github.com/heuer/segno/issues/69>`_)
* Removed segno.colors (part of segno.writers now)
* Documentation improvements


0.3.8 -- 2020-01-15
-------------------
* Added support for multiple (more than two) colors to SVG
  (fixes `#64 <https://github.com/heuer/segno/issues/64>`_)
* Fixed several test cases
* Removed ``QRCodeError`` and all derived exceptions from public API (still
  available but not thrown and they will be removed in 0.4.0)
* Documentation improvements


0.3.7 -- 2020-01-09
-------------------
* Documentation improvements: Added several examples, fixed docs
* Fixed `#62 <https://github.com/heuer/segno/issues/62>`_:
  PNG serializer adds only those colors to the PLTE which are
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
  (fixes `#58 <https://github.com/heuer/segno/issues/58>`_).
* Fixed Read the Docs build
* Improved documentation
* Minor performance and code improvements.


0.3.4 -- 2020-01-02
-------------------
* Fixed issue `#54 <https://github.com/heuer/segno/issues/54>`_:
  After last change (see 0.3.3), white background with transparent
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
* Fixed issue `#54 <https://github.com/heuer/segno/issues/54>`_:
  PNGs with white color and transparent background were rendered
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
* Added man page for the CLI (fixes `#41 <https://github.com/heuer/segno/issues/41>`_)
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
  initial code contributed by `Serge Morel <https://github.com/Vluf>`_
  (pr `#52 <https://github.com/heuer/segno/pull/52>`_).


0.2.8 -- 2018-10-17
-------------------
* Fixed `#45 <https://github.com/heuer/segno/issues/45>`_:
  CLI does not raise exceptions but indicates errors with return code 1 and
  writes the error message to ``sys.stderr``
* Added experimental ``utils.matrix_iter_detail()`` function which returns an iterator over
  the matrix to distinguish different dark and light modules by their function (i.e. separator,
  finder pattern etc.)
* Minor performance improvements
* Removed Python 2.6 from test environment
* Added support for vCard TITLE attribute, contributed by `Stefano Borini <https://github.com/stefanoborini>`_
  (pr `#48 <https://github.com/heuer/segno/pull/48>`_)
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
* Fixed `#33 <https://github.com/heuer/segno/issues/33>`_:
  Some Micro QR Codes may be unreadable due to wrong
  format information. Further, M1 and M3 codes may be wrong due to wrong
  encoding of final data symbol character (8 bits instead of (correct) 4 bits).
  Thanks to `Nicolas Boullis <https://github.com/nboullis>`_ for the bug report,
  initial fix, tests and patience.
* Fixed `#34 <https://github.com/heuer/segno/issues/34>`_:
  Change default error level from "M" to "L" to avoid surprises that
  the content does not fit into the provided version. This change is somewhat
  backwards incompatible.
* Fixed `#35 <https://github.com/heuer/segno/issues/35>`_:
  Check of user supplied mask pattern index was wrong.
* Fixed `#36 <https://github.com/heuer/segno/issues/36>`_:
  Wrong placement of codeword in M1 and M3 symbols.
* Fixed `#37 <https://github.com/heuer/segno/issues/37>`_:
  Generation of M1 / M3 symbols fail if the data modules are
  completely filled.
* Fixed `#38 <https://github.com/heuer/segno/issues/38>`_:
  Optimized mask pattern choosing algorithm: If the user supplied
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
* Fixed `#27 <https://github.com/heuer/segno/issues/27>`_:
  Email URI is wrong if CC or BCC is used.
* Fixed `#32 <https://github.com/heuer/segno/issues/32>`_:
  Don't add version attribute if SVG >= 2.0
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
  is also mentioned in the help message (``-h``) (`#24 <https://github.com/heuer/segno/issues/24>`_)
* Support for creating email addresses or complete messages (``segno.helpers``)
* Internal optimizations and more correct minimal version finding
  (`#26 <https://github.com/heuer/segno/issues/26>`_)


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
* Fixed serious issue `#23 <https://github.com/heuer/segno/issues/23>`_:
  Segno creates invalid QR Codes if boost_error is not disabled
  (enabled by default)


0.1.8 -- 2016-09-14
-------------------
* Removed ``utils.matrix_with_border_iter``
* Fixed `#21 <https://github.com/heuer/segno/issues/21>`_
  (type error while writing to terminal under Windows)
* Added option to serialize QR Codes as LaTeX vector graphic
* Added module ``segno.helpers`` which provides additional factory functions
  to create common QR Codes like a WIFI configuration, a geo location or MeCard


0.1.7 -- 2016-09-04
-------------------
* Changed API: Added a feature to increase the error correction level
  if it fits. Disable this feature via ``boost_error=False``
  (`#16 <https://github.com/heuer/segno/issues/16>`_)
* Added ``--no-error-boost`` to the command line script to disable error
  correction level incrementation (`#17 <https://github.com/heuer/segno/issues/17>`_)
* Command line script: Internal changes and better test coverage
* Added tests for issue `#18 <https://github.com/heuer/segno/issues/18>`_
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
  into an invalid SVG document (issue `#8 <https://github.com/heuer/segno/issues/8>`_).
* SVG serializer: If ``unit`` was set to ``None``, an invalid SVG document was
  generated (issue `#14 <https://github.com/heuer/segno/issues/14>`_).
* Better command line support:

  - The command line script recognizes all SVG options (`#9 <https://github.com/heuer/segno/issues/9>`_)
  - Added ``--mode``/``-m``, renamed ``--mask``/``-m`` to ``--pattern``/``-p``
    (issue `#10 <https://github.com/heuer/segno/issues/10>`_)
  - The script used an empty string as default value for the data to encode.
    The data to encode has no default value anymore
    (issue `#11 <https://github.com/heuer/segno/issues/11>`_)
  - Added ``--no-ad`` to omit the comment ``Software`` in PNG images
    (issue `#12 <https://github.com/heuer/segno/issues/12>`_)


0.1.4 -- 2016-08-21
-------------------
* Better terminal output
* Fixed issue `#5 <https://github.com/heuer/segno/issues/5>`_:
  QRCode.terminal() uses a special output function (if it
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
* Backward incompatible changes: Deprecated "eps", "svg", "png", "pdf", and
  "txt" methods from QRCode. Use QRCode.save.
  Methods will be removed in 0.1.3
* Fixed issue `#3 <https://github.com/heuer/segno/issues/3>`_
  (M1 and M3 codes may have undefined areas)
* Fixed issue `#4 <https://github.com/heuer/segno/issues/4>`_
  (wrong 'error' default value for encoder.encode(),
  factory function segno.make() wasn't affected)


0.1.1 -- 2016-08-14
-------------------
* Initial release
