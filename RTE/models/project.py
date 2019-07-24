import git
import os
import re
import glob
import json
from .labels import Label

class Project:
    def __init__(self, path):
        self.path = path
        #self.repo = git.Repo(path=path)
        if os.path.exists(os.path.join(path, ".rte-notes")):
            with open(os.path.join(path, ".rte-notes")) as f:
                self.notes = f.read()
        else:
            self.notes = ""

        self.labels = self.get_all_labels()
        pass

    def save_notes(self):
        with open(os.path.join(self.path, ".rte-notes"), "w") as f:
            f.write(self.notes)

    def get_all_labels(self):
        label_re = re.compile(r'(label) (\S+) ?:')
        labels = []
        for filename in self.get_all_files("rpy"):
            path = os.path.join(self.path, filename)
            with open(path, "r") as f:
                for i, line in enumerate(f):
                    match = label_re.match(line)
                    if match:
                        labels.append(Label(match.group(2), i, path))
        return labels

    def get_all_files(self, ext="rpy"):
        rv = []
        for filename in glob.iglob(os.path.join(self.path, f'**/*.{ext}'), recursive=True):
            rv.append(filename)
        return rv

    def save_project_metadata(self):
        d = {}
        d["labels"] = self.labels
        with open(os.path.join(self.path, ".rte-project"), "w") as f:
            json.dump(d, f)

    def load_project_metadata(self):
        f = open(os.path.join(self.path, ".rte-project"))
        d = self.labels = json.load(f)
        self.labels = d["labels"]
