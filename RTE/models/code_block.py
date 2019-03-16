import re
import tkinter as tk

class Block:
    tabs = re.compile(r'( {4})')
    start_re = re.compile(r'(.*:$|^ *#region.*)')
    end_re = re.compile(r'^ *#endregion.*')

    def __init__(self, parent=None, start=0, end=0, indent=0, text=""):
        self.children = []
        self.parent = parent
        if parent is not None:
            parent.children.append(self)
            self.start = start
            self.end = end
            self.indent = indent
        else:
            self.start = 0
            self.end = len(text)
            self.indent = 0
        self.collapsed = False
        self.text = text

    @property
    def image(self):
        self._img_opened = tk.BitmapImage(file="assets/button-collapse.xbm")
        self._img_collapsed = tk.BitmapImage(file="assets/button-open.xbm")
        if self.collapsed:
            return self._img_collapsed
        else:
            return self._img_opened

    @property
    def start_idx(self):
        return f"{self.start+1}.0 linestart"

    @property
    def end_idx(self):
        return f"{self.end}.0 lineend"

    def get_block(self, start):
        for child in self.get_all_children():
            if child.start == start:
                return child
        return self

    def get(self):
        return self.text

    def set_text(self, text):
        self.start = 0
        self.end = len(text)
        self.indent = 0
        self.text = text

    def detect(self):
        text = self.text.split("\n")
        i = 0
        while i < len(text):
            current_line = text[i]
            if self.start_re.match(current_line):
                indent = len(self.tabs.findall(current_line))
                for j, sub_line in enumerate(text[i:]):
                    new_indent = len(self.tabs.findall(sub_line))
                    # the end of the current block is when we reach the same ident
                    if (new_indent == indent and j != 0) or self.end_re.match(sub_line):
                        Block(parent=self, start=i, end=i + j, indent=indent, text="\n".join(text[i:j + i]))
                        i += j
                        break
            i += 1

    def detect_all(self):
        self.detect()
        for child in self.children:
            child.detect_all()

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return len(self.children) == 0

    def __contains__(self, item):
        if isinstance(item, int) or isinstance(item, float):
            return self.start <= int(item) <= self.end
        elif isinstance(item, Block):
            return item in self.children
        else:
            raise NotImplementedError

    def __len__(self):
        return self.end - self.start

    def get_all_children(self):
        """
            Method to return all the children of this block, recursively.

            Returns a list of all the children of this block.
        """
        rv = []
        for child in self.children:
            if child not in rv:
                rv.append(child)
                rv.extend(child.get_all_children())
        return rv

    def get_all_starts(self):
        rv = [self.start, ]
        for child in self.get_all_children():
            rv.append(child.start)
        return rv


if __name__ == "__main__":
    content = """
if test:
    for x in  list:
        print(x)

else:
    for y in other:
        print(test * y)
    """
    root = Block(text=content)
    root.detect_all()
    print(root.get_all_starts())
