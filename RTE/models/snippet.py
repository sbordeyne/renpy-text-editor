import tkinter as tk
from RTE.utils import text_get_selected
import RTE.constants as const
import json
import os

class Snippet:
    def __init__(self, name="", replace_selection=False, before_cursor="", after_cursor=""):
        self.name = name
        self.replace_selection = replace_selection
        self.before_cursor = before_cursor
        self.after_cursor = after_cursor

    @property
    def json(self):
        return {"name": self.name,
                "replace_selection": self.replace_selection,
                "before_cursor": self.before_cursor,
                "after_cursor": self.after_cursor}

    def insert(self, text):
        sel = text_get_selected(text)
        if sel and self.replace_selection:
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        current = text.index(tk.CURRENT)
        line, column = current.split(".")
        rv = self.before_cursor + sel + self.after_cursor
        text.insert(tk.CURRENT, rv)
        if self.replace_selection:
            column = int(column)
        else:
            column = int(column) + len(self.before_cursor)
        text.mark_set("current", f"{line}.{column}")

class SnippetStore:
    def __init__(self):
        dicts = []
        data = {}
        final_dict = {}
        self.snippets = {}
        for dirpath, dirnames, filenames in os.walk(const.snippets_folder_path):
            for fname in filenames:
                path = os.path.join(dirpath, fname)
                with open(path, "r") as f:
                    if fname == "snippets.json":
                        final_dict = json.load(f)
                    else:
                        dicts.append(json.load(f))
        for d in dicts:
            data.update(d)
        data.update(final_dict)
        for k, v in data.items():
            self.snippets[k] = Snippet(**v)

    def add(self, sname, **kwargs):
        self.snippets[sname] = Snippet(**kwargs)

    def save(self):
        path = os.path.join(const.snippets_folder_path, "snippets.json")
        dmp = {}
        for k, v in self.snippets.items():
            dmp[k] = v.json
        with open(path, "w") as f:
            json.dump(dmp, f, indent=4)


snippet_store = SnippetStore()
