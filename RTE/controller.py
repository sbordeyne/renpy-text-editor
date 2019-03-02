import os
from RTE.models.theme import Theme
from RTE.models.project import Project
import tkinter.filedialog as filedialog
import RTE.constants as const

from RTE.views.layeredimage_builder import LayeredImageBuilderGUI
import tkinter as tk


class MenusController():
    def __init__(self, master):
        self.master = master

        self.layeredimage_builder_wm = None
        return

    def file_new(self):
        path = filedialog.askdirectory()
        self.master.project = Project(path)
        self.master.view.project_manager.project_path = path
        self.master.view.project_manager.populate_roots()
        return

    def file_open(self):
        path = filedialog.askdirectory()
        self.master.project = Project(path)
        self.master.view.project_manager.project_path = path
        self.master.view.project_manager.populate_roots()
        return

    def file_save(self):
        return

    def file_save_as(self):
        return

    def tools_open_layeredimage_builder(self):
        if self.layeredimage_builder_wm is None:
            self.layeredimage_builder_wm = tk.Toplevel()
            gui = LayeredImageBuilderGUI(self.layeredimage_builder_wm)
            gui.pack()
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
        return


class ThemeController():
    def __init__(self):
        self.model = Theme()


class Controller():
    def __init__(self, view):
        self.menus = MenusController(self)
        self.project = None
        self.view = view
        self.last_entered_side = "left"
        return

    @property
    def get_all_themes(self):
        return [f.split(".")[0]
                for root, dirs, files in os.walk(const.theme_folder_path)
                for f in files
                if f.endswith("json") and not f.startswith("default")]

    def open_file(self, path, ftype):
        if ftype == "text":
            self.view.main.add_tab(self.last_entered_side, path, path.split('/')[-1])

    def set_last_entered_side(self, side):
        self.last_entered_side = side
