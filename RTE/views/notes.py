import tkinter as tk
from RTE.widgets.text import CustomText
from RTE.config import config
import tkinter.font as tkfont


class NotesView(tk.Frame):
    def __init__(self, master=None, project=None, **kwargs):
        super().__init__(master, **kwargs)
        self.text = CustomText(self, **config.get_theme().ui["text"])
        self.close_btn = tk.Button(self, command=self.on_close, image=tk.BitmapImage("assets/button-close.xbm"))
        self.project = project
        w = config.wm_width - config.side_notebook_width - config.scrollbar_width
        font = tkfont.Font(font=self.text["font"])
        self.text.bind('<<Change>>', self.on_change)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set,
                            wrap=tk.NONE,
                            undo=True,
                            width=w // font.measure(" "),
                            height=10)
        self.text.grid(row=0, column=0, columnspan=49)
        self.vsb.grid(row=0, column=50, sticky="ns")

    def on_change(self, event):
        if self.project is not None:
            self.project.save_notes()

    def on_close(self):
        self.grid_remove()
