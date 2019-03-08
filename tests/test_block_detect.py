import re


class Block:
    tabs = re.compile(r'( {4})')
    start = re.compile(r'(elif|else|except|finally|for|if|try|while|with|label|screen|transform|init|layeredimage|menu|style|# *region) *:?\b')
    end = re.compile(r'(\n|break|continue|return|yield|yield from|pass|# *endregion) *:?\b')

    def __init__(self, parent=None, start=0, end=0, indent=0):
        self.children = []
        self.parent = parent
        self.start = start
        self.end = end
        self.indent = indent

    def get(self, text):
        return '\n'.join(text.split("\n")[self.start:self.end])

    def detect(self, text):
        start_indices = []
        end_indices = []
        for line_nb, line in enumerate(self.get(text).split("\n")):
            indent = len(self.tabs.findall(line))
            if indent > self.indent + 1:
                continue
            if self.start.match(line):
                start_indices.append((line_nb, indent))
            elif self.end.match(line):
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

tabs = re.compile(r'( {4})')

expected = [(1, 8), (2, 5), (3, 4), (6, 7), (9, 10)]

def detect_block(text):
    start_indices = []
    end_indices = []
    rv = []
    for line_nb, line in enumerate(text.split("\n")):
        indent = len(tabs.findall(line))
        if "start" in line:
            start_indices.append((line_nb, indent))
        elif "end" in line:
            end_indices.append((line_nb, indent))
    for i, (idx, idx_indent) in enumerate(start_indices):
        for jdx, jdx_indent in end_indices:
            if jdx_indent == idx_indent and jdx > idx:
                rv.append((idx, jdx))
                break
    return rv


root = Block()
root.detect_all(sample)
