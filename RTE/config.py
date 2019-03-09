import RTE.constants as const
import json
from collections import defaultdict
from RTE.models.theme import Theme
from RTE.models.locale import Translator


class Config:
    def __init__(self):
        with open(const.config_file_path) as conf:
            data = json.load(conf)
        self._attrs = defaultdict()
        for k, v in data.items():
            self._attrs[k] = v

    def __getattr__(self, attr):
        return self._attrs[attr]

    def __setattr__(self, attr, value):
        if attr == '_attrs':
            return super(Config, self).__setattr__(attr, value)
        self._attrs[attr] = value

    @property
    def geometry(self):
        return f"{self.wm_width}x{self.wm_height}"

    def get_theme(self):
        return Theme(self.theme_name)

    def set_theme(self, theme_name):
        self.theme_name = theme_name

    def get_locale(self):
        return Translator(self.locale)

    def set_locale(self, locale):
        self.locale = Translator.validate_locale(locale)

    def save(self):
        to_save = dict(self._attrs)
        with open(const.config_file_path, "w") as conf:
            json.dump(to_save, conf, indent=4)

    def validate_width_height(self, root):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.wm_width = min(self.wm_width, screen_width)
        self.wm_height = min(self.wm_height, screen_height)


class Keybindings:
    def __init__(self):
        with open(const.keybindings_file_path) as conf:
            data = json.load(conf)
        self._attrs = defaultdict()
        for k, v in data.items():
            self._attrs[k] = v

    def __getattr__(self, attr):
        return self._attrs[attr]

    def __setattr__(self, attr, value):
        if attr == '_attrs':
            return super(Keybindings, self).__setattr__(attr, value)
        self._attrs[attr] = self.format(value)

    def format(self, value):
        v = value.strip('<>')
        return f"<{v}>"


config = Config()
keybindings = Keybindings()
