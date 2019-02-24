import tkinter as tk
import tkinter.ttk as ttk
from .editor_window import EditorFrame
from .project_manager import ProjectManagerView
from RTE.controller import Controller
from .console import ConsoleView
from RTE.config import config

class RenpyTextEditorGUI(tk.Frame):
    def __init__(self, master=None):
        super(RenpyTextEditorGUI, self).__init__()
        self.master = master
        self.controller = Controller(self)
        self.__setup_variables()
        self.__setup_menu()
        self.__setup_ui()
        return

    def __setup_variables(self):
        self.current_theme = tk.StringVar()
        self.current_theme.set(config.theme_name)

    def __setup_ui(self):
        self.main_frame = tk.PanedWindow(self, orient=tk.VERTICAL)
        self.text_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.left_notebook = ttk.Notebook(self)
        self.right_notebook = ttk.Notebook(self)
        self.bottom_notebook = ttk.Notebook(self)
        self.text_window.add(self.left_notebook)
        self.text_window.add(self.right_notebook)
        self.main_frame.add(self.text_window)
        self.main_frame.add(self.bottom_notebook)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.project_manager = ProjectManagerView()
        self.project_manager.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.console_ui = ConsoleView(self)
        self.bottom_notebook.add(self.console_ui, text="Console")

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
        self.menuthemes = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=menufile)
        self.menubar.add_cascade(label="Themes", menu=self.menuthemes)

        menufile.add_command(label="Open", command=self.controller.menus.file_open)
        menufile.add_command(label="Save", command=self.controller.menus.file_save)
        menufile.add_command(label="Save As", command=self.controller.menus.file_save_as)
        menufile.add_command(label="Quit", command=self.quit)

        for theme in self.controller.get_all_themes:
            self.menuthemes.add_radiobutton(label=theme,
                                            variable=self.current_theme)

    def loop(self):
        config.set_theme(self.current_theme.get())
        self.after(5, self.loop)

    def quit(self):
        self.master.destroy()

