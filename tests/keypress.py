import tkinter as tk

wn = tk.Tk()
wn.title('KeyDetect')


def down(e):
    print('Down\n', e.char, '\n', e)


def up(e):
    print('Up\n', e.char, '\n', e)


wn.bind('<KeyPress>', down)
wn.bind('<KeyRelease>', up)

wn.mainloop()
