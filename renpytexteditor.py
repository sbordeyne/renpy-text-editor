from RTE.views.main import RenpyTextEditorGUI
import tkinter as tk
from RTE.assets import AssetStore
from RTE.config import config

def main():
    root = tk.Tk()
    root.geometry(config.geometry)
    #root.iconbitmap(AssetStore.folder())
    view = RenpyTextEditorGUI(root)
    view.pack()
    view.add_tab("left")
    view.add_tab("right")
    root.mainloop()


if __name__ == '__main__':
    main()
