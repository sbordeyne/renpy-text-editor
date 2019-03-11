import tkinter as tk


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
    def __init__(self, master=None, keybinder_inst=None, target_keybind=""):
        super().__init__(master)

        self.keybinder = keybinder_inst
        self.target = target_keybind

        current = getattr(self.keybinder, self.target)[1:-1]
        if current:
            self.keys_pressed = current.split("-")
        else:
            self.keys_pressed = []
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<KeyPress>", self.on_key_pressed)
        self.bind('<KeyRelease>', self.on_key_released)

    def on_focus_in(self, event):
        self.keys_pressed = []
        self.update()
        pass

    def on_key_pressed(self, event):
        keysym = self.format_keysym(event.keysym)
        if keysym not in self.keys_pressed:
            self.keys_pressed.append(keysym)
            self.update()
        pass

    def on_key_released(self, event):
        v = "<" + "-".join(self.keys_pressed) + ">"
        setattr(self.keybinder, self.target, v)
        pass

    def format_keysym(self, keysym):
        keysym = keysym.capitalize()
        keysym = keysym.split("_")[0]
        return keysym

    def update(self):
        self.delete(0, tk.END)
        self.insert(tk.END, "+".join(self.keys_pressed))
