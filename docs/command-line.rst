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

    $ segno "Little wing" --micro


Version
^^^^^^^

If the ``version`` parameter is not provided, Segno chooses the minimal version
for the QR Code automatically. The version may be specified as integer or as
Micro QR Code identifier.

The content 'Layla' would fit into a version 1 QR Code, but the following command
enforces version 5::

    $ segno "Layla" --version=5
    $ segno "Layla" -v=5


Micro QR Code::

    $ segno "Layla" -v=m4
    $ segno "Layla" --version=M4


Error correction level
^^^^^^^^^^^^^^^^^^^^^^

The default error correction level is "M", use the ``error`` parameter to change
it::

    $ segno "Ain't no grave" --error=q
    $ segno "Heart of Gold" -e=h


QR Code serialization
^^^^^^^^^^^^^^^^^^^^^

Printing the QR Codes to the terminal is nice but the ``output`` parameter
serializes the QR Code in one of the supported file formats::

    $ segno "White Room" --output=white-room.png
    $ segno "Satellite Of Love" -o=satellite.svg
    $ segno "Mrs. Robinson" --output=mrs.eps
    $ segno "De Do Do Do, De Da Da Da" --output=dedodo.pdf
    $ segno "Tin Pan Alley" --output=tin-pan-alley.svgz
    $ segno "The Thrill Is Gone" --output=thrill-gone.txt


Scaling QR Codes
^^^^^^^^^^^^^^^^

If the resulting QR Code is too small, ``scale`` can be used to create a more
appropriate output::

    $ segno "Money Talks" --scale=10 --output=money-talks.png

If the serializer does not support a scaling factor (i.e. text output), this
parameter is ignored.


Changing the size of the quiet zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated QR Codes will have a recommended quiet zone / border around the
symbol. To change the size of the border, ``border`` can be utilized::

    $ segno "Black Magic Woman" --border=0 --output=black-magic-woman.svg
    $ segno "Shine On You Crazy Diamond" --border=10 --output=diamond.png


Colors
^^^^^^

Usually, all QR Codes are serialized in black and white. Use ``color``
to change the color of the dark modules and ``background`` to change the
color of the light modules. If the color or background should be transparent,
set the value to "transparent"::

    $ segno "So Excited" --color=darkblue --output=excited.png
    $ segno "Hotel California" --background=transparent --output=hotel.png
    $ segno "Don't Give Up" --color=transparent --output=dontgiveup.svg

If the serializer does not support ``color`` or ``background``, these arguments
are ignored.

