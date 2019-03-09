from RTE.views.main import RenpyTextEditorGUI
import tkinter as tk
from RTE.constants import assets
from RTE.config import config
from RTE.models.file import File
import os


def main():
    root = tk.Tk()
    config.validate_width_height(root)
    if config.start_maximized:
        root.state('zoomed')
    else:
        root.geometry(config.geometry)
    root.title("Renpy Text Editor")
    try:
        root.iconbitmap(default="assets/favicon.ico")
    except tk.TclError:
        # root.iconphoto(default=tk.PhotoImage("favicon.png"))
        root.iconbitmap('@assets/favicon.xbm')
    view = RenpyTextEditorGUI(root)
    view.grid(sticky="nswe")
    view.main.add_tab(File("", "left", is_new=True))
    view.main.add_tab(File("", "right", is_new=True))
    root.mainloop()


if __name__ == '__main__':
    main()
