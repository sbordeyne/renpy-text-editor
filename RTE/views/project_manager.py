import tkinter as tk
import tkinter.ttk as ttk
import os
from RTE.assets import AssetStore

class ProjectManagerView(tk.Frame):
    def __init__(self, master=None, project_path=None):
        super(ProjectManagerView, self).__init__()
        self.project_path = project_path

    def init_treeview(self):
        self.treeview = ttk.Treeview(self,
                                     columns=("name", "path"),
                                     displaycolumns=(0),
                                     height=128,
                                     selectmode="browse",
                                     show=())
        i = 0
        for root, dirs, files in os.walk(self.project_path):
            i += 1
            j = 0
            for directory in dirs:
                j += 1
                item_options = {"iid": i * 10 + j,
                                "text": directory,
                                "image": AssetStore.get_icon_by_extension("folder"),
                                "values": (directory, os.path.join(root, directory)),
                                "open": True}
                self.treeview.insert("", "end", **item_options)
            for filename in files:
                item_options = {"iid": i * 10,
                                "text": filename,
                                "image": AssetStore.get_icon_by_extension(filename.split(".")[-1]),
                                "values": (filename, os.path.join(root, filename)),
                                "open": True}
                self.treeview.insert("", "end", **item_options)
        self.treeview.pack()
