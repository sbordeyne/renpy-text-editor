import os
import RTE.constants as const
import json


class Token:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


class Theme:
    def __init__(self, theme_name):
        self.name = theme_name
        self.path = os.path.join(const.theme_folder_path, self.name + ".json")
        with open(self.path) as conf:
            data = json.load(conf)
        self._tokens = [Token(k, v) for k, v in data["tokens"].items()]
        self.ui_data = data["ui"]
        self.i = 0

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self._tokens):
            self.i += 1
            return self._tokens[self.i - 1]
        else:
            raise StopIteration
