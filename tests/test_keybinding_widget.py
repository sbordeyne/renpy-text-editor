import setup_tests
import tkinter as tk
from RTE.widgets.debounce import DebounceTk

class KeybindingEntry(tk.Entry):
    def __init__(self, master=None):
        super().__init__(master)
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
        pass

    def format_keysym(self, keysym):
        keysym = keysym.capitalize()
        keysym = keysym.split("_")[0]
        return keysym

    def update(self):
        self.delete(0, tk.END)
        self.insert(tk.END, "+".join(self.keys_pressed))


if __name__ == '__main__':
    root = DebounceTk()
    ety = KeybindingEntry(root)
    ety2 = KeybindingEntry(root)
    ety.pack(side=tk.TOP, fill=tk.Y)
    ety2.pack(side=tk.TOP, fill=tk.Y)
    root.mainloop()
