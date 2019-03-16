import tkinter as tk
import tkinter.ttk as ttk
from .editor_window import EditorFrame
from .project_manager import ProjectManagerView
from RTE.controllers.controller import Controller
from .console import ConsoleView
from .variable_viewer import VariableViewerView
from .snippets import SnippetsView
from .toolbar import Toolbar
from .debugger import DebuggerView
from RTE.config import config
import tkinter.font as tkfont
from RTE.models.snippet import snippet_store
from RTE.utils import tr, method_toggle
from RTE.widgets.notebooks import CloseableNotebook
from RTE.config import keybindings

class MainWindowView(tk.PanedWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowView, self).__init__(*args, **kwargs)
        self.config(orient=tk.VERTICAL)
        self.config(**config.get_theme().ui["frame"])
        self.texts = tk.PanedWindow(self)

        self.left_nb = CloseableNotebook(self, side="left")
        self.right_nb = CloseableNotebook(self, side="right")
        self.bottom_nb = ttk.Notebook(self)

        self.texts.add(self.left_nb)
        self.texts.add(self.right_nb)
        self.add(self.texts)
        self.add(self.bottom_nb)

        self.console_ui = ConsoleView(self.bottom_nb)
        self.bottom_nb.add(self.console_ui, text=tr("Console"))
        self.variable_viewer_ui = VariableViewerView(self.bottom_nb)
        self.bottom_nb.add(self.variable_viewer_ui, text=tr("Variable Viewer"))
        self.debugger_ui = DebuggerView(master=self.bottom_nb)
        self.bottom_nb.add(self.debugger_ui, text=tr("Debugger"))

        self.left_tabs = []
        self.right_tabs = []

    def add_tab(self, file_):
        side = file_.window_side
        fpath = file_.path
        fname = file_.fullname
        tab = EditorFrame(self, file_)
        if fpath is not None:
            tab.set_text(fpath)
        if side == "left":
            self.left_nb.add(tab, text=fname)
            self.left_tabs.append(tab)
            self.left_nb.select(tab)
        elif side == "right":
            self.right_nb.add(tab, text=fname)
            self.right_tabs.append(tab)
            self.right_nb.select(tab)
        else:
            raise Exception(f"Incorrect side specified. Values are (right|left) : {side}")


    def resize(self, width, height):
        self.config(width=width,
                    height=height)
        #self.left_nb.config(width=width // 2, height=height - 300)
        #self.right_nb.config(width=width // 2, height=height - 300)
        #self.bottom_nb.config(width=width, height=300)


class RenpyTextEditorGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.controller = Controller(self)
        self.__setup_variables()
        self.__setup_menu()
        self.__setup_ui()
        self.__setup_binds()
        self.config(**config.get_theme().ui["frame"])
        self.loop()
        self.slowloop()
        return

    def __setup_variables(self):
        self.current_theme = tk.StringVar()
        self.current_theme.set(config.theme_name)

    def __setup_ui(self):
        self.toolbar = Toolbar(self)

        self.main = MainWindowView(self)
        self.side_notebook = ttk.Notebook(self, width=config.side_notebook_width)
        self.project_manager = ProjectManagerView(self)
        self.snippets = SnippetsView(self)

        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.side_notebook.grid(row=1, column=0, sticky="ns")
        self.side_notebook.add(self.project_manager, text=tr("Project Manager"))
        self.side_notebook.add(self.snippets, text=tr("Snippets"))

        self.main.grid(row=1, column=1, sticky="ns")

    def __setup_menu(self):
        theme = config.get_theme()
        self.menubar = tk.Menu(self, **theme.ui["menu"])
        self.master.config(menu=self.menubar)
        menufile = tk.Menu(self.menubar, **theme.ui["menu"])
        self.menuthemes = tk.Menu(self.menubar, **theme.ui["menu"])
        menutools = tk.Menu(self.menubar, **theme.ui["menu"])
        menuedit = tk.Menu(self.menubar, **theme.ui["menu"])
        menuedit_formatting = tk.Menu(menuedit, **theme.ui["menu"])

        self.menubar.add_cascade(label=tr("File"), menu=menufile)
        self.menubar.add_cascade(label=tr("Edit"), menu=menuedit)
        self.menubar.add_cascade(label=tr("Themes"), menu=self.menuthemes)
        self.menubar.add_cascade(label=tr("Tools"), menu=menutools)

        menufile.add_command(label=tr("New"), command=self.controller.menus.file_new)
        menufile.add_command(label=tr("Open"), command=self.controller.menus.file_open)
        menufile.add_command(label=tr("Save"), command=self.controller.menus.file_save)
        menufile.add_command(label=tr("Save As"), command=self.controller.menus.file_save_as)
        menufile.add_command(label=tr("Quit"), command=self.quit)

        menuedit.add_command(label=tr("Undo"), command=self.controller.menus.edit_undo)
        menuedit.add_command(label=tr("Redo"), command=self.controller.menus.edit_redo)
        menuedit.add_command(label=tr("Duplicate line/selection"), command=self.controller.menus.edit_duplicate)
        menuedit.add_command(label=tr("Comment/Uncomment"), command=self.controller.menus.edit_comment)
        menuedit.add_cascade(label=tr("Formatting"), menu=menuedit_formatting)

        menuedit_formatting.add_command(label=tr("To UPPERCASE"), command=self.controller.menus.edit_formatting_upper)
        menuedit_formatting.add_command(label=tr("To lowercase"), command=self.controller.menus.edit_formatting_lower)
        menuedit_formatting.add_command(label=tr("To Capitalized"), command=self.controller.menus.edit_formatting_capitalized)
        menuedit_formatting.add_command(label=tr("To iNVERT cASING"), command=self.controller.menus.edit_formatting_invert)
        menuedit_formatting.add_command(label=tr("To RAnDom CASinG"), command=self.controller.menus.edit_formatting_random)
        menuedit_formatting.add_command(label=tr("To SpOnGeBoB cAsInG"), command=self.controller.menus.edit_formatting_spongebob)

        for theme in self.controller.get_all_themes:
            self.menuthemes.add_radiobutton(label=theme,
                                            variable=self.current_theme)

        menutools.add_command(label=tr("Layeredimage Builder"), command=self.controller.menus.tools_open_layeredimage_builder)
        menutools.add_command(label=tr("Variable Viewer"), command=self.controller.menus.tools_open_variable_viewer)
        menutools.add_command(label=tr("Screen Builder"), command=self.controller.menus.tools_open_screen_builder)
        menutools.add_command(label=tr("Add Snippet"), command=self.controller.menus.tools_open_add_snippet)
        menutools.add_command(label=tr("Options"), command=self.controller.menus.tools_open_options)

    def __setup_binds(self):
        self.bind('<Configure>', self.on_configure)
        self.bind(keybindings.quit, self.quit)
        self.bind(keybindings.to_upper, self.controller.menus.edit_formatting_upper)
        self.bind(keybindings.to_lower, self.controller.menus.edit_formatting_lower)
        self.bind(keybindings.to_capitalize, self.controller.menus.edit_formatting_capitalized)
        self.bind(keybindings.to_invert_casing, self.controller.menus.edit_formatting_invert)
        self.bind(keybindings.to_random_casing, self.controller.menus.edit_formatting_random)
        self.bind(keybindings.to_spongebob_casing, self.controller.menus.edit_formatting_spongebob)
        self.bind(keybindings.save_file, self.controller.menus.file_save)
        self.bind(keybindings.save_as, self.controller.menus.file_save_as)
        self.bind(keybindings.save_all, self.controller.menus.file_save_all)
        self.bind(keybindings.new_file, self.controller.menus.file_new)
        self.bind(keybindings.open_project, self.controller.menus.file_open)
        self.bind(keybindings.duplicate, self.controller.menus.edit_duplicate)
        self.bind(keybindings.comment_selected, self.controller.menus.edit_comment)

    def on_configure(self, event):
        global config
        config.wm_width = int(event.width)
        config.wm_height = int(event.height)
        pass


    def get_current_text(self, side):
        if side == "left":
            tabid = self.main.left_nb.select()
            return self.main.left_tabs[self.main.left_nb.index(tabid)]
        else:
            tabid = self.main.right_nb.select()
            return self.main.right_tabs[self.main.right_nb.index(tabid)]


    def slowloop(self):
        return
        w, h = config.wm_width, config.wm_height
        self.side_notebook.config(width=config.side_notebook_width, height=h)
        self.project_manager.resize(config.side_notebook_width, h)
        self.snippets.resize(config.side_notebook_width, h)
        self.main.resize(w - config.side_notebook_width, h)
        self.after(100, self.slowloop)

    def loop(self):
        config.set_theme(self.current_theme.get())
        self.after(5, self.loop)

    def quit(self):
        global config
        config.wm_width = int(self.master.winfo_width())
        config.wm_height = int(self.master.winfo_height())
        config.save()
        keybindings.save()
        snippet_store.save()
        self.master.destroy()
