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

# Currently implemented features

- [x] Editor View with Line numbering
- [x] Theme Support
- [x] Snippets Support
- [x] Duplicate line/ Selected Code Block
- [x] Fully Portable
- [x] Project Viewer, with Picture, and audio player.
- [x] Support for MD, JSON, YAML, XML markdown
- [x] Closeable tabs for multiple files open at the same time.
- [x] Layeredimage builder and preview
- [x] Syntax highlighting
- [x] Main window view, with 2 resizable frames for text editing.
- [x] opening a file from the project manager
- [x] Sort the project manager by item type (folder/file)
- [x] Save files
- [x] Undo/Redo
- [x] Formatting text (upper, lower, capitalize etc)
- [x] Comparing between two files
- [x] Toolbar
- [x] Snippets support
- [x] Translation support
- [x] GUI for adding in snippets
- [x] Collapsing blocks of code
    - [x] collapsing with "#region region-name" and "#endregion" comments
    - [x] collapsing labels, screens, python, init, statements and functions
- [x] Reassign Keybindings how you see fit, including support for F13-F24 keys.
- [x] GUI for setting up your preferences
- [x] Indent/Deindent code with tab/shift+tab
- [x] Full-featured renpy debugger (courtesy of @Enerccio) including breakpoints, pause, line-by-line execution.

# Planned Features


- [ ] Tab Autocompletion
- [ ] Variable viewer
- [ ] Renpy Console (run renpy code headless, jump to labels to test, call screens etc)
- [ ] Automatic Renpy markdown matching, with automatic detection of custom text tags ({b}, {u} etc tags)
- [ ] Autocompletion of variables in text
- [ ] Plugin support
- [ ] Automatic Indent
- [ ] Built-in linting line by line with PEP8 support, and Renpy's linting system
    - [ ] pycodestyle linting
    - [ ] renpy linting
- [ ] Git integration
- [ ] Save file viewer
- [ ] Screen builder and preview
- [ ] Visual scripting for Renpy Visual Novels (VSVN)
- [ ] Search, Replace, and Search in all files with regular expression support.
- [ ] Built-in inline boolean expression simplifier
- [ ] Boolean expression builder with variable names, and a truth table for those really complex conditions.

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

- [x] Duplicate line/selected block : Ctrl+D
- [ ] Run selected file in the console : F5
- [x] Quit : Alt+F4
- [ ] Close current file : Ctrl+W
- [ ] Comment/Uncomment selected block/line : Ctrl+Q
- [ ] Search : Ctrl+F
- [ ] Search & Replace : Ctrl+H
- [ ] Search & replace in all files : Ctrl+Shift+F
- [ ] Copy : Ctrl+C
- [ ] Paste : Ctrl+V
- [ ] Cut : Ctrl+X
- [x] Save : Ctrl+S
- [x] Save As : Ctrl+Shift+S
- [x] To lowercase : Ctrl+U
- [x] To UPPERCASE : Ctrl+Shift+U
- [x] To Capitalized case : Ctrl+Alt+U
- [x] Invert casing : Ctrl+Shift+Alt+U
- [x] Undo : Ctrl+Z
- [x] Redo : Ctrl+Y
