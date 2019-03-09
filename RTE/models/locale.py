import json
import RTE.constants as const
import os


class Translator:
    locale = "en-US"

    @classmethod
    def validate_locale(cls, locale):
        if locale in os.listdir(const.locale_folder_path):
            return locale
        else:
            return cls.locale

    def __init__(self, locale):
        self.locale = locale
        with open(os.path.join(const.locale_folder_path, f"{locale}.json")) as f:
            self._attrs = json.load(f)

    def translate(self, text):
        try:
            return self._attrs[text].encode("utf8")
        except KeyError:
            return text
