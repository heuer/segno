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
from flask import Flask, render_template, request, send_file, abort
import segno

app = Flask(__name__)

@app.route('/')
def home():
    qr = segno.make('The Continuing Story of Bungalow Bill')
    return render_template('example.html', qr=qr)


@app.route('/qr-svg/')
def qrcode_svg():
    data = request.args.get('data')
    if data not in ('Savoy Truffle', 'Rocky Raccoon'):
        return abort(404)
    buff = io.BytesIO()
    segno.make(data, micro=False).save(buff, kind='svg', scale=4)
    buff.seek(0)
    return send_file(buff, mimetype='image/svg+xml')


@app.route('/qr-png/')
def qrcode_png():
    data = request.args.get('data')
    if data not in ('Savoy Truffle', 'Rocky Raccoon'):
        return abort(404)
    buff = io.BytesIO()
    segno.make(data, micro=False) \
        .save(buff, kind='png', scale=4, dark='darkblue', data_dark='#474747',
              light='#efefef')
    buff.seek(0)
    return send_file(buff, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, port=5673)
