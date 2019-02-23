import tkinter as tk
import tkinter.ttk as ttk
import os
from RTE.assets import AssetStore
from RTE.config import config


class ProjectManagerView(tk.Frame):
    def __init__(self, master=None, project_path=None):
        super(ProjectManagerView, self).__init__()
        self.project_path = project_path
        self.init_treeview()

    def init_treeview(self):
        global config
        self.treeview = ttk.Treeview(self,
                                     columns=("name", "path"),
                                     displaycolumns=(0),
                                     height=config.wm_height//20,
                                     selectmode="browse",
                                     show=())
        self.treeview.pack()

    def build_tree(self, rootdir=None):
        if rootdir is None:
            rootdir = self.project_path
        for root, dirs, files in os.walk(rootdir):
            if dirs:
                for directory in dirs:
                    item_options = {"text": directory,
                                    "image": AssetStore.get_icon_by_extension("folder"),
                                    "values": (directory, os.path.join(root, directory)),
                                    "open": True}
                    self.treeview.insert("", "end", **item_options)
                    self.build_tree(os.path.join(root, directory))
            for filename in files:
                item_options = {"text": filename,
                                "image": AssetStore.get_icon_by_extension(filename.split(".")[-1]),
                                "values": (filename, os.path.join(root, filename)),
                                "open": True}
                self.treeview.insert("", "end", **item_options)
