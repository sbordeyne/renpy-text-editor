import re


class Block:
    tabs = re.compile(r'( {4})')
    start_re = re.compile(r' *(elif|else|except|finally|for|if|try|while|with|label|screen|transform|init|layeredimage|menu|style|# *region|def)\b')
    end_re = re.compile(r' *(\n|break|continue|return|yield|yield from|pass|# *endregion)\b')

    def __init__(self, parent=None, start=0, end=0, indent=0, text=""):
        self.children = []
        self.parent = parent
        if parent is not None:
            parent.children.append(self)
        self.start = start
        self.end = end
        self.indent = indent
        self.text = text

    def get(self, text):
        return '\n'.join(text.split("\n")[self.start:self.end])

    def detect(self, text):
        start_indices = []
        end_indices = []
        for line_nb, line in enumerate(self.get(text).split("\n")):
            indent = len(self.tabs.findall(line))
            if indent > self.indent + 1:
                continue
            if self.start_re.match(line):
                start_indices.append((line_nb, indent))
            elif self.end_re.match(line):
                end_indices.append((line_nb, indent))
        for i, (idx, idx_indent) in enumerate(start_indices):
            for jdx, jdx_indent in end_indices:
                if jdx_indent == idx_indent and jdx > idx and idx_indent == self.indent + 1:
                    self.children.append(Block(self, idx, jdx, idx_indent))
                    break

    def detect_all(self, text):
        self.detect(text)
        for child in self.children:
            child.detect_all(text)

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return len(self.children) == 0


sample = """
start
    start
        start
        end
    end
    start
    end
end
start
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
        line = text[i]
        if start_re.match(line):
            indent = len(tabs.findall(line))
            # indents = [(j, len(tabs.findall(line2))) for j, line2 in enumerate(text[i:]) if len(tabs.findall(line2)) < indent or end_re.match(line2)]
            for j, line2 in enumerate(text[i:]):
                new_indent = len(tabs.findall(line2))
                if new_indent < indent or end_re.match(line2):
                    Block(parent=root, start=i, end=j, indent=indent, text="\n".join(text[i:j]))
                    i = j + 1
                    break
        i += 1
    return root


root = detect(sample2)
blocks = [c.text for c in root.children]
for b in blocks:
    print(b)
