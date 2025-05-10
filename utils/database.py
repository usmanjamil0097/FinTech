import json
import os

class Database:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key, [])

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def append(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)
        self.save()
