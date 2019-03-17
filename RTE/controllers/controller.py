import os
from RTE.models.theme import Theme
from RTE.models.file import File
import RTE.constants as const


from RTE.views.image_viewer import ImageViewer
from RTE.views.sound_viewer import SoundViewer
from .menus import MenusController
import tkinter as tk
import sys
from difflib import Differ


class ThemeController():
    def __init__(self):
        self.model = Theme()


class Controller():
    def __init__(self, view):
        self.menus = MenusController(self)
        self.project = None
        self.view = view
        self.last_entered_side = "left"
        self.differ = Differ()
        self.marked_as_diff = None
        return

    @property
    def get_all_themes(self):
        return [f.split(".")[0]
                for root, dirs, files in os.walk(const.theme_folder_path)
                for f in files
                if f.endswith("json") and not f.startswith("default")]

    def open_file(self, path, ftype):
        if ftype == "text":
            file_ = File(path, self.last_entered_side, project=self.project)
            self.view.main.add_tab(file_)
        elif ftype == "image":
            root = tk.Toplevel()
            root.title("View image : " + path.split('/')[-1])
            img_viewer = ImageViewer(root, path)
            img_viewer.grid()
            root.mainloop()
        elif ftype == "music" and sys.platform == "win32":
            root = tk.Toplevel()
            root.title("Sound playing : " + path.split('/')[-1])
            root.geometry("300x70")
            root.resizable(False, False)
            sfx_view = SoundViewer(root, path)
            sfx_view.grid()
            root.mainloop()

    def mark_as_first_diff(self, *args):
        self.marked_as_diff = self.current_file
        return

    def diff(self, *args):
        if self.marked_as_diff is not None:
            file2 = self.current_file
            self._diff(self.marked_as_diff, file2)
            self.marked_as_diff = None
        return

    def _diff(self, file1, file2):
        diff = self.differ.compare(file1.text.splitlines(True), file2.text.splitlines(True))
        fpath = os.path.join(self.project.path, f"{file1.name}-{file2.name}.diff")
        file_ = File(fpath, self.last_entered_side, diff)
        self.view.main.add_tab(file_)

    def set_last_entered_side(self, side):
        self.last_entered_side = side

    @property
    def current_text(self):
        return self.view.get_current_text(self.last_entered_side).text

    @property
    def current_file(self):
        return self.view.get_current_text(self.last_entered_side).file

    @property
    def all_open_files(self):
        rv = []
        rv.extend([x.file for x in self.view.main.left_tabs])
        rv.extend([x.file for x in self.view.main.right_tabs])
        return rv
