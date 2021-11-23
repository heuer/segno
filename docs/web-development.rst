Web development
===============

A few proposals how to use Segno with popular Python web application
frameworks.


Flask
-----

There are various ways to output QR codes in Jinja templates in conjunction
with Flask. See also the Flask example in the repository:
https://github.com/heuer/segno/tree/master/examples/flask_qrcode


Data URIs
~~~~~~~~~

Create a QR code in the Flask view and use the :py:func:`segno.QRCode.svg_data_uri()`
or :py:func:`segno.QRCode.png_data_uri()` methods in the template.

.. code-block:: python

    from flask import Flask, render_template
    import segno

    app = Flask(__name__)

    @app.route('/)
    def home():
        qrcode = segno.make('The Continuing Story of Bungalow Bill')
        return render_template('example.html', qrcode=qrcode)



.. code-block:: jinja

    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>QR Codes</title>
      </head>
      <body>
        <img src="{{ qrcode.png_data_uri(dark='darkblue', data_dark='steelblue', alignment_dark='darkgreen', scale=3) }}"><br>
        <img src="{{ qrcode.svg_data_uri(dark='darkblue', scale=4) }}">
      </body>
    </html>


Embed SVG QR codes into HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since HTML5 supports SVG directly, it's also possible to embed the
generated SVG directly into a template.

Create the QR code within the Flask view and use the
:py:func:`segno.QRCode.svg_inline()` method in conjunction with the Jinja
``|safe`` filter.

.. code-block:: python

    @app.route('/')
    def home():
        qrcode = segno.make('While My Guitar Gently Weeps')
        return render_template('example.html', qrcode=qrcode)

.. code-block:: jinja

    <div>
      {{ qrcode.svg_inline(scale=3) | safe }}
    </div>


Create a view
~~~~~~~~~~~~~

Another possibility is to create the QR codes dynamically in a Flask view and
deliver them with ``send_file``.

.. code-block:: python

    BEATLES_SONGS = {'Yellow Submarine', 'Let It Be', 'Rocky Raccoon'}

    @app.route('/qr-png/')
    def qrcode_png():
        data = request.args.get('data')
        # Check if the data is acceptable otherwise a 404 error is generated
        if data not in BEATLES_SONGS:
            return abort(404)
        buff = io.BytesIO()
        segno.make(data, micro=False) \
             .save(buff, kind='png', scale=4, dark='darkblue',
                   data_dark='#474747', light='#efefef')
        buff.seek(0)
        return send_file(buff, mimetype='image/png')


.. code-block:: jinja

    <img src="{{ url_for('qrcode_png', data='Rocky Raccoon') }}">


Django
------

The project `django-segno-qr <https://pypi.org/project/django-segno-qr/>`_
provides a template tag for creating SVG QR codes in Django templates while
`django-qr-code <https://pypi.org/project/django-qr-code/>`_ provides more
template tags and utility functions.

Apart from that, the aforementioned information for Flask should also be
adaptable to Django, so here is just a hint on how to save QR codes in a
Django ``ImageField``.

The complete code is in the repository:
https://github.com/heuer/segno/tree/master/examples/django_qrcode


Saving a QR code to an ImageField
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming this simple model.

.. code-block:: python

    from django.db import models


    class Ticket(models.Model):
        name = models.CharField(max_length=150, unique=True)
        qrcode = models.ImageField(upload_to='ticket-qrcodes/')

Create a QR code with Segno and save it as PNG into a :py:class:`io.BytesIO`
instance.

.. code-block:: python

    import io
    import segno

    qrcode = segno.make('JULIA')
    # Save the QR code with transparent background and use dark blue for
    # the dark modules
    out = io.BytesIO()
    qrcode.save(out, kind='png', dark='#00008b', light=None, scale=3)

Now you can use the content of the buffer as input for a Django ``ContentFile``.

.. code-block:: python

    ticket = Ticket(name='JULIA')
    ticket.qrcode.save('JULIA.png', ContentFile(out.getvalue()), save=False)
    ticket.save()

If for some reason the QR codes should be stored in the lossy file format JPEG,
the ``qrcode-artistic`` plugin is required (see also :doc:`artistic-qrcodes`)::

    $ pip install qrcode-artistic


.. code-block:: python

    import io
    import segno

    qrcode = segno.make('JULIA')
    # img is a Pillow Image instance
    img = qrcode.to_pil(dark='#00008b', scale=3)
    # Now use Pillow Image.save() to save the QR code
    out = io.BytesIO()
    img.save(out, format='jpg')

    # ...

    ticket.qrcode.save('JULIA.jpg', ContentFile(out.getvalue()), save=False)

