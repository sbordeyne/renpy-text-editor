import tkinter as tk
import tkinter.ttk as ttk
from .editor_window import EditorFrame
from .project_manager import ProjectManagerView
from RTE.controller import Controller
from .console import ConsoleView
from RTE.config import config


class MainWindowView(tk.PanedWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowView, self).__init__(*args, **kwargs)
        self.config(orient=tk.VERTICAL)
        self.texts = tk.PanedWindow(self)

        self.left_nb = ttk.Notebook(self)
        self.right_nb = ttk.Notebook(self)
        self.bottom_nb = ttk.Notebook(self)

        self.texts.add(self.left_nb)
        self.texts.add(self.right_nb)
        self.add(self.texts)
        self.add(self.bottom_nb)

        self.console_ui = ConsoleView(self)
        self.bottom_nb.add(self.console_ui, text="Console")

    def add_tab(self, side="left"):
        if side == "left":
            tab = EditorFrame(self)
            self.left_nb.add(tab)
        elif side == "right":
            tab = EditorFrame(self)
            self.right_nb.add(tab)
        else:
            raise Exception(f"Incorrect side specified. Values are (right|left) : {side}")


class RenpyTextEditorGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
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
        self.frame = tk.Frame(self)

        self.main = MainWindowView(self)

        self.project_manager = ProjectManagerView(self)
        self.project_manager.grid(row=0, column=0, sticky="ns")

        self.main.grid(row=0, column=1, sticky="ns")

        #elf.frame.grid(row=0, column=0)

    def __setup_menu(self):
        self.menubar = tk.Menu(self)
        self.master.config(menu=self.menubar)
        menufile = tk.Menu(self.menubar)
        self.menuthemes = tk.Menu(self.menubar)
        menutools = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=menufile)
        self.menubar.add_cascade(label="Themes", menu=self.menuthemes)
        self.menubar.add_cascade(label="Tools", menu=menutools)

        menufile.add_command(label="Open", command=self.controller.menus.file_open)
        menufile.add_command(label="Save", command=self.controller.menus.file_save)
        menufile.add_command(label="Save As", command=self.controller.menus.file_save_as)
        menufile.add_command(label="Quit", command=self.quit)

        for theme in self.controller.get_all_themes:
            self.menuthemes.add_radiobutton(label=theme,
                                            variable=self.current_theme)

        menutools.add_command(label="Layeredimage Builder", command=self.controller.menus.tools_open_layeredimage_builder)
        menutools.add_command(label="Variable Viewer", command=self.controller.menus.tools_open_variable_viewer)
        menutools.add_command(label="Screen Builder", command=self.controller.menus.tools_open_screen_builder)
        menutools.add_command(label="Options", command=self.controller.menus.tools_open_options)

    def loop(self):
        config.set_theme(self.current_theme.get())
        self.after(5, self.loop)

    def quit(self):
        self.master.destroy()
