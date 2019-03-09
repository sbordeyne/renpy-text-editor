import tkinter as tk
import tkinter.ttk as ttk
from RTE.models.snippet import snippet_store
from RTE.config import config
from RTE.utils import autoscroll


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

    def update(self):
        self.tree.delete(*self.tree.get_children(''))
        for sname, snippet in snippet_store.snippets.items():
            self.tree.insert("", "end", text=snippet.name, values=[sname])

    def insert_snippet(self, event):
        item = self.tree.selection()[0]
        snippetname = self.tree.item(item)["values"][0]
        snippet = snippet_store.snippets[snippetname]
        controller = self.master.controller
        text = controller.view.get_current_text(controller.last_entered_side).text
        snippet.insert(text)
        pass

    pass
