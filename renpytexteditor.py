from RTE.views.main import RenpyTextEditorGUI
import tkinter as tk
from RTE.constants import assets
from RTE.config import config
import os


def main():
    root = tk.Tk()
    root.geometry(config.geometry)
    root.title("Renpy Text Editor")
    # root.iconbitmap(assets.folder())
    view = RenpyTextEditorGUI(root)
    view.grid(sticky="nswe")
    view.main.add_tab("left")
    view.main.add_tab("right")
    root.mainloop()


if __name__ == '__main__':
    main()
