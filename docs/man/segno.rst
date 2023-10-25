segno
=====

Synopsis
--------

**segno** [*options*] content


Description
-----------

:program:`segno` creates QR Codes and Micro QR Codes.

It can be used to print the codes to a terminal or to serialize them
in several output formats (like SVG and PNG).


Command Line Options
--------------------

.. program:: segno


.. option:: --ver, -V

    Shows Segno's version and exit

.. option:: -h, --help

    Show a help message which lists all commands and exit


QR Code Options
~~~~~~~~~~~~~~~

.. option:: --version VERSION, -v VERSION

    QR Code version: 1 \.\. 40 or Micro Code Version "M1", "M2", "M3", "M4"

.. option:: --error {L,M,Q,H,-}, -e {L,M,Q,H,-}

    Error correction level: "L": 7% (default), "M": 15%, "Q": 25%, "H": 30%,
    "-": no error correction (used for M1 symbols)

.. option:: --mode {numeric,alphanumeric,byte,kanji,hanzi}, -m {numeric,alphanumeric,byte,kanji,hanzi}

    Mode. If unspecified (default), an optimal mode is chosen for the given
    input.

.. option:: --pattern PATTERN, -p PATTERN

    Mask pattern to use. If unspecified (default), an optimal mask pattern is used.
    Valid values for QR Codes: 0 \.\. 7
    Valid values for Micro QR Codes: 0 \.\. 3

.. option:: --encoding ENCODING

    Specifies the encoding of the provided content.
    If not specified (default) either ISO 8859-1 is used or if it does
    not fit, UTF-8 or Shift_JIS (for Kanji content) is used.

.. option:: --micro

    Allow the creation of Micro QR Codes

.. option:: --no-micro

    Disallow creation of Micro QR Codes (default)

.. option:: --no-error-boost

    Disables the automatic error correction level incrementation.
    By default, the maximal error correction level is used (without changing the
    version).

.. option:: --seq

    Creates a sequence of QR Codes (Structured Append mode).
    The :option:`--version` or :option:`--symbol-count` must be provided

.. option:: --symbol-count SYMBOL_COUNT, -sc SYMBOL_COUNT

    Number of symbols to create

.. option:: --border BORDER, -b BORDER

    Size of the border / quiet zone of the output.
    By default, the standard border (4 modules for QR Codes, 2 modules for
    Micro QR Codes) will be used. A value of 0 omits the border


Output Options
~~~~~~~~~~~~~~

.. option:: --scale SCALE, -s SCALE

    Scaling factor of the output.
    By default, a scaling factor of 1 is used which can result into too small
    images. Some output formats, i.e. SVG, accept a decimal value.

.. option:: --output OUTPUT, -o OUTPUT

    Output file.
    If not specified, the QR Code is printed to the terminal

.. option:: --compact

    Indicates that the QR code should be printed to the terminal in a more
    compact manner.


Module Colors
~~~~~~~~~~~~~

Arguments to specify the module colors. Multiple colors are supported for
SVG and PNG. The module color support varies between the serialization
formats. Most serializers support at least "--dark" and "--light".
Unsupported arguments are ignored.

.. option:: --dark DARK

    Sets the (default) color of the dark modules.
    The color may be specified as web color name, i.e. "red" or as hexadecimal
    value, i.e. "#0033cc". Some serializers, i.e. SVG and PNG, support alpha
    channels (8-digit hexadecimal value) and some support "transparent" as color
    value. The standard color is black

.. option:: --light LIGHT

    Sets the (default) color of the light modules.
    The standard value is either white or transparent.
    See :option:`--dark` for a description of allowed values.

.. option:: --align-dark ALIGN_DARK

    Sets the color of the dark modules of the alignment patterns.
    See :option:`--dark` for a description of allowed values.

.. option:: --align-light ALIGN_LIGHT

    Sets the color of the light modules of the alignment patterns.
    See :option:`--dark` for a description of allowed values.

.. option:: --dark-module DARK_MODULE

    Sets the color of the dark module.
    See :option:`--dark` for a description of allowed values.

.. option:: --data-dark DATA_DARK

    Sets the color of the dark data modules.
    See :option:`--dark` for a description of allowed values.

