import tkinter as tk
import tkinter.ttk as ttk
from RTE.models.snippet import snippet_store
from RTE.config import config
from RTE.utils import autoscroll, EntryWithPlaceholder, tr


class SnippetsView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        global config
        self.vsb = ttk.Scrollbar(orient="vertical")
        self.tree = ttk.Treeview(self,
                                 columns=("name"),
                                 displaycolumns=(),
                                 height=config.wm_height // 20,
                                 selectmode="browse",
                                 yscrollcommand=lambda f, l: autoscroll(self.vsb, f, l),
                                 style="Custom.Treeview",
                                 )
        self.tree.heading("#0", text="Snippets", anchor='w')

        self.vsb['command'] = self.tree.yview

        self.tree.grid(row=0, column=0)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.tree.bind('<Double-Button-1>', self.insert_snippet)
        self.update()
        self.loop()

    def update(self):
        self.tree.delete(*self.tree.get_children(''))
        for sname, snippet in snippet_store.snippets.items():
            self.tree.insert("", "end", text=snippet.name, values=[sname])
        snippet_store.has_new_snippet = False

    def insert_snippet(self, event):
        item = self.tree.selection()[0]
        snippetname = self.tree.item(item)["values"][0]
        snippet = snippet_store.snippets[snippetname]
        controller = self.master.controller
        text = controller.view.get_current_text(controller.last_entered_side).text
        snippet.insert(text)
        pass

    def loop(self):
        if snippet_store.has_new_snippet:
            self.update()
        self.after(5, self.loop)

    pass


class SnippetsAddingView(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_cancel_btn)
        self.controller = controller

        self.sname = tk.StringVar()
        self.sname.trace_add("write", self.on_sname_change)
        self.sid = tk.StringVar()
        self.replace_select = tk.IntVar()

        self.sname_ety = EntryWithPlaceholder(self,
                                              placeholder=tr("Snippet Name"),
                                              textvariable=self.sname)
        self.sid_ety = EntryWithPlaceholder(self,
                                            placeholder="",
                                            textvariable=self.sid)
        self.replace_select_cb = tk.Checkbutton(self, variable=self.replace_select)
        self.before_cursor_txt = tk.Text(self, width=30, height=10)
        self.after_cursor_txt = tk.Text(self, width=30, height=10)
        self.ok_btn = tk.Button(self, text=tr("Ok"), command=self.on_ok_btn)
        self.cancel_btn = tk.Button(self, text=tr("Cancel"), command=self.on_cancel_btn)

        self.sname_ety.grid(row=0, column=1)
        self.sid_ety.grid(row=1, column=1)
        self.replace_select_cb.grid(row=2, column=1)
        self.before_cursor_txt.grid(row=3, column=1)
        self.after_cursor_txt.grid(row=4, column=1)
        self.ok_btn.grid(row=5, column=0, sticky="we")
        self.cancel_btn.grid(row=5, column=1)

        tk.Label(self, text=tr("Snippet Name :")).grid(row=0, column=0)
        tk.Label(self, text=tr("Snippet Id :")).grid(row=1, column=0)
        tk.Label(self, text=tr("Replace Selection ?")).grid(row=2, column=0)
        tk.Label(self, text=tr("Before Cursor :")).grid(row=3, column=0)
        tk.Label(self, text=tr("After Cursor :")).grid(row=4, column=0)

    def on_ok_btn(self):
        data = {"name": self.sname.get(),
                "replace_selection": self.replace_select.get() == 1,
                "before_cursor": self.before_cursor_txt.get("1.0", "end"),
                "after_cursor": self.after_cursor_txt.get("1.0", "end")}
        snippet_store.add(self.sid.get(), **data)
        self.on_cancel_btn()
        pass

    def on_cancel_btn(self):
        self.controller.add_snippet_wm = None
        self.master.destroy()
        pass

    def on_sname_change(self, *args):
        text = self.sname.get()
        text = text.lower()
        text = text.replace(" ", "_")
        text = text.replace("'", "")
        self.sid.set(text)

