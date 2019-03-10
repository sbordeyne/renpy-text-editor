import re


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

    def get(self):
        return self.text

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



sample = """
start:
    start:
        start:
        end
    end
    start:
    end
end
start:
end
"""

sample2 = """
def detect_block(text):
    if start is None:
        for t in text:
            start += 5
            continue
        pass
    else:
        print(start)
    return start

label test_block:
    player_name "wow"
    show player 1
    return
"""

tabs = re.compile(r'( {4})')

expected = [(1, 8), (2, 5), (3, 4), (6, 7), (9, 10)]

def detect_block(text):
    import re
    tabs = re.compile(r'( {4})')
    start_re = re.compile(r' *(elif|else|except|finally|for|if|try|while|with|label|screen|transform|init|layeredimage|menu|style|# *region|def)\b')
    end_re = re.compile(r' *(\n|break|continue|return|yield|yield from|pass|# *endregion)\b')
    start_indices = []
    end_indices = []
    rv = []
    for line_nb, line in enumerate(text.split("\n")):
        indent = len(tabs.findall(line))
        if start_re.match(line):
            start_indices.append((line_nb, indent))
        elif end_re.match(line):
            end_indices.append((line_nb, indent))
    for i, (idx, idx_indent) in enumerate(start_indices):
        for jdx, jdx_indent in end_indices:
            if jdx_indent == idx_indent and jdx > idx:
                rv.append((idx, jdx))
                break
    return rv


def detect(text):
    import re
    tabs = re.compile(r'( {4})')
    start_re = re.compile(r'(.*:$|^ *#region.*)')
    end_re = re.compile(r'^ *#endregion.*')
    text = text.split("\n")
    root = Block(start=0, end=len(text), text="\n".join(text))
    i = 0
    while i < len(text):
        current_line = text[i]
        if start_re.match(current_line):
            indent = len(tabs.findall(current_line))
            for j, sub_line in enumerate(text[i:]):
                new_indent = len(tabs.findall(sub_line))
                # the end of the current block is when we reach the same ident
                if (new_indent == indent and j != 0) or end_re.match(sub_line):
                    Block(parent=root, start=i, end=i + j, indent=indent, text="\n".join(text[i:j + i]))
                    i += j
                    break
        i += 1
    return root


root = Block(text=sample2)
root.detect_all()

for child in root.get_all_children():
    print(child.text)
    print()
