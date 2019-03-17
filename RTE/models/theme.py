import os
import RTE.constants as const
import json
import tkinter.font as tkfont

class Token:
    def __init__(self, name, attributes, font):
        self.name = name
        self.attributes = attributes
        self.font = font

    def set_font(self):
        convert = {"normal": tkfont.NORMAL,
                   "italic": tkfont.ITALIC,
                   "bold": tkfont.BOLD,
                   "roman": tkfont.ROMAN}
        if "font" in self.attributes.keys() and not isinstance(self.attributes["font"], tkfont.Font):
            fontstyle = self.attributes["font"]
            for k, v in fontstyle.items():
                if v.lower() in convert:
                    fontstyle[k] = convert[v.lower()]
            if "family" not in fontstyle.keys():
                fontstyle["family"] = self.font["family"]
            if "size" not in fontstyle.keys():
                fontstyle["size"] = self.font["size"]
            self.attributes["font"] = tkfont.Font(**fontstyle)


class Theme:
    def __init__(self, theme_name):
        self.name = theme_name
        self.path = os.path.join(const.theme_folder_path, self.name + ".json")
        with open(self.path) as conf:
            data = json.load(conf)
        font = data["default-font"]
        self._tokens = [Token(k, v, font) for k, v in data["tokens"].items()]
        self.ui = data["ui"]
        self.bitmapimage = data["bitmapimage"]
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
