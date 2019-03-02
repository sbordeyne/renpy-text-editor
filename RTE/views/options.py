import tkinter as tk
import tkinter.ttk as ttk

from RTE.config import config


class KeybindingsView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name = "Keybindings"
        pass

    def save_config(self):
        pass

class FormattingView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name = "Formatting"
        self.__init_variables()
        self.__init_tabs_spaces_frame()

    def __init_variables(self):
        self.show_whitespace = tk.IntVar()
        self.tabs_length = tk.StringVar()
        self.insert_spaces_over_tabs = tk.IntVar()

        self.insert_spaces_over_tabs.set(config.insert_spaces_instead_of_tabs)
        self.tabs_length.set(str(config.tabs_length))
        self.show_whitespace.set(config.show_whitespace_characters)

    def __init_tabs_spaces_frame(self):
        self.tabs_spaces_frame = tk.LabelFrame(self, text="Tabs and spaces settings")
        spaces_cb = tk.Checkbutton(self.tabs_spaces_frame,
                                   variable=self.insert_spaces_over_tabs,
                                   text="Insert spaces instead of tabs?")
        whitespace_cb = tk.Checkbutton(self.tabs_spaces_frame,
                                       variable=self.show_whitespace,
                                       text="Show Whitespace Characters?")
        tabs_length_sb = tk.Spinbox(self.tabs_spaces_frame, from_=2, to=12,
                                    increment=1, textvariable=self.tabs_length,
                                    text="Tabs Length")

        spaces_cb.grid(row=0)
        whitespace_cb.grid(row=1)
        tabs_length_sb.grid(row=2)
        self.tabs_spaces_frame.grid(row=0, column=0)

    def save_config(self):
        global config
        config.insert_spaces_instead_of_tabs = bool(self.insert_spaces_over_tabs.get())
        config.show_whitespace_characters = bool(self.show_whitespace.get())
        config.tabs_length = int(self.tabs_length.get())
        config.save()


class OptionsView(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        if controller is None:
            raise Exception("Controller excepted for OptionView Widget")
        else:
            self.controller = controller
        self.keybindings_view = KeybindingsView(self)
        self.formatting_view = FormattingView(self)

        self.notebook = ttk.Notebook(self)
        self.notebook.add(self.formatting_view, text=self.formatting_view.name)
        self.notebook.add(self.keybindings_view, text=self.keybindings_view.name)
        self.notebook.grid(row=0, column=0, columnspan=5, sticky="nswe")

        self.button_ok = tk.Button(self, text="OK", command=self.on_button_ok)
        self.button_cancel = tk.Button(self, text="Cancel", command=self.on_button_cancel)
        self.button_ok.grid(row=1, column=4)
        self.button_cancel.grid(row=1, column=5)

    def on_button_cancel(self):
        self.quit()

    def on_button_ok(self):
        self.keybindings_view.save_config()
        self.formatting_view.save_config()
        self.quit()

    def quit(self):
        self.controller.options_wm.destroy()
        self.controller.options_wm = None
