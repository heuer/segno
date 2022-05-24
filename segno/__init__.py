# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2022 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
QR Code and Micro QR Code implementation.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.
"""
from __future__ import absolute_import, unicode_literals
import sys
import io
from . import encoder
from .encoder import DataOverflowError
from . import writers, utils
try:  # pragma: no cover
    str_type = basestring  # noqa: F821
except NameError:  # pragma: no cover
    str_type = str

__version__ = '1.5.2'

__all__ = ('make', 'make_qr', 'make_micro', 'make_sequence', 'QRCode',
           'QRCodeSequence', 'DataOverflowError')


# <https://wiki.python.org/moin/PortingToPy3k/BilingualQuickRef#New_Style_Classes>
__metaclass__ = type


def make(content, error=None, version=None, mode=None, mask=None, encoding=None,
         eci=False, micro=None, boost_error=True):
    """\
    Creates a (Micro) QR Code.

    This is main entry point to create QR Codes and Micro QR Codes.

    Aside from `content`, all parameters are optional and an optimal (minimal)
    (Micro) QR code with a maximal error correction level is generated.

    :param content: The data to encode. Either a Unicode string, an integer or
            bytes. If bytes are provided, the `encoding` parameter should be
            used to specify the used encoding.
    :type content: str, int, bytes
    :param error: Error correction level. If ``None`` (default), error
            correction level ``L`` is used (note: Micro QR Code version M1 does
            not support any error correction. If an explicit error correction
            level is used, a M1 QR code won't be generated).
            Valid values: ``None`` (allowing generation of M1 codes or use error
            correction level "L" or better see :paramref:`boost_error <segno.make.boost_error>`),
            "L", "M", "Q", "H" (error correction level "H" isn't available for
            Micro QR Codes).

            =====================================   ===========================
            Error correction level                  Error correction capability
            =====================================   ===========================
            L (Segno's default unless version M1)   recovers  7% of data
            M                                       recovers 15% of data
            Q                                       recovers 25% of data
            H (not available for Micro QR Codes)    recovers 30% of data
            =====================================   ===========================

            Higher error levels may require larger QR codes (see also
            :paramref:`version <segno.make.version>` parameter).

            The `error` parameter is case insensitive.

            See also the :paramref:`boost_error <segno.make.boost_error>` parameter.
    :type error: str or None
    :param version: QR Code version. If the value is ``None`` (default), the
            minimal version which fits for the input data will be used.
            Valid values: "M1", "M2", "M3", "M4" (for Micro QR codes) or an
            integer between 1 and 40 (for QR codes).
            The `version` parameter is case insensitive.
    :type version: int, str or None
    :param mode: "numeric", "alphanumeric", "byte", "kanji" or "hanzi".
            If the value is ``None`` (default) the appropriate mode will
            automatically be determined.
            If `version` refers to a Micro QR code, this function may raise a
            :py:exc:`ValueError` if the provided `mode` is not supported.

            The `mode` parameter is case insensitive.

            ============    =======================
            Mode            (Micro) QR Code Version
            ============    =======================
            numeric         1 - 40, M1, M2, M3, M4
            alphanumeric    1 - 40,     M2, M3, M4
            byte            1 - 40,         M3, M4
            kanji           1 - 40,         M3, M4
            hanzi           1 - 40
            ============    =======================

            .. note::
                The Hanzi mode may not be supported by all QR code readers since
                it is not part of ISO/IEC 18004:2015(E).
                For this reason, this mode must be specified explicitly by the
                user::

                    import segno
                    qrcode = segno.make('书读百遍其义自现', mode='hanzi')

    :type mode: str or None
    :param mask: Data mask. If the value is ``None`` (default), the
            appropriate data mask is chosen automatically. If the `mask`
            parameter is provided, this function may raise a :py:exc:`ValueError`
            if the mask is invalid.
    :type mask: int or None
    :param encoding: Indicates the encoding in mode "byte". By default
            (`encoding` is ``None``) the implementation tries to use the
            standard conform ISO/IEC 8859-1 encoding and if it does not fit, it
            will use UTF-8. Note that no ECI mode indicator is inserted by
            default (see :paramref:`eci <segno.make.eci>`).
            The `encoding` parameter is case insensitive.
    :type encoding: str or None
    :param bool eci: Indicates if binary data which does not use the default
            encoding (ISO/IEC 8859-1) should enforce the ECI mode. Since a lot
            of QR code readers do not support the ECI mode, this feature is
            disabled by default and the data is encoded in the provided
            `encoding` using the usual "byte" mode. Set `eci` to ``True`` if
            an ECI header should be inserted into the QR Code. Note that
            the implementation may not know the ECI designator for the provided
            `encoding` and may raise an exception if the ECI designator cannot
            be found.
            The ECI mode is not supported by Micro QR Codes.
    :param micro: If :paramref:`version <segno.make.version>` is ``None`` (default)
            this parameter can be used to allow the creation of a Micro QR code.
            If set to ``False``, a QR code is generated. If set to
            ``None`` (default) a Micro QR code may be generated if applicable.
            If set to ``True`` the algorithm generates a Micro QR Code or
            raises an exception if the `mode` is not compatible or the `content`
            is too large for Micro QR codes.
    :type micro: bool or None
    :param bool boost_error: Indicates if the error correction level may be
            increased if it does not affect the version (default: ``True``).
            If set to ``True``, the :paramref:`error <segno.make.error>`
            parameter is interpreted as minimum error level. If set to ``False``,
            the resulting (Micro) QR code uses the provided `error` level
            (or the default error correction level, if error is ``None``)
    :raises: :py:exc:`ValueError` or :py:exc:`DataOverflowError`: In case the
             data does not fit into a (Micro) QR Code or it does not fit into
             the provided :paramref:`version`.
    :rtype: QRCode
    """
    return QRCode(encoder.encode(content, error, version, mode, mask, encoding,
                                 eci, micro, boost_error=boost_error))


def make_qr(content, error=None, version=None, mode=None, mask=None,
            encoding=None, eci=False, boost_error=True):
    """\
    Creates a QR code (never a Micro QR code).

    See :py:func:`make` for a description of the parameters.

    :rtype: QRCode
    """
    return make(content, error=error, version=version, mode=mode, mask=mask,
                encoding=encoding, eci=eci, micro=False, boost_error=boost_error)


def make_micro(content, error=None, version=None, mode=None, mask=None,
               encoding=None, boost_error=True):
    """\
    Creates a Micro QR code.

    See :py:func:`make` for a description of the parameters.

    Note: Error correction level "H" isn't available for Micro QR codes. If
    used, this function raises a :py:class:`segno.ErrorLevelError`.

    :rtype: QRCode
    """
    return make(content, error=error, version=version, mode=mode, mask=mask,
                encoding=encoding, micro=True, boost_error=boost_error)


def make_sequence(content, error=None, version=None, mode=None, mask=None,
                  encoding=None, boost_error=True, symbol_count=None):
    """\
    Creates a sequence of QR codes using the Structured Append mode.

    If the content fits into one QR code and neither ``version`` nor
    ``symbol_count`` is provided, this function may return a sequence with
    one QR Code which does not use the Structured Append mode. Otherwise a
    sequence of 2 .. n  (max. n = 16) QR codes is returned which use the
    Structured Append mode.

    The Structured Append mode allows to split the content over a number
    (max. 16) QR Codes.

    The Structured Append mode isn't available for Micro QR Codes, therefor
    the returned sequence contains QR codes, only.

    Since this function returns an iterable object, it may be used as follows:

    .. code-block:: python

        for i, qrcode in enumerate(segno.make_sequence(data, symbol_count=2)):
             qrcode.save('seq-%d.svg' % i, scale=10, color='darkblue')

    The number of QR codes is determined by the `version` or `symbol_count`
    parameter.

    See :py:func:`make` for a description of the other parameters.

    :param int symbol_count: Number of symbols.
    :rtype: QRCodeSequence
    """
    return QRCodeSequence(map(QRCode,
                              encoder.encode_sequence(content, error=error,
                                                      version=version,
                                                      mode=mode, mask=mask,
                                                      encoding=encoding,
                                                      boost_error=boost_error,
                                                      symbol_count=symbol_count)))


class QRCode:
    """\
    Represents a (Micro) QR Code.
    """
    __slots__ = ('matrix', 'mask', '_version', '_error', '_mode')

    def __init__(self, code):
        """\
        Initializes the QR Code object.

        :param code: An object with a ``matrix``, ``version``, ``error``,
            ``mask`` and ``segments`` attribute.
        """
        self.matrix = code.matrix
        """Returns the matrix.

        :rtype: tuple of :py:class:`bytearray` instances.
        """
        self.mask = code.mask
        """Returns the data mask pattern reference

        :rtype: int
        """
        self._version = code.version
        self._error = code.error
        self._mode = code.segments[0].mode if len(code.segments) == 1 else None

    @property
    def version(self):
        """\
        (Micro) QR Code version. Either a string ("M1", "M2", "M3", "M4") or
        an integer in the range of 1 .. 40.

        :rtype: str or int
        """
        return encoder.get_version_name(self._version)

    @property
    def error(self):
        """\
        Error correction level; either a string ("L", "M", "Q", "H") or ``None``
        if the QR code provides no error correction (Micro QR Code version M1)

        :rtype: str
        """
        if self._error is None:
            return None
        return encoder.get_error_name(self._error)

    @property
    def mode(self):
        """\
        String indicating the mode ("numeric", "alphanumeric", "byte", "kanji",
        or "hanzi").
        May be ``None`` if multiple modes are used.

        :rtype: str or None
        """
        if self._mode is not None:
            return encoder.get_mode_name(self._mode)
        return None

    @property
    def designator(self):
        """\
        Returns the version and error correction level as string `V-E` where
        `V` represents the version number and `E` the error level.

        :rtype: str
        """
        version = str(self.version)
        return '-'.join((version, self.error) if self.error else (version,))

    @property
    def default_border_size(self):
        """\
        Indicates the default border size aka quiet zone.

        QR Codes have a quiet zone of four light modules, while Micro QR Codes
        have a quiet zone of two light modules.

        :rtype: int
        """
        return utils.get_default_border_size(self._version)

    @property
    def is_micro(self):
        """\
        Indicates if this QR code is a Micro QR code

        :rtype: bool
        """
        return self._version < 1

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.matrix == other.matrix

    __hash__ = None

    def symbol_size(self, scale=1, border=None):
        """\
        Returns the symbol size (width x height) with the provided border and
        scaling factor.

        :param scale: Indicates the size of a single module (default: 1).
                The size of a module depends on the used output format; i.e.
                in a PNG context, a scaling factor of 2 indicates that a module
                has a size of 2 x 2 pixel. Some outputs (i.e. SVG) accept
                floating point values.
        :type scale: int or float
        :param int border: The border size or ``None`` to specify the
                default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
        :rtype: tuple (width, height)
        """
        return utils.get_symbol_size(self._version, scale=scale, border=border)

    def matrix_iter(self, scale=1, border=None, verbose=False):
        """\
        Returns an iterator over the matrix which includes the border.

        The border is returned as sequence of light modules.
        Dark modules are reported as ``0x1``, light modules have the value
        ``0x0``.

        The following example converts the QR code matrix into a list of
        lists which use boolean values for the modules (True = dark module,
        False = light module)::

            >>> import segno
            >>> qrcode = segno.make('The Beatles')
            >>> width, height = qrcode.symbol_size(scale=2)
            >>> res = []
            >>> # Scaling factor 2, default border
            >>> for row in qrcode.matrix_iter(scale=2):
            >>>     res.append([col == 0x1 for col in row])
            >>> width == len(res[0])
            True
            >>> height == len(res)
            True

        If `verbose` is ``True``, the iterator returns integer constants which
        indicate the type of the module, i.e. ``segno.consts.TYPE_FINDER_PATTERN_DARK``,
        ``segno.consts.TYPE_FINDER_PATTERN_LIGHT``, ``segno.consts.TYPE_QUIET_ZONE`` etc.

        To check if the returned module type is dark or light, use::

            if mt >> 8:
                print('dark module')

            if not mt >> 8:
                print('light module')


        :param int scale: The scaling factor (default: ``1``).
        :param int border: The size of border / quiet zone or ``None`` to
                indicate the default border.
        :param bool verbose: Indicates if the type of the module should be returned
                instead of ``0x1`` and ``0x0`` values.
                See :py:mod:`segno.consts` for the return values.
                This feature is currently in EXPERIMENTAL state.
        :raises: :py:exc:`ValueError` if the scaling factor or the border is
                invalid (i.e. negative).
        """
        iterfn = utils.matrix_iter_verbose if verbose else utils.matrix_iter
        return iterfn(self.matrix, self._version, scale, border)

    def show(self, delete_after=20, scale=10, border=None, dark='#000',
             light='#fff'):  # pragma: no cover
        """\
        Displays this QR code.

        This method is mainly intended for debugging purposes.

        This method saves the QR code as an image (by default with a scaling
        factor of 10) to a temporary file and opens it with the standard PNG
        viewer application or within the standard webbrowser.
        The temporary file is deleted afterwards (unless
        :paramref:`delete_after <segno.QRCode.show.delete_after>` is set to ``None``).

        If this method does not show any result, try to increase the
        :paramref:`delete_after <segno.QRCode.show.delete_after>` value or set
        it to ``None``

        :param delete_after: Time in seconds to wait till the temporary file is
                deleted.
        :type delete_after: int or None
        :param int scale: Integer indicating the size of a single module.
        :param border: Integer indicating the size of the quiet zone.
                If set to ``None`` (default), the recommended border size
                will be used.
        :type border: int or None
        :param dark: The color of the dark modules (default: black).
        :param light: The color of the light modules (default: white).
        """
        import os
        import time
        import tempfile
        import webbrowser
        import threading
        try:  # Python 3
            from urllib.parse import urljoin
            from urllib.request import pathname2url
        except ImportError:  # Python 2
            from urlparse import urljoin  # noqa
            from urllib import pathname2url  # noqa

        def delete_file(name):
            time.sleep(delete_after)
            try:
                os.unlink(name)
            except OSError:
                pass

        f = tempfile.NamedTemporaryFile('wb', suffix='.png', delete=False)
        try:
            self.save(f, scale=scale, dark=dark, light=light, border=border)
        except:  # noqa: E722
            f.close()
            os.unlink(f.name)
            raise
        f.close()
        webbrowser.open_new_tab(urljoin('file:', pathname2url(f.name)))
        if delete_after is not None:
            t = threading.Thread(target=delete_file, args=(f.name,))
            t.start()

    def svg_data_uri(self, xmldecl=False, encode_minimal=False,
                     omit_charset=False, nl=False, **kw):
        """\
        Converts the QR code into an SVG data URI.

        The XML declaration is omitted by default (set
        :paramref:`xmldecl <segno.QRCode.svg_data_uri.xmldecl>` to ``True``
        to enable it), further the newline is omitted by default (set ``nl`` to
        ``True`` to enable it).

        Aside from the missing `out` parameter, the different `xmldecl` and
        `nl` default values, and the additional parameters
        :paramref:`encode_minimal <segno.QRCode.svg_data_uri.encode_minimal>`
        and :paramref:`omit_charset <segno.QRCode.svg_data_uri.omit_charset>`,
        this method uses the same parameters as the usual SVG serializer, see
        :py:func:`save` and the available `SVG parameters <#svg>`_

        .. note::
            In order to embed a SVG image in HTML without generating a file, the
            :py:func:`svg_inline` method could serve better results, as it
            usually produces a smaller output.

        :param bool xmldecl: Indicates if the XML declaration should be
                        serialized (default: ``False``)
        :param bool encode_minimal: Indicates if the resulting data URI should
                        use minimal percent encoding (disabled by default).
        :param bool omit_charset: Indicates if the ``;charset=...`` should be omitted
                        (disabled by default)
        :param bool nl: Indicates if the document should have a trailing newline
                        (default: ``False``)
        :rtype: str
        """
        return writers.as_svg_data_uri(self.matrix, self._version,
                                       xmldecl=xmldecl, nl=nl,
                                       encode_minimal=encode_minimal,
                                       omit_charset=omit_charset, **kw)

    def svg_inline(self, **kw):
        """\
        Returns an SVG representation which is embeddable into HTML5 contexts.

        Due to the fact that HTML5 directly supports SVG, various elements of
        an SVG document can or should be suppressed (i.e. the XML declaration and
        the SVG namespace).

        This method returns a string that can be used in an HTML context.

        This method uses the same parameters as the usual SVG serializer, see
        :py:func:`save` and the available `SVG parameters <#svg>`_ (the ``out``
        and ``kind`` parameters are not supported).

        The returned string can be used directly in
        `Jinja <https://jinja.palletsprojects.com/>`_ and
        `Django <https://www.djangoproject.com/>`_ templates, provided the
        ``safe`` filter is used which marks a string as not requiring further
        HTML escaping prior to output.
        ::

            <div>{{ qr.svg_inline(dark='#228b22', scale=3) | safe }}</div>

        :rtype: str
        """
        buff = io.BytesIO()
        self.save(buff, kind='svg', xmldecl=False, svgns=False, nl=False, **kw)
        return buff.getvalue().decode(kw.get('encoding', 'utf-8'))

    def png_data_uri(self, **kw):
        """\
        Converts the QR code into a PNG data URI.

        Uses the same keyword parameters as the usual PNG serializer,
        see :py:func:`save` and the available `PNG parameters <#png>`_

        :rtype: str
        """
        return writers.as_png_data_uri(self.matrix, self._version, **kw)

    def terminal(self, out=None, border=None, compact=False):
        """\
        Serializes the matrix as ANSI escape code or Unicode Block Elements
        (if ``compact`` is ``True``).

        Under Windows, no ANSI escape sequence is generated but the Windows
        API is used *unless* :paramref:`out <segno.QRCode.terminal.out>`
        is a writable object or using WinAPI fails or if ``compact`` is ``True``.

        :param out: Filename or a file-like object supporting to write text.
                If ``None`` (default), the matrix is written to :py:class:`sys.stdout`.
        :param int border: Integer indicating the size of the quiet zone.
                If set to ``None`` (default), the recommended border size
                will be used (``4`` for QR Codes, ``2`` for Micro QR Codes).
        :param bool compact: Indicates if a more compact QR code should be shown
                (default: ``False``).
        """
        if compact:
            writers.write_terminal_compact(self.matrix, self._version, out or sys.stdout, border)
        elif out is None and sys.platform == 'win32':  # pragma: no cover
            # Windows < 10 does not support ANSI escape sequences, try to
            # call the a Windows specific terminal output which uses the
            # Windows API.
            try:
                writers.write_terminal_win(self.matrix, self._version, border)
            except OSError:
                # Use the standard output even if it may print garbage
                writers.write_terminal(self.matrix, self._version, sys.stdout, border)
        else:
            writers.write_terminal(self.matrix, self._version, out or sys.stdout, border)

    def save(self, out, kind=None, **kw):
        """\
        Serializes the QR code in one of the supported formats.
        The serialization format depends on the filename extension.

        .. _common_keywords:

        **Common keywords**

        ==========    ==============================================================
        Name          Description
        ==========    ==============================================================
        scale         Integer or float indicating the size of a single module.
                      Default: 1. The interpretation of the scaling factor depends
                      on the serializer. For pixel-based output (like :ref:`PNG <png>`)
                      the scaling factor is interpreted as pixel-size (1 = 1 pixel).
                      :ref:`EPS <eps>` interprets ``1`` as 1 point (1/72 inch) per
                      module.
                      Some serializers (like :ref:`SVG <svg>`) accept float values.
                      If the serializer does not accept float values, the value will be
                      converted to an integer value (note: int(1.6) == 1).
        border        Integer indicating the size of the quiet zone.
                      If set to ``None`` (default), the recommended border size
                      will be used (``4`` for QR codes, ``2`` for a Micro QR codes).
                      A value of ``0`` indicates that border should be omitted.
        dark          A string or tuple representing a color value for the dark
                      modules. The default value is "black".  The color can be
                      provided as ``(R, G, B)`` tuple, as web color name
                      (like "red") or in hexadecimal format (``#RGB`` or
                      ``#RRGGBB``). Some serializers (i.e. :ref:`SVG <svg>` and
                      :ref:`PNG <png>`) accept an alpha transparency value like
                      ``#RRGGBBAA``.
        light         A string or tuple representing a color for the light modules.
                      See `dark` for valid values.
                      The default value depends on the serializer. :ref:`SVG <svg>`
                      uses no color (``None``) for light modules by default, other
                      serializers, like :ref:`PNG <png>`, use "white" as default
                      light color.
        ==========    ==============================================================


        .. _module_colors:

        **Module Colors**

        ===============    =======================================================
        Name               Description
        ===============    =======================================================
        finder_dark        Color of the dark modules of the finder patterns
                           Default: undefined, use value of "dark"
        finder_light       Color of the light modules of the finder patterns
                           Default: undefined, use value of "light"
        data_dark          Color of the dark data modules
                           Default: undefined, use value of "dark"
        data_light         Color of the light data modules.
                           Default: undefined, use value of "light".
        version_dark       Color of the dark modules of the version information.
                           Default: undefined, use value of "dark".
        version_light      Color of the light modules of the version information,
                           Default: undefined, use value of "light".
        format_dark        Color of the dark modules of the format information.
                           Default: undefined, use value of "dark".
        format_light       Color of the light modules of the format information.
                           Default: undefined, use value of "light".
        alignment_dark     Color of the dark modules of the alignment patterns.
                           Default: undefined, use value of "dark".
        alignment_light    Color of the light modules of the alignment patterns.
                           Default: undefined, use value of "light".
        timing_dark        Color of the dark modules of the timing patterns.
                           Default: undefined, use value of "dark".
        timing_light       Color of the light modules of the timing patterns.
                           Default: undefined, use value of "light".
        separator          Color of the separator.
                           Default: undefined, use value of "light".
        dark_module        Color of the dark module (a single dark module which
                           occurs in all QR Codes but not in Micro QR Codes.
                           Default: undefined, use value of "dark".
        quiet_zone         Color of the quiet zone / border.
                           Default: undefined, use value of "light".
        ===============    =======================================================


        .. _svg:

        **Scalable Vector Graphics (SVG)**

        All :ref:`common keywords <common_keywords>` and :ref:`module colors <module_colors>`
        are supported.

        ================ ==============================================================
        Name             Description
        ================ ==============================================================
        out              Filename or :py:class:`io.BytesIO`
        kind             "svg" or "svgz" (to create a gzip compressed SVG)
        scale            integer or float
        dark             Default: "#000" (black)
                         ``None`` is a valid value. If set to ``None``, the resulting
                         path won't have a "stroke" attribute. The "stroke" attribute
                         may be defined via CSS (external).
                         If an alpha channel is defined, the output depends of the
                         used SVG version. For SVG versions >= 2.0, the "stroke"
                         attribute will have a value like "rgba(R, G, B, A)", otherwise
                         the path gets another attribute "stroke-opacity" to emulate
                         the alpha channel.
                         To minimize the document size, the SVG serializer uses
                         automatically the shortest color representation: If
                         a value like "#000000" is provided, the resulting
                         document will have a color value of "#000". If the color
                         is "#FF0000", the resulting color is not "#F00", but
                         the web color name "red".
        light            Default value ``None``. If this parameter is set to another
                         value, the resulting image will have another path which
                         is used to define the color of the light modules.
                         If an alpha channel is used, the resulting path may
                         have a "fill-opacity" attribute (for SVG version < 2.0)
                         or the "fill" attribute has a "rgba(R, G, B, A)" value.
        xmldecl          Boolean value (default: ``True``) indicating whether the
                         document should have an XML declaration header.
                         Set to ``False`` to omit the header.
        svgns            Boolean value (default: ``True``) indicating whether the
                         document should have an explicit SVG namespace declaration.
                         Set to ``False`` to omit the namespace declaration.
                         The latter might be useful if the document should be
                         embedded into a HTML 5 document where the SVG namespace
                         is implicitly defined.
        title            String (default: ``None``) Optional title of the generated
                         SVG document.
        desc             String (default: ``None``) Optional description of the
                         generated SVG document.
        svgid            A string indicating the ID of the SVG document
                         (if set to ``None`` (default), the SVG element won't have
                         an ID).
        svgclass         Default: "segno". The CSS class of the SVG document
                         (if set to ``None``, the SVG element won't have a class).
        lineclass        Default: "qrline". The CSS class of the path element
                         (which draws the dark modules (if set to ``None``, the path
                         won't have a class).
        omitsize         Indicates if width and height attributes should be
                         omitted (default: ``False``). If these attributes are
                         omitted, a ``viewBox`` attribute will be added to the
                         document.
        unit             Default: ``None``
                         Indicates the unit for width / height and other coordinates.
                         By default, the unit is unspecified and all values are
                         in the user space.
                         Valid values: em, ex, px, pt, pc, cm, mm, in, and percentages
                         (any string is accepted, this parameter is not validated
                         by the serializer)
        encoding         Encoding of the XML document. "utf-8" by default.
        svgversion       SVG version (default: ``None``). If specified (a float),
                         the resulting document has an explicit "version" attribute.
                         If set to ``None``, the document won't have a "version"
                         attribute. This parameter is not validated.
        compresslevel    Default: 9. This parameter is only valid, if a compressed
                         SVG document should be created (file extension "svgz").
                         1 is fastest and produces the least compression, 9 is slowest
                         and produces the most. 0 is no compression.
        draw_transparent Indicates if transparent SVG paths should be
                         added to the graphic (default: ``False``)
        nl               Indicates if the document should have a trailing newline
                         (default: ``True``)
        ================ ==============================================================


        .. _png:

        **Portable Network Graphics (PNG)**

        This writes either a grayscale (maybe with transparency) PNG (color type 0)
        or a palette-based (maybe with transparency) image (color type 3).
        If the dark / light values are ``None``, white or black, the serializer
        chooses the more compact grayscale mode, in all other cases a palette-based
        image is written.

        All :ref:`common keywords <common_keywords>` and :ref:`module colors <module_colors>`
        are supported.

        ===============    ==============================================================
        Name               Description
        ===============    ==============================================================
        out                Filename or :py:class:`io.BytesIO`
        kind               "png"
        scale              integer
        dark               Default: "#000" (black)
                           ``None`` is a valid value iff light is not ``None``.
                           If set to ``None``, the dark modules become transparent.
        light              Default value "#fff" (white)
                           See keyword "dark" for further details.
        compresslevel      Default: 9. Integer indicating the compression level
                           for the ``IDAT`` (data) chunk.
                           1 is fastest and produces the least compression, 9 is slowest
                           and produces the most. 0 is no compression.
        dpi                Default: ``None``. Specifies the DPI value for the image.
                           By default, the DPI value is unspecified. Please note
                           that the DPI value is converted into meters (maybe with
                           rounding errors) since PNG does not support the unit
                           "dots per inch".
        ===============    ==============================================================


        .. _eps:

        **Encapsulated PostScript (EPS)**

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.StringIO`
        kind             "eps"
        scale            integer or float
        dark             Default: "#000" (black)
        light            Default value: ``None`` (transparent light modules)
        =============    ==============================================================


        .. _pdf:

        **Portable Document Format (PDF)**

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.BytesIO`
        kind             "pdf"
        scale            integer or float
        dark             Default: "#000" (black)
        light            Default value: ``None`` (transparent light modules)
        compresslevel    Default: 9. Integer indicating the compression level.
                         1 is fastest and produces the least compression, 9 is slowest
                         and produces the most. 0 is no compression.
        =============    ==============================================================


        .. _txt:

        **Text (TXT)**

        Aside of "scale", all :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.StringIO`
        kind             "txt"
        dark             Default: "1"
        light            Default: "0"
        =============    ==============================================================


        .. _ansi:

        **ANSI escape code**

        Supports the "border" keyword, only!

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.StringIO`
        kind             "ans"
        =============    ==============================================================


        .. _pbm:

        **Portable Bitmap (PBM)**

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.BytesIO`
        kind             "pbm"
        scale            integer
        plain            Default: False. Boolean to switch between the P4 and P1 format.
                         If set to ``True``, the (outdated) P1 serialization format is
                         used.
        =============    ==============================================================


        .. _pam:

        **Portable Arbitrary Map (PAM)**

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.BytesIO`
        kind             "pam"
        scale            integer
        dark             Default: "#000" (black).
        light            Default value "#fff" (white). Use ``None`` for transparent
                         light modules.
        =============    ==============================================================


        .. _ppm:

        **Portable Pixmap (PPM)**

        All :ref:`common keywords <common_keywords>` and :ref:`module colors <module_colors>`
        are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.BytesIO`
        kind             "ppm"
        scale            integer
        dark             Default: "#000" (black).
        light            Default value "#fff" (white).
        =============    ==============================================================



        .. _latex:

        **LaTeX / PGF/TikZ**

        To use the output of this serializer, the ``PGF/TikZ`` (and optionally
        ``hyperref``) package is required in the LaTeX environment. The
        serializer itself does not depend on any external packages.

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.StringIO`
        kind             "tex"
        scale            integer or float
        dark             LaTeX color name (default: "black"). The color is written
                         "at it is", please ensure that the color is a standard color
                         or it has been defined in the enclosing LaTeX document.
        url              Default: ``None``. Optional URL where the QR code should
                         point to. Requires the ``hyperref`` package in the LaTeX
                         environment.
        =============    ==============================================================


        .. _xbm:

        **X BitMap (XBM)**

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.StringIO`
        kind             "xbm"
        scale            integer
        name             Name of the variable (default: "img")
        =============    ==============================================================


        .. _xpm:

        **X PixMap (XPM)**

        All :ref:`common keywords <common_keywords>` are supported.

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        out              Filename or :py:class:`io.StringIO`
        kind             "xpm"
        scale            integer
        dark             Default: "#000" (black).
                         ``None`` indicates transparent dark modules.
        light            Default value "#fff" (white)
                         ``None`` indicates transparent light modules.
        name             Name of the variable (default: "img")
        =============    ==============================================================


        :param out: A filename or a writable file-like object with a
                ``name`` attribute. Use the :paramref:`kind <segno.QRCode.save.kind>`
                parameter if `out` is a :py:class:`io.BytesIO` or
                :py:class:`io.StringIO` stream which don't have a ``name``
                attribute.
        :param str kind: Default ``None``.
                If the desired output format cannot be determined from
                the :paramref:`out <segno.QRCode.save.out>` parameter, this
                parameter can be used to indicate the serialization format
                (i.e. "svg" to enforce SVG output). The value is case
                insensitive.
        :param kw: Any of the supported keywords by the specific serializer.
        """
        writers.save(self.matrix, self._version, out, kind, **kw)

    def __getattr__(self, name):
        """\
        This is used to plug-in external serializers.

        When a "to_<name>" method is invoked, this method tries to find
        a ``segno.plugin.converter`` plugin with the provided ``<name>``.
        If such a plugin exists, a callable function is returned. The result
        of invoking the function depends on the plugin.
        """
        if name.startswith('to_'):
            from pkg_resources import iter_entry_points
            from functools import partial
            for ep in iter_entry_points(group='segno.plugin.converter',
                                        name=name[3:]):
                plugin = ep.load()
                return partial(plugin, self)
        raise AttributeError('{0} object has no attribute {1}'
                             .format(self.__class__, name))


class QRCodeSequence(tuple):
    """\
    Represents a sequence of  1 .. n (max. n = 16) :py:class:`QRCode` instances.

    Iff this sequence contains only one item, it behaves like :py:class:`QRCode`.
    """
    __slots__ = ()

    def __new__(cls, qrcodes):
        return super(QRCodeSequence, cls).__new__(cls, qrcodes)

    def terminal(self, out=None, border=None, compact=False):
        """\
        Serializes the sequence of QR codes as ANSI escape code.

        See :py:meth:`QRCode.terminal()` for details.
        """
        for qrcode in self:
            qrcode.terminal(out=out, border=border, compact=compact)

    def save(self, out, kind=None, **kw):
        """\
        Saves the sequence of QR codes to `out`.

        If `out` is a filename, this method modifies the filename and adds
        ``<Number of QR codes>-<Current QR code>`` to it.
        ``structured-append.svg`` becomes (if the sequence contains two QR codes):
        ``structured-append-02-01.svg`` and ``structured-append-02-02.svg``

        Please note that using a file or file-like object may result into an
        invalid serialization format since all QR codes are written to the same
        output.

        See :py:meth:`QRCode.save()` for a detailed enumeration of options.
        """
        filename = lambda o, n: o  # noqa: E731
        m = len(self)
        if m > 1 and isinstance(out, str_type):
            dot_idx = out.rfind('.')
            if dot_idx > -1:
                out = out[:dot_idx] + '-{0:02d}-{1:02d}' + out[dot_idx:]
                filename = lambda o, n: o.format(m, n)  # noqa: E731
        for n, qrcode in enumerate(self, start=1):
            qrcode.save(filename(out, n), kind=kind, **kw)

    def __getattr__(self, item):
        """\
        Behaves like :py:class:`QRCode` iff this sequence contains a single item.
        """
        if len(self) == 1:
            return getattr(self[0], item)
        raise AttributeError("{0} object has no attribute '{1}'"
                             .format(self.__class__, item))
