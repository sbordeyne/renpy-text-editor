class ConsoleHistory:
    def __init__(self, length=None):
        self.history = []
        self.history_args = []
        self.index = 0
        self.max_index = -1
        self.length = length

    def push(self, command, args=None):
        if self.length is not None and self.max_index == self.length:
            self.history.pop(0)
            self.history_args.pop(0)
        self.history.append(command)
        self.history_args.append(args)
        self.max_index = len(self.history)
        self.index = self.max_index
        assert (len(self.history) == len(self.history_args)), "Histories have two different lengths"

    def pop(self):
        if 0 <= self.index < self.max_index:
            return self.history[self.index], self.history_args[self.index]

    def pop_str(self):
        if 0 <= self.index < self.max_index:
            return self.history[self.index] + " ".join(self.history_args[self.index])
        else:
            return ""

    def rollback(self):
        self.index = max(0, self.index - 1)

    def rollforward(self):
        self.index += 1
