import os
from RTE.assets import AssetStore

config_file_path = os.path.join(os.getcwd(), "config", "config.json")
keybindings_file_path = os.path.join(os.getcwd(), "config", "keybindings.json")
theme_folder_path = os.path.join(os.getcwd(), "themes")
assets = AssetStore()
