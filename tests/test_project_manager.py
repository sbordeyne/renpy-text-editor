import os
import setup_tests
from RTE.views.project_manager import ProjectManagerView
import tkinter as tk


if __name__ == '__main__':
    cwd = os.getcwd()
    path = os.path.join(cwd, "project")
    root = tk.Tk()
    gui = ProjectManagerView(root, path)
    gui.build_tree()
    gui.pack()
    root.mainloop()
