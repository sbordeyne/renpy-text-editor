def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)

def get_type_by_extension(extension):
    if isinstance(extension, str):
        extension = extension.lower()
    if extension is None or extension == "folder":
        return "directory"
    elif extension in ("png", "jpg", "image"):
        return "image"
    elif extension in ("webm", "mp4", "avi", "movie"):
        return "movie"
    elif extension in ("mp3", "wav", "music"):
        return "music"
    else:
        return "text"
