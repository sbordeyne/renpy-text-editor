import tkinter as tk
from RTE.config import config


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
