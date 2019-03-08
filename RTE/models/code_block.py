import re


class Block:
    tabs_re = re.compile(r'( {4})')
    start_re = re.compile(r'(elif|else|except|finally|for|if|try|while|with|label|screen|transform|init|layeredimage|menu|style|# *region|class) ?\w*\b')
    end_re = re.compile(r'(\n|break|continue|return|yield|yield from|pass|# *endregion) ?\w*\b')

    def __init__(self, parent=None, start=0, end=0, indent=0):
        self.children = []
        self.parent = parent
        self.start = start
        self.end = end
        self.indent = indent
        self.collapsed = False

    def get(self, text):
        return '\n'.join(text.split("\n")[self.start:self.end])

    def detect(self, text):
        start_indices = []
        end_indices = []
        for line_nb, line in enumerate(self.get(text).split("\n")):
            indent = len(self.tabs_re.findall(line))
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
