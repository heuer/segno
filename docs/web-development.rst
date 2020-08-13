Web development
===============

A few proposals how to integrate Segno with popular Python web application
frameworks.


Flask
-----

There are various ways to output QR codes in Jinja templates in conjunction
with Flask. See also the Flask example in the repository:
https://github.com/heuer/segno/tree/develop/examples/flask_qrcode


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
        qr = segno.make('The Continuing Story of Bungalow Bill')
        return render_template('example.html', qr=qr)



.. code-block:: jinja

    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>QR Codes</title>
      </head>
      <body>
        <img src="{{ qr.png_data_uri(dark='darkblue', data_dark='steelblue', alignment_dark='darkgreen', scale=3) }}"><br>
        <img src="{{ qr.svg_data_uri(dark='darkblue', scale=4) }}">
      </body>
    </html>


Embed SVG QR codes into HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since HTML5 supports SVG directly, it's also possible to embed the
generated SVG directly into a template.

Create the QR code and the SVG within the Flask view and use the ``|safe`` filter
in the Jinja template or wrap the result into a ``markupsafe.Markup`` object.

.. code-block:: python

    def make_qr_svg(content):
        buff = io.ByteIO()
        qr = segno.make(content)
        # Omit the XML declaration and the SVG namespace declaration
        # and the trailing newline.
        qr.save(buff, kind='svg', xmldecl=False, svgns=False, nl=False, scale=3)
        # Alternative:
        # return markupsafe.Markup(buff.getvalue().decode('utf-8'))
        return buff.getvalue().decode('utf-8')

    @app.route('/')
    def home():
        qr_svg = make_qr_svg('While My Guitar Gently Weeps')
        return render_template('example.html', qr_svg=qr_svg)

.. code-block:: jinja

    <div>
      {{ qr_svg | safe }}
    </div>


Create a view
~~~~~~~~~~~~~

Another possibility is to create the QR codes dynamically in a Flask view and
then to deliver them with ``send_file``.

Note that anyone can call up the route and create QR codes of any content.

.. code-block:: python

    @app.route('/qr-png/')
    def qrcode_png():
        buff = io.BytesIO()
        segno.make(request.args.get('data', ''), micro=False) \
             .save(buff, kind='png', scale=4, dark='darkblue',
                   data_dark='#474747', light='#efefef')
        buff.seek(0)
        return send_file(buff, mimetype='image/png')


.. code-block:: jinja

    <img src="{{ url_for('qrcode_png', data='Rocky Raccoon') }}">
