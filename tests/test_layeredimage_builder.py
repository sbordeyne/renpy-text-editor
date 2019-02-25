import setup_tests
import tkinter as tk
from RTE.views.layeredimage_builder import LayeredImageBuilderGUI

if __name__ == "__main__":
    root = tk.Tk()
    gui = LayeredImageBuilderGUI(root)
    gui.pack(side="top", fill="both", expand=True)
    root.mainloop()
