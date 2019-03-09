import os
from RTE.models.theme import Theme
from RTE.models.project import Project
from RTE.models.file import File
import tkinter.filedialog as filedialog
import RTE.constants as const

from RTE.views.layeredimage_builder import LayeredImageBuilderGUI
from RTE.views.options import OptionsView
from RTE.views.image_viewer import ImageViewer
from RTE.views.sound_viewer import SoundViewer
from RTE.utils import text_get_selected
import tkinter as tk
import string
import random
import sys
from difflib import Differ


class MenusController():
    def __init__(self, master):
        self.master = master

        self.layeredimage_builder_wm = None
        self.options_wm = None
        return

    def file_new(self):
        file_ = File("", self.master.last_entered_side, is_new=True)
        self.master.view.main.add_tab(file_)
        return

    def file_open(self):
        path = filedialog.askdirectory()
        self.master.project = Project(path)
        self.master.view.project_manager.project_path = path
        self.master.view.project_manager.populate_roots()
        return

    def file_save(self, file_=None):
        if file_ is None:
            file_ = self.master.current_file
        if file_.is_new:
            self.file_save_as(file_)
        else:
            file_.save()
        return

    def file_save_as(self, file_=None):
        if file_ is None:
            file_ = self.master.current_file
        initialdir = None
        if self.master.project is None:
            initialdir = os.getcwd()
        else:
            initialdir = self.master.project.path
        filename = filedialog.asksaveasfilename(initialdir=initialdir,
                                                title="Select file",
                                                filetypes=(("RenPy Scripts", "*.rpy"),
                                                           ("JSON files", "*.json"),
                                                           ("YAML files", "*.yml"),
                                                           ("XML files", "*.xml"),
                                                           ("Diff files", "*.diff"),
                                                           ("Text files", "*.txt"),
                                                           ("All files", "*.*")))
        file_.path = os.path.join(self.master.project.path, filename)
        file_.save()
        return

    def file_save_all(self):
        for f in self.master.all_open_files:
            self.file_save(file_=f)
        return

    def tools_open_layeredimage_builder(self):
        if self.layeredimage_builder_wm is None:
            self.layeredimage_builder_wm = tk.Toplevel()
            gui = LayeredImageBuilderGUI(self.layeredimage_builder_wm)
            gui.grid()
            self.layeredimage_builder_wm.protocol("WM_DELETE_WINDOW", self.on_layeredimage_builder_quit)
            self.layeredimage_builder_wm.mainloop()

    def on_layeredimage_builder_quit(self):
        self.layeredimage_builder_wm.destroy()
        self.layeredimage_builder_wm = None

    def tools_open_variable_viewer(self):
        return

    def tools_open_screen_builder(self):
        return

    def tools_open_options(self):
        if self.options_wm is None:
            self.options_wm = tk.Toplevel()
            gui = OptionsView(master=self.options_wm, controller=self)
            gui.grid()
            self.options_wm.protocol("WM_DELETE_WINDOW", gui.quit)
            self.options_wm.mainloop()

        return

    def edit_undo(self):
        text = self.master.current_text
        text.text.edit_undo()

    def edit_redo(self):
        text = self.master.current_text
        text.text.edit_redo()

    def edit_duplicate(self):
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, f"\n{selection}")
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", f"\n{selection}")
        pass  # TODO

    def edit_formatting_upper(self):
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, selection.upper())
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", selection.upper())
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        pass

    def edit_formatting_lower(self):
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, selection.lower())
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", selection.lower())
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        pass

    def edit_formatting_capitalized(self):
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, selection.capitalize())
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", selection.capitalize())
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        pass

    def edit_formatting_invert(self):
        def invert(s):
            rv = ""
            for char in s:
                if char in string.ascii_lowercase:
                    rv += char.upper()
                elif char in string.ascii_uppercase:
                    rv += char.lower()
                else:
                    rv += char
            return rv
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, invert(selection))
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", invert(selection))
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        pass

    def edit_formatting_random(self):
        def rand(s):
            rv = ""
            for char in s:
                rv += [char.upper(), char.lower()][random.randint(0, 1)]
            return rv
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, rand(selection))
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", rand(selection))
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def edit_formatting_spongebob(self):
        def sponge(s):
            rv = ""
            i = 0
            for char in s:
                if char == " ":
                    rv += " "
                    continue
                rv += [char.upper(), char.lower()][i % 2]
                i += 1
            return rv
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, sponge(selection))
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", sponge(selection))
            text.delete(tk.SEL_FIRST, tk.SEL_LAST)

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
            file_ = File(path, self.last_entered_side)
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
        return self.current_text.file

    @property
    def all_open_files(self):
        rv = []
        rv.extend([x.file for x in self.view.main.left_tabs])
        rv.extend([x.file for x in self.view.main.right_tabs])
        return rv
