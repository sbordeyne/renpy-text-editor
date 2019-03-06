import tkinter as tk

class AssetStore:
    @classmethod
    def get_icon_by_extension(cls, extension):
        if isinstance(extension, str):
            extension = extension.lower()
        if extension is None or extension == "folder":
            return cls.folder()
        elif extension in ("png", "jpg", "image"):
            return cls.image()
        elif extension in ("webm", "mp4", "avi", "movie"):
            return cls.movie()
        elif extension in ("mp3", "wav", "opus", "music"):
            return cls.music()
        else:
            return cls.text()

    @classmethod
    def folder(cls):
        return tk.BitmapImage("@assets/folder.xbm")

    @classmethod
    def image(cls):
        return tk.BitmapImage("@assets/imagefile.xbm")

    @classmethod
    def movie(cls):
        return tk.BitmapImage("@assets/moviefile.xbm")

    @classmethod
    def music(cls):
        return tk.BitmapImage("@assets/musicfile.xbm")

    @classmethod
    def text(cls):
        return tk.BitmapImage("@assets/textfile.xbm")
