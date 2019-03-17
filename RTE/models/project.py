import git
import os

class Project:
    def __init__(self, path):
        self.path = path
        self.repo = git.Repo(path=path)
        if os.path.exists(os.path.join(path, ".rte-notes")):
            with open(os.path.join(path, ".rte-notes")) as f:
                self.notes = f.read()
        else:
            self.notes = ""
        pass

    def save_notes(self):
        with open(os.path.join(self.path, ".rte-notes"), "w") as f:
            f.write(self.notes)
