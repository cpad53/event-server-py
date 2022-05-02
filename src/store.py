import json

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
