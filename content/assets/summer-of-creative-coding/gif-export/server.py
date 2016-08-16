#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division

import base64
from os.path import dirname, join, realpath

from flask import Flask, request
from flask.ext.cors import CORS


CURRENT_DIR = dirname(realpath(__file__))
IMAGES_DIR = join(CURRENT_DIR, 'images')
IMAGE_INDEX = 0

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    global IMAGE_INDEX

    png_data = request.form['imageData'].split(',')[-1]
    decoded = base64.b64decode(png_data)
    path = join(IMAGES_DIR, '%04d.png' % IMAGE_INDEX)

    with open(path, 'w+') as f:
        f.write(decoded)

    IMAGE_INDEX += 1

    return ''


if __name__ == '__main__':
    app.run(debug=True)
