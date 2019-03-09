import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class Toolbar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = self.master.controller
        self.newfile_img = ImageTk.PhotoImage(image=Image.open("assets/newfile.png"))
        self.openfile_img = ImageTk.PhotoImage(image=Image.open("assets/openfile.png"))
        self.redo_img = ImageTk.PhotoImage(image=Image.open("assets/redo.png"))
        self.undo_img = ImageTk.PhotoImage(image=Image.open("assets/undo.png"))
        self.savefile_img = ImageTk.PhotoImage(image=Image.open("assets/savefile.png"))
        self.saveall_img = ImageTk.PhotoImage(image=Image.open("assets/saveall.png"))
        self.firstdiff_img = ImageTk.PhotoImage(image=Image.open("assets/firstdiff.png"))
        self.diff_img = ImageTk.PhotoImage(image=Image.open("assets/diff.png"))

        tk.Button(self, image=self.newfile_img, command=self.controller.menus.file_new).grid(row=0, column=0)
        tk.Button(self, image=self.openfile_img, command=self.controller.menus.file_open).grid(row=0, column=1)
        tk.Button(self, image=self.savefile_img, command=self.controller.menus.file_save).grid(row=0, column=2)
        tk.Button(self, image=self.saveall_img, command=self.controller.menus.file_save_all).grid(row=0, column=3)
        tk.Button(self, image=self.undo_img, command=self.controller.menus.edit_undo).grid(row=0, column=4)
        tk.Button(self, image=self.redo_img, command=self.controller.menus.edit_redo).grid(row=0, column=5)
        tk.Button(self, image=self.firstdiff_img, command=self.controller.mark_as_first_diff).grid(row=0, column=6)
        tk.Button(self, image=self.diff_img, command=self.controller.diff).grid(row=0, column=7)

