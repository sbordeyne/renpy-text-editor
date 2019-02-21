import tkinter as tk
from RTE.views import EditorFrame

if __name__ == "__main__":
    root = tk.Tk()
    EditorFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
