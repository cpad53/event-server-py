#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import Response

import json
import os

app = Flask(__name__)


class FileStore:
    """Manages the backend store for event messages."""

    def __init__(self, fname):
        self._file = fname

    def store_event(self, event):
        """Store the received event in the store"""
        with open(self._file, 'a') as f:
            f.write("{}\n".format(event))

    def get_last_event(self):
        """Return the last stored event"""
        with open(self._file) as f:
            l = f.readlines()
        if len(l):
            return l[-1]


def handle_errors(func):
    """A decorator which handles failures in the HTTP controllers.
    This decorator ensures that a JSON response with status code 500
    is sent back in case of any error."""
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
    """
    POST /event
    Stores the received payload as is
    """
    e = request.data.decode('utf-8')
    fs.store_event(e)
    return Response(status=200)


@handle_errors
@app.route("/lastEvent")
def last_event():
    """
    GET /lastEvent
    {
        "ts": "<timestamp>",
        "msg": "<event message>"
    }
    Stores the entire payload as a event as-is. Does not validate inputs.
    Timestamp is an integer in string format: Milliseconds since unix epoch
    """
    last_eve = fs.get_last_event()
    return Response(last_eve, status=200, mimetype='application/json')


if __name__ == "__main__":
    
    # store events inside 'events/events.log' from the current working directory
    # can be made configurable in the future

    cur_path = os.getcwd()
    events_store_path = os.path.join(cur_path, "events")
    if not os.path.exists(events_store_path):
        os.makedirs(events_store_path)

    events_store_file = os.path.join(events_store_path, "events.log")

    fs = FileStore(events_store_file)
    app.run()
