#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import Response

import json
import os

from src.store import FileStore

app = Flask(__name__)

def handle_errors(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Response(
                "'error':'{}'".format(e),
                status=500,
                mimetype="application/json"
            )
    return inner


@handle_errors
@app.route("/event", methods=['POST'])
def store_event():
    e = request.data.decode('utf-8')
    fs.store_event(e)
    return Response(status=200)


@handle_errors
@app.route("/lastEvent")
def last_event():
    last_eve = fs.get_last_event()
    return Response(last_eve, status=200, mimetype='application/json')


if __name__ == "__main__":
    
    cur_path = os.getcwd()
    events_store_path = os.path.join(cur_path, "events")
    if not os.path.exists(events_store_path):
        os.makedirs(events_store_path)

    events_store_file = os.path.join(events_store_path, "events.log")

    fs = FileStore(events_store_file)
    app.run()
