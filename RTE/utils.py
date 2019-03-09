import tkinter as tk
from RTE.config import config


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # miliseconds
        self.wraplength = 180   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)

def get_type_by_extension(extension):
    """
        Returns a file type (folder, image, text, movie, music)
        based on the extension provided

        get_type_by_extension(extension:str) -> str
    """

    if isinstance(extension, str):
        extension = extension.lower()
    if extension is None or extension == "folder":
        return "directory"
    elif extension in ("png", "jpg", "image"):
        return "image"
    elif extension in ("webm", "mp4", "avi", "movie"):
        return "movie"
    elif extension in ("mp3", "wav", "opus", "music"):
        return "music"
    elif extension in ("rpy", 'py', 'txt', 'json', 'xml', 'md', 'rst',
                       'yaml', 'yml', 'html', 'css', 'js', ''):
        return "text"

def text_get_selected(text):
    if text.tag_ranges("sel"):
        return text.get(tk.SEL_FIRST, tk.SEL_LAST)
    else:
        return ""

def tr(text):
    return config.get_locale().translate(text)