.. option:: --data-light DATA_LIGHT

    Sets the color of the light data modules.
    See :option:`--dark` for a description of allowed values.

.. option:: --finder-dark FINDER_DARK

    Sets the color of the dark modules of the finder pattern.
    See :option:`--dark` for a description of allowed values.

.. option:: --finder-light FINDER_LIGHT

    Sets the color of the light modules of the finder pattern.
    See :option:`--dark` for a description of allowed values.

.. option:: --format-dark FORMAT_DARK

    Sets the color of the dark modules of the format information.
    See :option:`--dark` for a description of allowed values.

.. option:: --format-light FORMAT_LIGHT

    Sets the color of the light modules of the format information.
    See :option:`--dark` for a description of allowed values.

.. option:: --quiet-zone QUIET_ZONE

    Sets the color of the quiet zone (border).
    See :option:`--dark` for a description of allowed values.

.. option:: --separator SEPARATOR

    Sets the color of the separator.
    See :option:`--dark` for a description of allowed values.

.. option:: --timing-dark TIMING_DARK

    Sets the color of the dark modules of the timing pattern.
    See :option:`--dark` for a description of allowed values.

.. option:: --timing-light TIMING_LIGHT

    Sets the color of the light modules of the timing pattern.
    See :option:`--dark` for a description of allowed values.

.. option:: --version-dark VERSION_DARK

    Sets the color of the dark modules of the version information.
    See :option:`--dark` for a description of allowed values.

.. option:: --version-light VERSION_LIGHT

    Sets the color of the light modules of the version information.
    See :option:`--dark` for a description of allowed values.


SVG Options
~~~~~~~~~~~

.. option:: --no-classes

    Omits the (default) SVG classes

.. option:: --no-xmldecl

    Omits the XML declaration header

.. option:: --no-namespace

    Indicates that the SVG document should have no SVG namespace declaration

.. option:: --no-newline

    Indicates that the SVG document should have no trailing newline

.. option:: --title TITLE

    Specifies the title of the SVG document

.. option:: --desc DESC

    Specifies the description of the SVG document

.. option:: --svgid SVGID

    Indicates the ID of the <svg/> element

.. option:: --svgclass SVGCLASS

    Indicates the CSS class of the <svg/> element (default: 'segno').
    An empty string omits the attribute.

.. option:: --lineclass LINECLASS

    Indicates the CSS class of the <path/> elements.
    An empty string omits the attribute.

.. option:: --no-size

    Indicates that the SVG document should not have "width" and "height" attributes

.. option:: --unit UNIT

    Indicates SVG coordinate system unit

.. option:: --svgversion SVGVERSION

    Indicates the SVG version

.. option:: --svgencoding ENCODING

    Specifies the encoding of the document

.. option:: --draw-transparent

    Indicates if invisible paths should be added to the SVG document.
    By default all transparent paths are omitted.


PNG Options
~~~~~~~~~~~

.. option:: --dpi DPI

    Sets the DPI value of the PNG file


Exit Status
-----------
:program:`segno` exits 0 on success, and 1 if an error occurs.


Examples
--------

.. code-block:: bash

    $ segno "Up jumped the devil"

Prints a 2-Q QR code to the terminal


.. code-block:: bash

    $ segno --compact "I am the walrus"

Prints a 1-L QR code to the terminal in a more compact manner


.. code-block:: bash

    $ segno -o=yesterday.png "Yesterday"

Saves the 1-Q QR code as PNG image.


.. code-block:: bash

    $ segno -o=fool.svg --title="Example QR code" "The Fool on the Hill"

Saves the 2-Q QR code as SVG document with the given title.


.. code-block:: bash

    $ segno -o=a-day-in-the-life.svg --scale=10 --dark darkblue "A Day in the Life"

Saves the 1-L QR code as SVG document, using a scaling factor of 10 and the
dark modules use the color "darkblue" instead of black.


.. code-block:: bash

    $ segno -o rain.png -s 4 --dark "#003399" --micro RAIN


Saves the Micro QR Code (M2-M) as PNG image, using the color #003399 for dark
modules. Each module corresponds to 4 x 4 pixels because the scaling factor
was set to 4.
