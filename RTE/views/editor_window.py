import tkinter as tk
import tkinter.ttk as ttk
from pygments import lex
from RTE.syntaxhighlight.lexer import RenpyLexer
from RTE.config import config


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class EditorFrame(tk.Frame):
    def __init__(self, master=None):
        super(EditorFrame, self).__init__()
        self.master = master
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.text.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal",
                                command=self.text.xview)
        self.text.configure(yscrollcommand=self.vsb.set,
                            xscrollcommand=self.hsb.set,
                            wrap=tk.NONE)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.text.bind("<Tab>", self._tab_key_pressed)

        self.theme = config.current_theme
        self.init_theme()

        self.loop()

    def _on_change(self, event):
        self.linenumbers.redraw()
        self.colorize()

    def _tab_key_pressed(self, event):
        if config.insert_spaces_instead_of_tabs:
            self.text.insert(tk.END, " " * config.tabs_length)
        else:
            self.text.insert(tk.END, "\t")

    def init_theme(self):
        global renpylexer
        for token in self.theme:
            self.text.tag_configure(f"Token.{token.name}", **token.attributes)
        content = self.text.get("1.0", tk.END).split("\n")
        self.previous_content = ""
        self.text.config(**self.theme.ui["text"])
        for i in range(1, len(content) + 1):
            self.colorize(i)

    def colorize(self, row=None):
        content = self.text.get("1.0", tk.END)
        lines = content.split("\n")
        if row is None:
            row = int(self.text.index("insert linestart").split(".")[0])

        if (self.previous_content != content):
            self.text.mark_set("range_start", f"{row}.0")
            data = self.text.get(f"{row}.0",
                                 f"{row}." + str(len(lines[int(row) - 1])))

            for token, content in lex(data, RenpyLexer()):
                self.text.mark_set("range_end",
                                   "range_start + %dc" % len(content))
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")

        self.previous_content = self.text.get("1.0", f"{row}.0")

    def loop(self):
        self.after(5, self.loop)
