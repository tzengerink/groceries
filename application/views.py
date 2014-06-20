# -*- coding: utf-8 -*-
"""
    APPLICATION.VIEWS
    -----------------
    Views to handle the several requests.

    Copyright (c) 2014 Teun Zengerink
    Licensed under MIT License.
    See: https://raw.github.com/Mytho/groceries/master/LISENCE.md
"""
import os
import json
from flask import (abort, current_app, make_response, render_template, request,
                   send_from_directory)
from flask.views import MethodView
from flask.ext.login import login_required
from .auth import logged_in_or_redirect
from .models import Item
from .decorators import cache_control, content_type


class ApiView(MethodView):

    decorators = [content_type('application/json'), login_required]


class FaviconView(MethodView):

    decorators = [content_type('image/vnd.microsoft.icon')]

    def get(self):
        path = os.path.join(current_app.root_path, 'static')
        file = send_from_directory(path, 'icons/shopping-cart-32x32.png')
        return make_response(file)


class GroceriesView(MethodView):

    decorators = [cache_control(86400), logged_in_or_redirect]

    def get(self):
        return make_response(render_template('groceries.html'))


class ItemView(ApiView):

    def delete(self, item_id):
        Item.delete(item_id)
        return make_response('')

    def get(self):
        items = Item.query.filter_by(bought_by=None)
        return make_response(json.dumps([item.serialize() for item in items]))

    def post(self):
        if not request.data:
            abort(400)
        data = json.loads(request.data)
        item = Item.create(data['name'])
        return make_response(json.dumps(item.serialize()))

    def put(self, item_id):
        if not request.data:
            abort(400)
        data = json.loads(request.data)
        item = Item.bought(item_id, data['bought'])
        if not item:
            abort(404)
        return make_response(json.dumps(item.serialize()))


class SuggestionView(ApiView):

    def get(self):
        suggestions = [dict([['name', k], ['count', v]])
                       for (k, v) in Item.suggestions()]
        return make_response(json.dumps(suggestions))
