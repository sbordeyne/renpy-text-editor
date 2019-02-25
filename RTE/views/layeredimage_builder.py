import tkinter as tk
import tkinter.filedialog as filedialog
# from PIL import Image, ImageTk


class ImageLayer:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.path = ""
        self.img = None


class LayeredImageBuilderGUI(tk.Frame):
    def __init__(self, master=None):
        super(LayeredImageBuilderGUI, self).__init__()
        self.master = master
        self.init_contextual()
        self.canvas = tk.Canvas(self, width=1024, height=768,
                                background="white")
        self.canvas.pack()
        self.master.bind('<Button-3>', self.display_contextual)
        self.images = []

    def init_contextual(self):
        self.contextual_menu = tk.Menu(self, tearoff=0)
        self.contextual_menu.add_command(label='Add Image',
                                         command=self.add_image)

    def display_contextual(self, event):
        try:
            self.contextual_menu.tk_popup(event.x_root, event.y_root, 0)
        except Exception:
            pass
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.contextual_menu.grab_release()

    def add_image(self):
        img_path = filedialog.askopenfilename()
        print(img_path)
        im = tk.PhotoImage(file=img_path)
        layer = ImageLayer()
        layer.width = im.width()
        layer.height = im.height()
        layer.path = img_path
        layer.img = self.canvas.create_image(0, 0, image=im, anchor="nw")
        self.images.append(layer)
        self.canvas.update_idletasks()
        return
