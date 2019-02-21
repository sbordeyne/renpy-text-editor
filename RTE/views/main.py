import tkinter as tk
import tkinter.ttk as ttk
from .editor_window import EditorFrame
from RTE.controller import Controller


class RenpyTextEditorGUI(tk.Frame):
    def __init__(self, master=None):
        super(RenpyTextEditorGUI, self).__init__()
        self.master = master
        self.controller = Controller()
        self.__setup_menu()
        self.__setup_ui()
        return

    def __setup_ui(self):
        self.main_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.left_notebook = ttk.Notebook(self)
        self.right_notebook = ttk.Notebook(self)
        self.main_window.add(self.left_notebook)
        self.main_window.add(self.right_notebook)
        self.main_window.grid(row=0, column=1)

    def add_tab(self, side="left"):
        if side == "left":
            tab = EditorFrame(self)
            self.left_notebook.add(tab)
        elif side == "right":
            tab = EditorFrame(self)
            self.right_notebook.add(tab)
        else:
            raise Exception(f"Incorrect side specified. Values are (right|left) : {side}")

    def __setup_menu(self):
        self.menubar = tk.Menu(self)
        self.master.config(menu=self.menubar)
        menufile = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=menufile)

        menufile.add_command(label="New", command=self.controller.menus.file_new)
        menufile.add_command(label="Open", command=self.controller.menus.file_open)
        menufile.add_command(label="Save", command=self.controller.menus.file_save)
        menufile.add_command(label="Save As", command=self.controller.menus.file_save_as)
        menufile.add_command(label="Quit", command=self.quit)

    def quit(self):
        self.master.destroy()

