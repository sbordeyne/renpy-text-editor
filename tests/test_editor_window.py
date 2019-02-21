import tkinter as tk
from RTE.views import EditorFrame

if __name__ == "__main__":
    root = tk.Tk()
    gui = EditorFrame(root)
    gui.pack(side="top", fill="both", expand=True)
    gui.text.insert("end", "one\ntwo\nthree\n")
    gui.text.insert("end", "four\n", ("bigfont",))
    gui.text.insert("end", "five\n")
    root.mainloop()
