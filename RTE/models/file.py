import os
from RTE.syntaxhighlight.lexer import RenpyLexer, NullLexer
from pygments.lexers.diff import DiffLexer
from pygments.lexers.data import JsonLexer, YamlLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.html import XmlLexer
from RTE.config import config

class File:
    def __init__(self, fpath, window_side="left", text="", is_new=False):
        self.window_side = window_side
        if not is_new:
            self.path = fpath
            self.fullname = os.path.split(fpath)[-1]
            self.extension = self.fullname.split(".")[-1].lower()
            self.name = self.fullname.split(".")[0]
        else:
            self.path = None
            self.fullname = "New File"
            self.extension = ""
            self.name = "New File"
        self.text = text

    @property
    def lexer(self):
        def strip(lex):
            return [x[2:] for x in lex.filenames]

        if self.extension in strip(RenpyLexer):
            return RenpyLexer()
        elif self.extension in strip(DiffLexer):
            return DiffLexer()
        elif self.extension in strip(JsonLexer):
            return JsonLexer()
        elif self.extension in strip(YamlLexer):
            return YamlLexer()
        elif self.extension in strip(MarkdownLexer):
            return MarkdownLexer()
        elif self.extension in strip(XmlLexer):
            return XmlLexer()
        else:
            return NullLexer()

    def save(self):
        text = self.text.replace("\t", " " * config.tabs_length)
        with open(self.path, "w") as f:
            f.write(text)

    def update_text(self, text):
        self.text = text
