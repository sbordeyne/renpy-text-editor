# renpy-text-editor
Renpy Text Editor - A dedicated text editor and IDE for the Ren'Py Engine.

[Discord Server](https://discord.gg/aHk5kur)

# Installation instructions

In order to use this software, you must have the following installed on your computer :

- A python 3.6.5+ installation
- pip
- Tcl/Tk 8.5+ (should be included in any python release)

Run the following command in a terminal

`pip install -r requirements.txt --upgrade`

Then, run the renpytexteditor.py file in any python 3.6.5+ interpretor.

`python3 -m renpytexteditor.py`


# Contributing

Contributions should be done via pull requests (PR). If you have a feature to add to the software, whether it's a planned feature or not, please fork this repository and open up a PR with your changes. This will be reviewed, and integrated if applicable.

All code in this repository adheres to the PEP8 styling guide as much as possible, except for the line length guideline, although it is mostly kept under 80 characters long, sometimes, it is unavoidable. Code shall be linted with the pycodestyle linter and the following ignore flags : `E501, W142, W191, E303, E302, W293`.

All code in this repository should be MVC oriented (Model-View-Controller). The entry point is in the RTE.views.main subpackage.

# Planned Features

- [x] Editor View with Line numbering
- [x] RenPy Syntax Highlighting
- [x] Theme Support
- [x] Snippets Support
- [x] Duplicate line/ Selected Code Block
- [ ] Tab Autocompletion
- [ ] Variable viewer
- [ ] Renpy Console (run renpy code headless, jump to labels to test, call screens etc)
- [ ] Automatic Renpy markdown matching, with automatic detection of custom text tags ({b}, {u} etc tags)
- [ ] Autocompletion of variables in text
- [x] Multiple Views with resizable frames
- [x] Fully Portable
- [x] Project Viewer, with Picture, and audio player.
- [ ] Plugin support
- [ ] Automatic Indent
- [ ] Built-in linting line by line with PEP8 support, and Renpy's linting system
- [ ] Git integration
- [x] Support for MD, JSON, YAML, XML markdown
- [ ] Save file viewer
- [x] Layeredimage builder and preview
- [ ] Screen builder and preview
- [x] Tabs for multiple files open at the same time.
- [ ] Collapsing blocks of code
    - [ ] collapsing with "#region region-name" and "#endregion" comments
    - [ ] collapsing labels, screens, python, init, statements and functions
- [ ] Visual scripting for Renpy Visual Novels (VSVN)
- [ ] Reassign Keybindings how you see fit, including support for F13-F24 keys.
- [ ] Search, Replace, and Search in all files with regular expression support.

## LayeredImage Builder Feature

- [ ] Support for any number of layers with easy photoshop-like layer window
- [ ] Support for basic transforms:
    - [x] rotate
    - [x] zoom
    - [x] xoffset, yoffset
    - [x] crop
- [x] View a layered image from the builder

## Screen Builder Feature

- [ ] Preview the resulting screen
- [ ] Supported screen displayables :
    - [ ] imagebutton
    - [ ] textbutton
    - [ ] frame
    - [ ] viewport
    - [ ] add
    - [ ] use
- [ ] support for conditions
- [ ] in-depth actions builder with support for any screen action && User-defined actions
- [ ] output in a new screen.rpy file, with proper formatting.

## Available Keybindings

- [ ] Duplicate line/selected block : Ctrl+D
- [ ] Run selected file in the console : F5
- [ ] Quit : Alt+F4
- [ ] Close current file : Ctrl+W
- [ ] Comment/Uncomment selected block/line : Ctrl+Q
- [ ] Search : Ctrl+F
- [ ] Search & Replace : Ctrl+H
- [ ] Search & replace in all files : Ctrl+Shift+F
- [ ] Copy : Ctrl+C
- [ ] Paste : Ctrl+V
- [ ] Cut : Ctrl+X
- [ ] Save : Ctrl+S
- [ ] Save As : Ctrl+Shift+S
- [ ] To lowercase : Ctrl+U
- [ ] To UPPERCASE : Ctrl+Shift+U
- [ ] To Capitalized case : Ctrl+Alt+U
- [ ] Invert casing : Ctrl+Shift+Alt+U
- [x] Undo : Ctrl+Z
- [x] Redo : Ctrl+Y

# To do list :

- [x] Syntax highlighting
- [x] Main window view, with 2 resizable frames for text editing.
- [x] Project manager view
- [x] Theme support
- [x] opening a file from the project manager
- [x] Sort the project manager by item type (folder/file)
- [ ] Improve the lexer for the RenPy language
    - [x] Lexing screen language
    - [ ] Lexing screen language attributes
    - [ ] Lexing the $ sign for inline python
    - [x] Adding new Renpy token type
    - [ ] lexing transform/atl language
    - [x] lexing renpy keywords
    - [ ] lexing style attributes
    - [ ] lexing renpy built-in functions
- [x] Save files
- [ ] Handle keyboard input / changing the Keybindings
- [x] Adding in the Options window.
- [x] Integrate picture viewer into project manager / Implement music (sound) player.
- [x] Make tabs closeable
- [ ] Resizing window support + saving in the config file for later restoration.
- [x] Undo/Redo
- [x] Duplicate line & formatting text (upper, lower, capitalize etc)
- [x] Comparing between two files
- [x] Toolbar
- [x] favicon asset
- [x] open/collapse assets
- [ ] Tooltips
    - [x] Create Tooltip class
    - [ ] add tooltips to buttons
- [x] Snippets support
- [ ] GUI for adding in snippets
