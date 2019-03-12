import tkinter as tk
import tkinter as ttk


class DialogueEntry(tk.Toplevel):
    """
        DialogueEntry : tkinter.Toplevel

        Dialgue box that allow the user to input a text in a field.

        kwargs :
            title : title of the dialogue box
            text : text displayed in the label of the dialogue box
            ok_button_callback : callable that is called when the ok button is pressed
            textvariable : tkinter.StringVar that is used in the Entry widget
            width : 300 by default, width of the window
            height : 70 by default, height of the window
            xpos, ypos : screen coordinates. By default, these coordinates place the window in the middle of the screen

        methods :
            get(self) : gets the string in the entry widget
            set(self, value) : sets the string in the entry widget
    """
    def __init__(self, *args, title="Please Enter a value", text="Enter a value", ok_button_callback=None, textvariable=None, width=300, height=70, xpos=None, ypos=None, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = width, height
        if xpos is None:
            ws = self.winfo_screenwidth()  # width of the screen
            x = (ws // 2) - (w // 2)
        else:
            x = xpos
        if ypos is None:
            hs = self.winfo_screenheight()  # height of the screen
            y = (hs // 2) - (h // 2)
        else:
            y = ypos

        self.title(title)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.resizable(False, False)
        self.update()
        self.textvar = textvariable or tk.StringVar()
        self.ok_button_callback = ok_button_callback
        self.entry = tk.Entry(self, textvariable=self.textvar, width=w // 6)
        self.ok_btn = tk.Button(self, text="Ok", command=self.on_ok_btn)
        self.cancel_btn = tk.Button(self, text="Cancel", command=self.on_cancel_btn)
        self.label = tk.Label(self, text=text)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel_btn)

        self.label.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.entry.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.ok_btn.grid(row=2, column=0, sticky="ew")
        self.cancel_btn.grid(row=2, column=1, sticky="ew")
        self.mainloop()

    def on_ok_btn(self):
        if callable(self.ok_button_callback):
            self.ok_button_callback()
        self.on_cancel_btn()
        pass

    def on_cancel_btn(self):
        self.destroy()
        pass

    def get(self):
        return self.textvar.get()

    def set(self, value):
        self.textvar.set(value)


if __name__ == '__main__':
    def open_entry():
        DialogueEntry()
    root = tk.Tk()
    btn = tk.Button(root, text="open entry toplevel", command=open_entry)
    btn.pack()
    root.mainloop()
