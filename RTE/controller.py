import os
from RTE.models.theme import Theme
from RTE.models.project import Project
import tkinter.filedialog as filedialog
import RTE.constants as const


class MenusController():
    def __init__(self, master):
        self.master = master
        return

    def file_new(self):
        path = filedialog.askdirectory()
        self.master.project = Project(path)
        self.master.view.project_manager.project_path = path
        self.master.view.project_manager.build_tree()
        return

    def file_open(self):
        path = filedialog.askdirectory()
        self.master.project = Project(path)
        self.master.view.project_manager.project_path = path
        self.master.view.project_manager.build_tree()
        return

    def file_save(self):
        return

    def file_save_as(self):
        return


class ThemeController():
    def __init__(self):
        self.model = Theme()


class Controller():
    def __init__(self, view):
        self.menus = MenusController(self)
        self.project = None
        self.view = view
        return

    @property
    def get_all_themes(self):
        return [f.split(".")[0]
                for root, dirs, files in os.walk(const.theme_folder_path)
                for f in files
                if f.endswith("json") and not f.startswith("default")]
