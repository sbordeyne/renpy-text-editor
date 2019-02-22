import RTE.constants as const
import json
from collections import defaultdict


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


config = Config()
