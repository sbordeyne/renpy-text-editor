import tkinter as tk
import tkinter.ttk as ttk
import os

class ProjectManagerView(tk.Frame):
    def __init__(self, master=None, project_path=None):
        super(ProjectManagerView, self).__init__()
        if project_path is None:
            raise Exception("No project path specified")
        self.treeview = ttk.Treeview(self,
                                     columns=("name", "path"),
                                     height=128,
                                     selectmode="browse",
                                     show=("tree"))
        self.project_path = project_path
        for root, dirs, files in os.walk(project_path):
            self.treeview.insert()
            pass
