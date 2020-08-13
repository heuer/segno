# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Example Flask app to show different possibilities to embed Segno.
"""
import io
from flask import Flask, render_template, request, send_file
import segno

app = Flask(__name__)


def make_svg_qrcode(content):
    buff = io.BytesIO()
    # See <https://segno.readthedocs.io/en/stable/svg-options.html>
    # for SVG options
    segno.make(content).save(buff, kind='svg', xmldecl=False, nl=False, svgns=False,
                             dark='darkred', data_dark='#cb410b', scale=4)
    return buff.getvalue().decode('utf-8')


@app.route('/')
def home():
    qr = segno.make('The Continuing Story of Bungalow Bill')
    qr_svg = make_svg_qrcode('While My Guitar Gently Weeps')
    return render_template('example.html', qr=qr, qr_svg=qr_svg)


@app.route('/qr-svg/')
def qrcode_svg():
    buff = io.BytesIO()
    segno.make(request.args.get('data'), micro=False).save(buff, kind='svg', scale=4)
    buff.seek(0)
    return send_file(buff, mimetype='image/svg+xml')


@app.route('/qr-png/')
def qrcode_png():
    buff = io.BytesIO()
    segno.make(request.args.get('data'), micro=False) \
        .save(buff, kind='png', scale=4, dark='darkblue', data_dark='#474747',
              light='#efefef')
    buff.seek(0)
    return send_file(buff, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, port=5673)
