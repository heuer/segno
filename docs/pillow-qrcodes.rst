Pillow
======

In order to process the output of Segno with Pillow you may use the
:doc:`artistic-qrcodes <artistic-qrcodes>` plugin or use the result
of Segno's capability to generate PNG images directly.

All PNG images can be opened by the Pillow library:

.. code-block:: python

    >>> import io
    >>> from PIL import Image
    >>> import segno
    >>> # Create a 5-H QR code
    >>> qrcode = segno.make('Blackbird singing in the dead of night', error='h')
    >>> # Save the QR code into a memory buffer as PNG
    >>> out = io.BytesIO()
    >>> qrcode.save(out, scale=5, kind='png')
    >>> out.seek(0)  # Important to let PIL / Pillow load the image
    >>> img = Image.open(out)  # Done, do what ever you want with the PIL/Pillow image


Convert QR code to RGB(A)
-------------------------

Since Segno tries to return a minimal PNG representation it may be necessary to convert the Pillow
image into a RGB or RGBA image:

.. code-block:: python

    >>> img = Image.open(out).convert('RGB')  # We want to use Pillow with colors
    >>> # Only necessary if further processing requires transparency / an alpha channel
    >>> img = Image.open(out).convert('RGBA')


Add a logo to a QR code
-----------------------

A common request to add a logo or any kind of other picture to the QR code is beyond the purpose of
this library since it requires 3rd party libraries.
The following code provides an example how to use Pillow to add a logo to the center
of a QR code.

.. code-block:: python

    import io
    from PIL import Image
    import segno

    out = io.BytesIO()
    # Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
    segno.make('Blackbird singing in the dead of night', error='h').save(out, scale=5, kind='png')
    out.seek(0)  # Important to let Pillow load the PNG
    img = Image.open(out)
    img = img.convert('RGB')  # Ensure colors for the output
    img_width, img_height = img.size
    logo_max_size = img_height // 3  # May use a fixed value as well
    logo_img = Image.open('./blackbird.jpg')  # The logo
    # Resize the logo to logo_max_size
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    # Calculate the center of the QR code
    box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
    img.paste(logo_img, box)
    img.save('qrcode_with_logo.png')


