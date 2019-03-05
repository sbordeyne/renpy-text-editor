import tkinter as tk
import tkinter.font as tkfont
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
    def __init__(self, master=None, windowside="left"):
        super(EditorFrame, self).__init__(master)
        self.master = master
        self.window_side = windowside
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.text.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal",
                                command=self.text.xview)
        self.text.configure(yscrollcommand=self.vsb.set,
                            xscrollcommand=self.hsb.set,
                            wrap=tk.NONE,
                            height=config.wm_height // 20,
                            undo=True)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.text.bind("<Tab>", self._tab_key_pressed)
        self.text.bind("<Key-space>", lambda event: self.on_key_whitespace(self.text, ' '))
        self.text.bind("<Key-Tab>", lambda event: self.on_key_whitespace(self.text, '\t'))
        self.text.bind("<Return>", lambda event: self.on_key_whitespace(self.text, '\n'))
        self.text.bind("<FocusIn>", lambda event: self.master.master.controller.set_last_entered_side(self.window_side))

        # self.text.bind("<Control-w>", self.init_theme)

        self.text.mark_set("range_start", "1.0")
        self.text.mark_set("range_end", "1.0")

        self.theme = config.get_theme()
        self.showinvis = config.show_whitespace_characters
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
        return 'break'

    def on_key_whitespace(self, char, event=None):
        convstr = ''
        if self.showinvis:
            if char == ' ':
                convstr = '·'
            elif char == '\t':
                convstr = '»\t'
            elif char == '\n':
                convstr = '¶\n'
            self.text.insert(tk.INSERT, convstr)

    def convert_whitespace_characters(self):
        if self.showinvis:
            convlst = [[' ', '·'], ['\t', '»\t'], ['\n', '¶\n']]
        else:
            convlst = [['·', ' '], ['»\t', '\t'], ['¶\n', '\n']]
        for i in range(len(convlst)):
            res = True
            char = convlst[i][0]
            subchar = convlst[i][1]
            while res:
                res = self.replace(char, subchar)

    def replace(self, char, subchar):
        where = '1.0'
        past_subchar = '1.0'
        while where:
            where = self.text.search(char, past_subchar, tk.END + '-1c')
            past_subchar = '{}+{}c'.format(where, len(subchar))
            past_char = '{}+{}c'.format(where, len(char))
            if where:
                self.text.delete(where, past_char)
                self.text.insert(where, subchar)
            else:
                return False

    def toggle_show_whitespace(self):
        self.showinvis = not self.showinvis
        config.show_whitespace_characters = self.showinvis
        self.convert_whitespace_characters()

    def test_colorize(self, curtoken):
        curtoken = str(curtoken)
        if self.window_side == "right" or not config.debug:
            return
        token_to_follow = ""
        token_to_follow = "Token." + token_to_follow
        if curtoken == token_to_follow:
            print(curtoken, " : ", self.text.get("range_start", 'range_end'))
        elif token_to_follow == "Token.all":
            print(curtoken, " : ", self.text.get("range_start", 'range_end'))

    def init_theme(self, *args):
        for token in self.theme:
            token.set_font()
            self.text.tag_configure(f"Token.{token.name}", **token.attributes)
        content = self.text.get("1.0", tk.END).split("\n")
        self.previous_content = ""
        self.text.config(**self.theme.ui["text"])
        font = tkfont.Font(font=self.text["font"])
        self.text.config(tabs=(font.measure(' ' * config.tabs_length), ))
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
                for tok in self.theme:
                    self.text.tag_configure(f"Token.{tok.name}", **tok.attributes)
                self.test_colorize(token)
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")

        self.previous_content = self.text.get("1.0", f"{row}.0")

    def set_text(self, fpath):
        with open(fpath, "r") as f:
            self.text.insert(tk.END, f.read())
        self.init_theme()

    def loop(self):
        self.after(5, self.loop)
