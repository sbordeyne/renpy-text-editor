import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk


class ImageLayer:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.path = ""
        self.img = None
        self.photo_img = None
        self.reference = None
        self.mouse_pos = (0, 0)
        self.margin = 5  # px, on either side of the selection box
        self.edge_mouse_coords = (0, 0)

        self.transforms = set()

        self.scale_factor = 1
        self.crop_rect = (0, 0, self.width, self.height)

    def __bool__(self):
        return True

    def __str__(self):
        return f"rect:{self.rect} - ref:{self.reference}"

    def hitbox(self, x, y):
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def move(self, x, y):
        self.transforms.add("xoffset")
        self.transforms.add("yoffset")
        self.x = x - self.mouse_pos[0]
        self.y = y - self.mouse_pos[1]

    @property
    def rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def on_image_edge(self, x, y, orientation):
        edge = self.get_image_edge(x, y)
        h = "right" in edge or "left" in edge
        v = "up" in edge or "down" in edge
        if orientation == "horizontal":
            return h
        elif orientation == "vertical":
            return v
        else:
            return (h and v)

    def get_image_edge(self, x, y):
        x0, y0, x1, y1 = self.rect
        m = self.margin
        right = (x0 - m <= x <= x0 + m)
        left = (x1 - m <= x <= x1 + m)
        up = (y0 - m <= y <= y0 + m)
        down = (y1 - m <= y <= y1 + m)
        rv = ""
        if right:
            rv += "right"
        if left:
            rv += "left"
        if up:
            rv += "up"
        if down:
            rv += "down"
        return rv

    def get_scale_factor(self, x, y):
        edge = self.get_image_edge(x, y)
        oldx, oldy = self.edge_mouse_coords
        if "right" in edge:
            return x / oldx
        elif "up" in edge:
            return oldy / y
        elif "down" in edge:
            return y / oldy
        elif "left" in edge:
            return oldx / x

    def rotate(self, angle, canvas):
        self.transforms.add("rotate")
        canvas.delete(self.reference)
        self.img = self.img.rotate(angle)
        self.photo_img = ImageTk.PhotoImage(self.img)
        self.reference = canvas.create_image((self.x, self.y),
                                             image=self.photo_img,
                                             anchor="nw")
        return canvas

    def scale(self, factor, canvas):
        self.transforms.add("zoom")
        canvas.delete(self.reference)
        self.img = self.img.resize((self.width * factor,
                                    self.height * factor),
                                   Image.NEAREST)
        self.photo_img = ImageTk.PhotoImage(self.img)
        self.reference = canvas.create_image((self.x, self.y),
                                             image=self.photo_img,
                                             anchor="nw")
        return canvas

    def crop(self, rect, canvas):
        self.transforms.add("crop")
        canvas.delete(self.reference)
        self.img = self.img.crop(rect)
        self.photo_img = ImageTk.PhotoImage(self.img)
        self.reference = canvas.create_image((self.x, self.y),
                                             image=self.photo_img,
                                             anchor="nw")
        return canvas


class LayeredImageBuilderGUI(tk.Frame):
    def __init__(self, master=None):
        super(LayeredImageBuilderGUI, self).__init__(master)
        self.master = master
        self.init_contextual()
        self.canvas = tk.Canvas(self, width=1024, height=768)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.master.bind('<Button-3>', self.display_contextual)
        self.master.bind('<Button-1>', self.on_left_mouse_click)
        self.master.bind('<B1-Motion>', self.on_left_mouse_move)
        self.master.bind('<ButtonRelease-1>', self.on_left_mouse_release)
        self.master.bind('<Motion>', self.on_mouse_movement)
        self.master.bind('<KeyPress>', self.on_key_pressed)
        self.master.bind('<KeyRelease>', self.on_key_released)
        self.images = []
        self.selected = None
        self.selection_rect = None
        self.dragging = False
        self.loop()

    def init_contextual(self):
        self.contextual_menu = tk.Menu(self, tearoff=0)
        self.contextual_menu.add_command(label='Add Image',
                                         command=self.add_image)
        self.contextual_menu.add_command(label="Clear All Images",
                                         command=self.clear_canvas)

    def display_contextual(self, event):
        try:
            self.contextual_menu.tk_popup(event.x_root, event.y_root, 0)
        except Exception:
            pass
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.contextual_menu.grab_release()

    def on_left_mouse_click(self, event):
        print(f"mouse click - {event.x} {event.y}")
        if self.selected is not None and self.selected.on_image_edge(event.x, event.y, "both"):
            self.selected.edge_mouse_coords = (event.x, event.y)
            self.dragging = True
        if self.selected is not None and self.selected.hitbox(event.x, event.y):
            self.selected.mouse_pos = (event.x, event.y)
        for img in reversed(self.images):
            if img.hitbox(event.x, event.y):
                self.selected = img
                self.selected.mouse_pos = (event.x, event.y)
                if self.selection_rect is None:
                    self.selection_rect = self.canvas.create_rectangle(self.selected.x, self.selected.y,
                                                                       self.selected.width, self.selected.height)
                return
        self.selected = None
        self.remove_selection_rect()
        return

    def on_left_mouse_move(self, event):
        if self.selected is not None:
            if self.selected.on_image_edge(event.x, event.y, "both"):
                factor = self.selected.get_scale_factor(event.x, event.y)
                print("\n\n\n", factor)
                self.canvas = self.selected.scale(factor, canvas)
            elif self.selected.hitbox(event.x, event.y):
                self.selected.move(event.x, event.y)
                self.canvas.coords(self.selected.reference, (self.selected.x, self.selected.y))
        if self.selection_rect is not None:
            self.canvas.coords(self.selection_rect, self.selected.rect)

    def on_mouse_movement(self, event):
        if self.selected is not None:
            if self.selected.on_image_edge(event.x, event.y, "horizontal"):
                self.canvas.config(cursor="sb_h_double_arrow")
            elif self.selected.on_image_edge(event.x, event.y, "vertical"):
                self.canvas.config(cursor="sb_v_double_arrow")
            else:
                self.canvas.config(cursor="left_ptr")
        else:
            self.canvas.config(cursor="left_ptr")

    def on_left_mouse_release(self, event):
        if self.dragging:
            self.dragging = False

    def on_key_pressed(self, event):
        print(event.keysym)

    def on_key_released(self, event):
        print(event.keysym)

    def clear_canvas(self):
        for img in self.images:
            self.canvas.delete(img.reference)
        self.images = []
        self.remove_selection_rect()

    def add_image(self):
        img_path = filedialog.askopenfilename()
        if not img_path:
            return
        i = Image.open(img_path)
        im = ImageTk.PhotoImage(i)
        layer = ImageLayer()
        layer.width = im.width()
        layer.height = im.height()
        layer.path = img_path
        layer.img = i
        layer.photo_img = im
        layer.reference = self.canvas.create_image((0, 0), image=im, anchor="nw")
        self.images.append(layer)
        return

    def remove_selection_rect(self):
        self.canvas.delete(self.selection_rect)
        self.selection_rect = None

    def loop(self):
        if self.selected:
            print(str(self.selected))
        self.canvas.update_idletasks()
        self.after(5, self.loop)
