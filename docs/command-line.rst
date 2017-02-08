QR Code creation from the command line
======================================

The command line script "segno" can be used to print QR Codes to the
terminal or to save them as file (SVG, PNG, EPS, ...).

By default, the script does not create Micro QR Codes, use ``--micro`` to
allow the creation of Micro QR Codes or specify the version (like ``--version=M3``)
to create a Micro QR Code.


Usage
-----

Output the QR Code to the terminal::

    $ segno "Little wing"


Same content, but as Micro QR Code (M4)::

    $ segno --micro "Little wing"


Version
^^^^^^^

If the ``version`` parameter is not provided, Segno chooses the minimal version
for the QR Code automatically. The version may be specified as integer or as
Micro QR Code identifier.

The content 'Layla' would fit into a version 1 QR Code, but the following command
enforces version 5::

    $ segno --version=5 Layla
    $ segno -v=5 Layla


Micro QR Code::

    $ segno -v m4 Layla
    $ segno --version M4 Layla


Error correction level
^^^^^^^^^^^^^^^^^^^^^^

The default error correction level is "L", use the ``error`` parameter to change
it::

    $ segno --error=q "Ain't no grave"
    $ segno -e=h "Heart of Gold"


QR Code serialization
^^^^^^^^^^^^^^^^^^^^^

Printing the QR Codes to the terminal is nice but the ``output`` parameter
serializes the QR Code in one of the supported file formats::

    $ segno --output=white-room.png "White Room"
    $ segno -o=satellite.svg "Satellite Of Love"
    $ segno --output=mrs.eps "Mrs. Robinson"
    $ segno --output=dedodo.pdf "De Do Do Do, De Da Da Da"
    $ segno --output=tin-pan-alley.svgz "Tin Pan Alley"
    $ segno --output=thrill-gone.txt "The Thrill Is Gone"


Scaling QR Codes
^^^^^^^^^^^^^^^^

If the resulting QR Code is too small, ``scale`` can be used to create a more
appropriate output::

    $ segno --scale=10 --output=money-talks.png "Money Talks"

If the serializer does not support a scaling factor (i.e. text output), this
parameter is ignored.


Changing the size of the quiet zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated QR Codes will have a recommended quiet zone / border around the
symbol. To change the size of the border, ``border`` can be utilized::

    $ segno --border=0 --output=black-magic-woman.svg "Black Magic Woman"
    $ segno --border=10 --output=diamond.png "Shine On You Crazy Diamond"


Colors
^^^^^^

Usually, all QR Codes are serialized in black and white. Use ``color``
to change the color of the dark modules and ``background`` to change the
color of the light modules. If the color or background should be transparent,
set the value to "transparent"::

    $ segno --color=darkblue --output=excited.png "So Excited"
    $ segno --background=transparent --output=hotel.png "Hotel California"
    $ segno --color=transparent --output=dontgiveup.svg "Don't Give Up"

If the serializer does not support ``color`` or ``background``, these arguments
are ignored.

