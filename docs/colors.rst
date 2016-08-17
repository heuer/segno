Colors
======

Almost all serializers support custom settings for the color of the dark modules
and the background (light modules) of a (Micro) QR Code.

The color values can be provides as tuple (``(R, G, B)``), as web color name
(like 'red') or as hexadecimal ``#RRGGBB`` value (i.e. '#085A75'). If alpha
transparency is supported (i.e. PNG and SVG), hexadecimal values like
``#RRGGBBAA`` are accepted.

The color values are automatically converted into a meaningful value of the
specific output format (note that providing an alpha channel to a serializer
which does not accept an alpha channel results into an error).



