# -*- coding: utf-8 -*-
"""
    APPLICATION.VIEWS
    -----------------
    Controls the routes and serves templates to the user.

    Copyright (c) 2013 T. Zengerink
    Licensed under MIT License.
    See: https://raw.github.com/Mytho/groceries/master/LISENCE.md
"""
from application import app
from auth import logged_in_or_redirect
from decorators import cache_control, content_type
from flask import make_response, render_template, request, send_from_directory
from flask.ext.login import login_required
from json import dumps, loads
from models import Item
from os import path


@app.route('/favicon.ico', methods=['GET'])
@content_type('image/vnd.microsoft.icon')
def favicon():
    static_path = path.join(app.root_path, 'static')
    return make_response(send_from_directory(static_path,
                                             'icons/shopping-cart-32x32.png'))


@app.route('/')
@logged_in_or_redirect
@cache_control()
def home():
    return make_response(render_template('home.html'))


@app.route('/items', methods=['GET'])
@login_required
@content_type('application/json')
def get_items():
    items = Item.query.filter_by(bought_by=None)
    return make_response(dumps([item.serialize() for item in items]))


@app.route('/items', methods=['POST'])
@login_required
@content_type('application/json')
def post_items():
    data = loads(request.data)
    item = Item.create(data['name'])
    return make_response(dumps(item.serialize()))


@app.route('/items/<item_id>', methods=['PUT'])
@login_required
@content_type('application/json')
def put_items(item_id):
    data = loads(request.data)
    Item.bought(item_id, data['bought'])
    return make_response(dumps(''))


@app.route('/items/<item_id>', methods=['DELETE'])
@login_required
@content_type('application/json')
def delete_items(item_id):
    Item.delete(item_id)
    return make_response('')


@app.route('/suggestions', methods=['GET'])
@login_required
@content_type('application/json')
def get_suggests():
    suggestions = [dict([['name', k], ['count', v]])
                   for (k, v) in Item.suggestions()]
    return make_response(dumps(suggestions))
