import tkinter as tk
from copy import copy
import tkinter.filedialog as filedialog
from RTE.utils import tr


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class KeybindingEntry(tk.Entry):
    def __init__(self, master=None, current=[]):
        super().__init__(master)

        self.keys_pressed = copy(current)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<KeyPress>", self.on_key_pressed)
        self.update()

    def on_focus_in(self, event):
        self.keys_pressed = []
        self.update()
        pass

    def on_key_pressed(self, event):
        keysym = self.format_keysym(event.keysym)
        if keysym not in self.keys_pressed:
            self.keys_pressed.append(keysym)
            self.update()
        return 'break'

    def format_keysym(self, keysym):
        keysym = keysym.capitalize()
        keysym = keysym.split("_")[0]
        return keysym

    def update(self):
        self.delete(0, tk.END)
        self.insert(tk.END, "+".join(self.keys_pressed))


class EntrySelectFolder(tk.Frame):
    def __init__(self, master=None, title="Select a directory", path=None):
        super().__init__(master)
        self.ety = tk.Entry(self)
        self.button_img = tk.BitmapImage("@assets/folder.xbm")
        button = tk.Button(self, bitmap=self.button_img, command=self.on_btn_click)

        self.ety.bind("<Double-Button-1>", self.on_btn_click)
        self.path = path
        if path is not None:
            self.ety.delete(0, tk.END)
            self.ety.insert(tk.END, self.path)

        self.ety.grid(row=0, column=0)
        button.grid(row=0, column=1)

    def on_btn_click(self, *args):
        self.path = filedialog.askdirectory(title=tr(self.title))
        self.ety.delete(0, tk.END)
        self.ety.insert(tk.END, self.path)
