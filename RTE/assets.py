import tkinter as tk

class AssetStore:
    loaded_assets = []

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
        asset = tk.BitmapImage("@assets/folder.xbm")
        cls.loaded_assets.append(asset)
        return AssetStore.loaded_assets[-1]

    @classmethod
    def image(cls):
        asset = tk.BitmapImage("@assets/imagefile.xbm")
        cls.loaded_assets.append(asset)
        return AssetStore.loaded_assets[-1]

    @classmethod
    def movie(cls):
        asset = tk.BitmapImage("@assets/moviefile.xbm")
        cls.loaded_assets.append(asset)
        return AssetStore.loaded_assets[-1]

    @classmethod
    def music(cls):
        asset = tk.BitmapImage("@assets/musicfile.xbm")
        cls.loaded_assets.append(asset)
        return AssetStore.loaded_assets[-1]

    @classmethod
    def text(cls):
        asset = tk.BitmapImage("@assets/textfile.xbm")
        cls.loaded_assets.append(asset)
        return AssetStore.loaded_assets[-1]
