from RTE.views.main import RenpyTextEditorGUI
import tkinter as tk


def main():
    root = tk.Tk()
    view = RenpyTextEditorGUI(root)
    view.pack()
    view.add_tab()
    view.add_tab("right")
    root.mainloop()


if __name__ == '__main__':
    main()
