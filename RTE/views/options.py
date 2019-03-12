import tkinter as tk
import tkinter.ttk as ttk
import string

from RTE.config import config, keybindings
from RTE.widgets.entries import KeybindingEntry
from RTE.utils import tr
from RTE.models.locale import Translator

class KeybindingsView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name = tr("Keybindings")
        self.entries = []
        for i, (key, value) in enumerate(keybindings._attrs.items()):
            if value:
                cur = value[1:-1].split("-")
                current = []
                for char in cur:
                    if char in string.ascii_letters:
                        c = char.upper()
                    else:
                        c = char
                    current.append(c)
            else:
                current = []
            if i > 20:
                j = 2
            else:
                j = 0
            ety = KeybindingEntry(self, current)
            lbl = tk.Label(self, text=tr(f"{key.capitalize()} :"))
            lbl.grid(row=i, column=j)
            ety.grid(row=i, column=j + 1)
            self.entries.append((ety, key))
        pass

    def save_config(self):
        for ety, key in self.entries:
            kp = []
            for c in ety.keys_pressed:
                if c in string.ascii_letters:
                    char = c.lower()
                else:
                    char = c
                kp.append(char)
            v = "<" + "-".join(kp) + ">"
            setattr(keybindings, key, v)
        pass

class GeneralView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name = tr("General")
        self.__init_variables()
        self.__init_tabs_spaces_frame()

    def __init_variables(self):
        self.locale_code = tk.StringVar()
        self.locale_code.set(config.locale)
        pass

    def __init_tabs_spaces_frame(self):
        self.formatting_frame = FormattingView(master=self, text=tr("Formatting"))
        self.formatting_frame.grid(row=0, column=0, columnspan=2)

        self.locale_combo = ttk.Combobox(self, values=Translator.get_all_locales(),
                                         textvariable=self.locale_code,
                                         state="readonly",
                                         justify="left",
                                         height=10)
        self.locale_combo.grid(row=1, column=1)
        tk.Label(self, text=tr("Language :")).grid(row=1, column=0)


    def save_config(self):
        self.formatting_frame.save_config()
        global config
        config.locale = self.locale_code.get()
        config.save()


class FormattingView(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.__init_variables()
        self.__setup_ui()

    def __setup_ui(self):
        tk.Label(self, text=tr("Insert spaces instead of tabs? ")).grid(row=0, column=0)
        tk.Label(self, text=tr("Show Whitespace Characters? ")).grid(row=1, column=0)
        tk.Label(self, text=tr("Start maximized? ")).grid(row=2, column=0)
        tk.Label(self, text=tr("Tabs Length :")).grid(row=3, column=0)

        spaces_cb = tk.Checkbutton(self,
                                   variable=self.insert_spaces_over_tabs)
        whitespace_cb = tk.Checkbutton(self,
                                       variable=self.show_whitespace)
        start_maximized_cb = tk.Checkbutton(self,
                                            variable=self.start_maximized)
        tabs_length_sb = tk.Spinbox(self, from_=2, to=12,
                                    increment=1, textvariable=self.tabs_length)
        spaces_cb.grid(row=0, column=1)
        whitespace_cb.grid(row=1, column=1)
        tabs_length_sb.grid(row=2, column=1)
        start_maximized_cb.grid(row=3, column=1)


    def __init_variables(self):
        self.show_whitespace = tk.IntVar()
        self.tabs_length = tk.StringVar()
        self.insert_spaces_over_tabs = tk.IntVar()
        self.start_maximized = tk.IntVar()

        self.insert_spaces_over_tabs.set(config.insert_spaces_instead_of_tabs)
        self.tabs_length.set(str(config.tabs_length))
        self.show_whitespace.set(config.show_whitespace_characters)
        self.start_maximized.set(config.start_maximized)


    def save_config(self):
        global config
        config.insert_spaces_instead_of_tabs = bool(self.insert_spaces_over_tabs.get())
        config.show_whitespace_characters = bool(self.show_whitespace.get())
        config.tabs_length = int(self.tabs_length.get())
        config.start_maximized = bool(self.start_maximized.get())


class OptionsView(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        if controller is None:
            raise Exception("Controller expected for OptionView Widget")
        else:
            self.controller = controller
        self.master.resizable(False, False)
        self.master.update()

        self.notebook = ttk.Notebook(self, width=self.master.winfo_width(),
                                     height=self.master.winfo_height() - 50)
        self.notebook.grid(row=0, column=0, columnspan=5, sticky="nswe")

        self.keybindings_view = KeybindingsView(self.notebook)
        self.general_view = GeneralView(self.notebook)

        self.notebook.add(self.general_view, text=self.general_view.name, sticky="nswe")
        self.notebook.add(self.keybindings_view, text=self.keybindings_view.name, sticky="nswe")

        self.button_ok = tk.Button(self, text=tr("OK"), command=self.on_button_ok)
        self.button_cancel = tk.Button(self, text=tr("Cancel"), command=self.on_button_cancel)
        self.button_ok.grid(row=1, column=3)
        self.button_cancel.grid(row=1, column=4)

    def on_button_cancel(self):
        self.quit()

    def on_button_ok(self):
        self.keybindings_view.save_config()
        self.general_view.save_config()
        self.quit()

    def quit(self):
        self.controller.options_wm.destroy()
        self.controller.options_wm = None
