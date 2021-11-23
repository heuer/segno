Writing plugins for Segno
=========================

:py:class:`segno.QRCode` provides a plugin architecture which utilizes egg
entry points.

All plugins must use the ``segno.plugin.converter`` entry point to be recognized.
If a plugin is detected, the user may use the the plugin by calling ``to_XXX``
where ``XXX`` refers to the plugin name.

The specific plugin is invoked by providing the :py:class:`segno.QRCode`
instance and any further arguments or keywords.


Simple plugin
-------------

This section explains how to write a plugin which writes to ``stdout`` and uses
``X`` for dark modules and ``_`` for light modules.

Content of ``simple_plugin.py``:

.. code-block:: python

    import sys

    def write(qrcode):
        write = sys.stdout.write
        for row in qrcode.matrix:
            for col in row:
                write('X' if col else '_')
            write('\n')


``setup.py``:

.. code-block:: python

    setup(
        name='simple-plugin',
        version='1.0',
        license='BSD',
        author='John Doe',
        author_email='john@example.org',
        platforms=['any'],
        py_modules=['simple_plugin'],
        entry_points="""
        [segno.plugin.converter]
        simple = simple_plugin:write
        """,
        install_requires=['segno'],
    )

Once installed, it's possible to call this plugin via:

.. code-block:: python

    >>> import segno
    >>> qrcode = segno.make('Chelsea Hotel No. 2')
    >>> qrcode.to_simple()
    XXXXXXX_XXXX_XX_X_XXXXXXX
    X_____X___________X_____X
    X_XXX_X_XX__XXX___X_XXX_X
    X_XXX_X__X_XXX_X__X_XXX_X
    X_XXX_X__XX_XX__X_X_XXX_X
    X_____X_X__XXX__X_X_____X
    XXXXXXX_X_X_X_X_X_XXXXXXX
    __________X_X__XX________
    X_X___XX__XXXXX_X__X__X_X
    _XX__X_XXXXXX__XX_XX_X__X
    _X____X____X_XXXX__XX_X_X
    _XX__X_XX_XXX__XXXX_XX___
    __X_XXXX_XXX_XX_X_XXXX_X_
    _____X_X_X___X__XXXX_XX_X
    XXXXX_X_X_XX___XX_XXXXX_X
    ____XX__XXX__X_______X_XX
    XX_X__X__XXXXX_XXXXXX__XX
    ________X_X_X___X___X____
    XXXXXXX_X___XXX_X_X_X___X
    X_____X__X_XX_X_X___XX_XX
    X_XXX_X___X__XXXXXXXXX_XX
    X_XXX_X______XX__X__XX_X_
    X_XXX_X_XXXX_____X_XX_XXX
    X_____X___X__X__XX_X_X___
    XXXXXXX_XXXXXX__X_XXXX__X


