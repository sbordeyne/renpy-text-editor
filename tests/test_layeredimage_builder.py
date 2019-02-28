import setup_tests
import os
import tkinter as tk
from RTE.views.layeredimage_builder import LayeredImageBuilderGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Layered Image Builder")
    gui = LayeredImageBuilderGUI(root)
    gui.pack(side="top", fill="both", expand=True)
    root.mainloop()

# os.system('xset r on')
