import setup_tests
import os
import tkinter as tk
from RTE.views.snippets import SnippetsAddingView

if __name__ == "__main__":
    root = tk.Tk()
    gui = SnippetsAddingView(root)
    gui.grid()
    root.mainloop()
