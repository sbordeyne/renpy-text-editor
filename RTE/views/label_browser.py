import tkinter as tk
import tkinter.ttk as ttk
from RTE.config import config


class LabelBrowserView(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.project = self.master.master.controller.project

    def __init_treeview(self):
        self.tree = ttk.Treeview(self,
                                 columns=("name", ),
                                 displaycolumns=(),
                                 height=config.wm_height // 20,
                                 selectmode='browse',
                                 style='Custom.Treeview')
