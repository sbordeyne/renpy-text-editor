import tkinter as tk
import tkinter.filedialog as filedialog
import string
import random
import os

from RTE.views.snippets import SnippetsAddingView
from RTE.views.layeredimage_builder import LayeredImageBuilderGUI
from RTE.views.options import OptionsView

from RTE.models.project import Project
from RTE.models.file import File

from RTE.utils import text_get_selected


class MenusController():
    def __init__(self, master):
        self.master = master

        self.layeredimage_builder_wm = None
        self.options_wm = None
        self.add_snippet_wm = None
        return

    def file_new(self, *args):
        file_ = File("", self.master.last_entered_side, is_new=True)
        self.master.view.main.add_tab(file_)
        return

    def file_open(self, *args):
        path = filedialog.askdirectory()
        self.master.project = Project(path)
        self.master.view.project_manager.clear_tree()
        self.master.view.project_manager.project_path = path
        self.master.view.project_manager.populate_roots()
        return

    def file_save(self, *args, file_=None):
        if file_ is None:
            file_ = self.master.current_file
        if file_.is_new:
            self.file_save_as(file_)
        else:
            file_.save()
        return

    def file_save_as(self, *args, file_=None):
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
        if filename:
            file_.path = os.path.join(self.master.project.path, filename)
            file_.save()
        return

    def file_save_all(self, *args):
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

    def tools_open_add_snippet(self):
        if self.add_snippet_wm is None:
            self.add_snippet_wm = tk.Toplevel()
            gui = SnippetsAddingView(master=self.add_snippet_wm, controller=self)
            gui.grid()
            self.add_snippet_wm.mainloop()

    def tools_open_options(self):
        if self.options_wm is None:
            self.options_wm = tk.Toplevel()
            self.options_wm.geometry("640x480")
            self.options_wm.title("Options")
            gui = OptionsView(master=self.options_wm, controller=self)
            gui.grid()
            self.options_wm.protocol("WM_DELETE_WINDOW", gui.quit)
            self.options_wm.mainloop()

        return

    def edit_undo(self, *args):
        text = self.master.current_text
        text.text.edit_undo()

    def edit_redo(self, *args):
        text = self.master.current_text
        text.text.edit_redo()

    def edit_comment(self, *args):
        text = self.master.current_text
        file = self.master.current_file
        selection = text_get_selected(text)
        if selection:
            file.insert_comment(text.index(tk.SEL_FIRST), text.index(tk.SEL_LAST))
        else:
            file.insert_comment(text.index("current linestart"), text.index("current lineend"))

    def edit_duplicate(self, *args):
        text = self.master.current_text
        selection = text_get_selected(text)
        if selection:
            text.insert(tk.SEL_LAST, f"\n{selection}")
        else:
            selection = text.get(tk.CURRENT + " linestart",
                                 tk.CURRENT + " lineend")
            text.insert(tk.CURRENT + " lineend", f"\n{selection}")
        pass  # TODO

    def edit_formatting_upper(self, *args):
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

    def edit_formatting_lower(self, *args):
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

    def edit_formatting_capitalized(self, *args):
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

    def edit_formatting_invert(self, *args):
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

    def edit_formatting_random(self, *args):
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

    def edit_formatting_spongebob(self, *args):
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
