import os
from RTE.syntaxhighlight.lexer import RenpyLexer, NullLexer
from pygments.lexers.diff import DiffLexer
from pygments.lexers.data import JsonLexer, YamlLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.html import XmlLexer
from RTE.config import config
from RTE.utils import tr, compare_path


class File:
    def __init__(self, fpath, window_side="left", text="", is_new=False, project=None):
        self.window_side = window_side
        self.is_new = is_new
        self._path = None
        if not is_new:
            self.path = fpath
        else:
            self.path = None
        self.text = text
        self.widget = None
        self.project = project

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
        text = "\n".join([line.rstrip() for line in text.split("\n")])
        if self.path.endswith("\\\\"):
            return
        with open(self.path, "w") as f:
            f.write(text)

    def update_text(self, text):
        self.text = text

    def __set_path(self, fpath):
        if fpath is not None:
            self._path = fpath
            self.fullname = os.path.split(fpath)[-1]
            self.extension = self.fullname.split(".")[-1].lower()
            self.name = self.fullname.split(".")[0]
        else:
            self._path = None
            self.fullname =tr("New File")
            self.extension = ""
            self.name = tr("New File")

    def __get_path(self):
        return self._path

    path = property(__get_path, __set_path)

    def get_comment_token(self):
        if self.extension in ("rpy", "yml", "yaml"):
            return ("#", "")
        elif self.extension == "xml":
            return ("<--", "-->")
        else:
            return ("", "")

    def insert_comment(self, start, end):
        token_start, token_end = self.get_comment_token()
        while int(start.split(".")[0]) <= int(end.split(".")[0]):
            line = self.widget.get(start + " linestart", start + " lineend")
            if line.lstrip().startswith(token_start):
                # remove comment token
                if token_start:
                    self.widget.delete(start + " linestart", start + f" linestart +{len(token_start)}c")
                if token_end:
                    self.widget.delete(start + f" lineend -{len(token_start)}c", start + " lineend")
            else:
                # insert comment token
                if token_start:
                    self.widget.insert(start + ' linestart', token_start)
                if token_end:
                    self.widget.insert(start + ' lineend', token_end)
            start = str(int(start.split(".")[0]) + 1) + ".0"
        pass

    def get_diff(self):
        if self.project is None:
            return
        hcommit = self.project.repo.head.commit
        diff = hcommit.diff()
        added = [d for d in diff.iter_change_type('A') if compare_path(d.a_rawpath, self.path)]
        deleted = [d for d in diff.iter_change_type('D') if compare_path(d.a_rawpath, self.path)]
        modified = [d for d in diff.iter_change_type('M') if compare_path(d.a_rawpath, self.path)]
        print("added ", added)
        print("deleted ", deleted)
        print("modified ", modified)
