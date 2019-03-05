import tkinter as tk
from PIL import Image, ImageTk


class ImageViewer(tk.Frame):
    def __init__(self, master=None, fpath=None):
        super().__init__(master)
        self.canvas = tk.Canvas(self, width=100, height=100)
        self.path = fpath
        i = Image.open(fpath)
        self.im = ImageTk.PhotoImage(i)
        width = self.im.width()
        height = self.im.height()
        self.canvas.config(width=width, height=height)
        self.reference = self.canvas.create_image((0, 0), image=self.im, anchor="nw")
        self.canvas.grid()
        self.loop()

    def loop(self):
        self.canvas.update_idletasks()
        self.after(5, self.loop)
