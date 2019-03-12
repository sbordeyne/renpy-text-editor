import setup_tests
import os
import tkinter as tk
from RTE.views.options import OptionsView

if __name__ == "__main__":
    ctrl = setup_tests.TestController()
    root = tk.Tk()
    root.geometry("600x480")
    ctrl.options_wm = root
    root.title("Options")
    gui = OptionsView(root, controller=ctrl)
    gui.grid(sticky="nswe")
    root.mainloop()
