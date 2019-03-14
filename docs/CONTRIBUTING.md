# Contributing

Contributions should be done via pull requests (PR). If you have a feature to add to the software, whether it's a planned feature or not, please fork this repository and open up a PR with your changes. This will be reviewed, and integrated if applicable.

All code in this repository adheres to the PEP8 styling guide as much as possible, except for the line length guideline, although it is mostly kept under 80 characters long, sometimes, it is unavoidable. Code shall be linted with the pycodestyle linter and the following ignore flags : `E501, W142, W191, E303, E302, W293`.

All code in this repository should be MVC oriented (Model-View-Controller). The entry point is in the RTE.views.main subpackage.

# Translating

The RenPy Text Editor supports translations. In order to translate the software, you must provide a `<locale>.json` file which will set up a dictionnary. The keys to this dictionnary are the sentences in english to translate, the value for that key must be a single string, if possible of similar length, which will be displayed instead of the english string.

If keys are missing from the translation file, then the default english strings will be used.

# Creating themes

Themes for the renpy text editor are just json files which will apply custom colors/font styles to particular UI elements. Themes are also responsible of the syntax highlighting.

## Theme Creation

Themes are stored in JSON format. To create a theme, you must provide a json file with a dictionnary in it. That dictionnary should define the keys :

- ui : for everything UI related (text background color, etc)
- tokens : for syntax highlighting. The tokens used are the token names from the pygments python library.

Please see the monokai.json file for an example.

### Available Attributes

#### For text tags (syntax highlighting)

- background (color)
    The background color to use for text having this tag.

- bgstipple (bitmap)
    The name of a bitmap which is used as a stipple brush when drawing the background. Typical values are “gray12”, “gray25”, “gray50”, or “gray75”. Default is a solid brush (no bitmap).

- borderwidth (distance)
    The width of the text border. The default is 0 (no border).

- fgstipple (bitmap)
    The name of a bitmap which is used as a stipple brush when drawing the text. Typical values are “gray12”, “gray25”, “gray50”, or “gray75”. Default is a solid brush (no bitmap).

- font (font)
    The font to use for text having this tag.

- foreground (color)
    The color to use for text having this tag.

- justify (constant)
    Controls text justification (the first character on a line determines how to justify the whole line). Use one of LEFT, RIGHT, or CENTER. Default is LEFT.

- lmargin1 (distance)
    The left margin to use for the first line in a block of text having this tag. Default is 0 (no left margin).

- lmargin2 (distance)
    The left margin to use for every line but the first in a block of text having this tag. Default is 0 (no left margin).

- offset (distance)
    Controls if the text should be offset from the baseline. Use a positive value for superscripts, a negative value for subscripts. Default is 0 (no offset).

- overstrike (flag)
    If non-zero, the text widget draws a line over the text that has this tag. For best results, you should use overstrike fonts instead.

- relief (constant)
    The border style to use for text having this tag. Use one of SUNKEN, RAISED, GROOVE, RIDGE, or FLAT. Default is FLAT (no border).

- rmargin (distance)
    The right margin to use for blocks of text having this tag. Default is 0 (no right margin).

- spacing1 (distance)
    Spacing to use above the first line in a block of text having this tag. Default is 0 (no extra spacing).

- spacing2 (distance)
    Spacing to use between the lines in a block of text having this tag. Default is 0 (no extra spacing).

- spacing3 (distance)
    Spacing to use after the last line of text in a block of text having this tag. Default is 0 (no extra spacing).

- underline (flag)
    If non-zero, the text widget underlines the text that has this tag. For example, you can get the standard hyperlink look with (foreground=”blue”, underline=1). For best results, you should use underlined fonts instead.

- wrap (constant)
    The word wrap mode to use for text having this tag. Use one of NONE, CHAR, or WORD.

#### For the UI

TODO (check the tkinter config options on effbot.org for the widget to change)

## Theme Installation

Themes are installed by dropping the appropriate JSON theme file in the themes/ folder. The file name will be used to determine the theme name. Authorized characters are "[A-z]-_"

