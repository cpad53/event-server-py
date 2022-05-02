import json

class FileStore:

    def __init__(self, fname):
        self._file = fname

    def store_event(self, event):
        with open(self._file, 'a') as f:
            f.write("{}\n".format(event))

    def get_last_event(self):
        with open(self._file) as f:
            l = f.readlines()
        if len(l):
            return l[-1]
