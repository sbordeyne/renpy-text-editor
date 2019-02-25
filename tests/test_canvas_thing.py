import tkinter as tk
import tkinter.filedialog as filedialog

root = tk.Tk()
can = tk.Canvas(root, width=1024, height=768)
can.pack(expand=True, fill=tk.BOTH)
im = tk.PhotoImage(file=filedialog.askopenfilename())
img = can.create_image(0, 0, image=im, anchor="nw")
root.mainloop()
