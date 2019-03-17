import tkinter as tk
import tkinter.ttk as ttk
import os
from RTE.config import config
from RTE.utils import autoscroll, get_type_by_extension
import tkinter.font as tkfont


class ProjectManagerView(tk.Frame):
    def __init__(self, master=None, project_path=None):
        super(ProjectManagerView, self).__init__(master)
        self._project_path = project_path
        self.init_treeview()

    def _get_project_path(self):
        return self._project_path

    def _set_project_path(self, ppath):
        self._project_path = ppath
        dir_ = os.path.abspath(self.project_path).replace('\\', '/')
        self.project_name = dir_.split("/")[-1]

    project_path = property(_get_project_path, _set_project_path)

    def init_treeview(self):
        global config
        self.vsb = ttk.Scrollbar(master=self, orient="vertical")
        self.hsb = ttk.Scrollbar(master=self, orient="horizontal")
        style = ttk.Style()
        style.configure("Custom.Treeview", **config.get_theme().ui["treeview"]["base"])
        style.configure("Custom.Treeview.Heading",
                        **config.get_theme().ui["treeview"]["heading"],
                        relief='flat')
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])
        self.tree = ttk.Treeview(self,
                                 columns=("fullpath", "type", "size"),
                                 displaycolumns=(),
                                 height=config.wm_height // 20,
                                 selectmode="browse",
                                 yscrollcommand=lambda f, l: autoscroll(self.vsb, f, l),
                                 xscrollcommand=lambda f, l: autoscroll(self.hsb, f, l),
                                 style='Custom.Treeview',
                                 )

        self.tree.heading("#0", text="Directory Structure", anchor='w')
        self.tree.heading("size", text="File Size", anchor='w')
        self.tree.column("size", stretch=0, width=100)

        self.vsb['command'] = self.tree.yview
        self.hsb['command'] = self.tree.xview

        self.tree.grid(row=0, column=0)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ns")
        self.tree.bind('<<TreeviewOpen>>', self.update_tree)
        self.tree.bind('<Double-Button-1>', self.on_double_click)
        self.images = []
        self.tree.tag_configure("base", **config.get_theme().ui["treeview"]["base"])

    def populate_tree(self, node=""):
        if self.tree.set(node, "type") != 'directory':
            return

        path = self.tree.set(node, "fullpath")
        # path = self.project_path
        self.tree.delete(*self.tree.get_children(node))

        #parent = self.tree.parent(node)
        special_dirs = [] #if parent else glob.glob('.') + glob.glob('..')

        for p in special_dirs + os.listdir(path):
            ptype = None
            p = os.path.join(path, p).replace('\\', '/')
            if os.path.isdir(p):
                ptype = "directory"
            elif os.path.isfile(p):
                ptype = "file"

            fname = os.path.split(p)[1]
            id_ = self.tree.insert(node, "end", text=fname, values=[p, ptype])

            if ptype == 'directory':
                if fname not in ('.', '..'):
                    self.images.append(tk.BitmapImage("assets/folder.xbm", **config.get_theme().bitmapimage))
                    self.tree.insert(id_, 0, text="dummy")
                    self.tree.item(id_, text=fname,
                                   image=self.images[-1],
                                   tags=("base",))
            elif ptype == 'file':
                extension = fname.split(".")[-1]
                if extension in ("png", "jpg", "image"):
                    img = tk.BitmapImage("assets/imagefile.xbm", **config.get_theme().bitmapimage)
                elif extension in ("webm", "mp4", "avi", "movie"):
                    img = tk.BitmapImage("assets/moviefile.xbm", **config.get_theme().bitmapimage)
                elif extension in ("mp3", "wav", "opus", "music"):
                    img = tk.BitmapImage("assets/musicfile.xbm", **config.get_theme().bitmapimage)
                else:
                    img = tk.BitmapImage("assets/textfile.xbm", **config.get_theme().bitmapimage)
                self.images.append(img)
                self.tree.item(id_, image=self.images[-1],
                               tags=("base",))

    def sort_tree(self, node, col="type", reverse=False):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children(node)]
        items.sort(reverse=reverse)
        for index, (val, k) in enumerate(items):
            self.tree.move(k, node, index)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children(''))

    def populate_roots(self):
        dir_ = os.path.abspath(self.project_path).replace('\\', '/')
        node = self.tree.insert('', 'end',
                                text=self.project_name.capitalize(),
                                values=[dir_, "directory"], open=True,
                                tags=("base",))
        self.populate_tree(node)
        self.sort_tree(node)


    def update_tree(self, event):
        tree = event.widget
        self.populate_tree(tree.focus())
        self.sort_tree(tree.focus())

    def on_double_click(self, event):
        tree = event.widget
        node = tree.focus()
        if tree.item(node)["values"][1] == "directory":
            to_open = not bool(tree.item(node, option="open"))
            try:
                tree.item(node, option={"open": to_open})
            except TypeError:
                pass
        elif tree.item(node)["values"][1] == "file":
            path = tree.item(node)["values"][0]
            ftype = get_type_by_extension(path.split("/")[-1].split(".")[-1])
            self.master.controller.open_file(path, ftype)

    def resize(self, width, height):
        # font = tkfont.Font(font=self.tree["font"])
        self.tree.config(height=height // 20)
