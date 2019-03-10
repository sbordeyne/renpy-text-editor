# -*- coding: utf-8 -*-
"""
    RTE.syntaxhighlight.lexer
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for RenPy
    Based on the Python Lexer from the Pygments team.
"""

import re

from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, \
    default, words, combined, do_insertions
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic, Other
from .tokens import Renpy, Block

__all__ = ['RenpyLexer', 'RenpyConsoleLexer', 'RenpyTracebackLexer']

line_re = re.compile('.*?\n')


class RenpyBlockLexer(RegexLexer):
    name = "RenpyBlock"
    aliases = ["renpyblock"]

    tokens = {
        'root': [
            (r'[a-zA-Z_]\w*', Name),
            (words((
                'elif', 'else', 'except', 'finally', 'for', 'if',
                'try', 'while', 'with', 'label', 'screen', 'transform',
                'init', 'layeredimage', 'menu', 'style'), suffix=r'\b'),
             Block.Start),
            (r'# *region\b', Block.Start),
            (r'# *endregion\b', Block.End),
            (words((
                '\n\n', 'break', 'continue', 'return', 'yield', 'yield from',
                'pass', '# *endregion'), suffix=r'\b'),
             Block.End),
        ],
    }


class RenpyLexer(RegexLexer):
    """
    For `Renpy <http://www.renpy.org>`_ source code.
    """

    name = 'Renpy'
    aliases = ['renpy', 'rpy']
    filenames = ['*.rpy']

    def innerstring_rules(ttype):
        return [
            # the old style '%s' % (...) string formatting
            (r'%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?'
             '[hlL]?[E-GXc-giorsux%]', String.Interpol),
            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"%\n]+', ttype),
            (r'[\'"\\]', ttype),
            # unhandled string formatting sign
            (r'%', ttype),
            # newlines are an error (use "nl" state)
        ]

    tokens = {
        'root': [
            (r'\n', Text),
            include('screen_lang'),
            (r'^ *\$', Renpy.Python.Inline),
            (r'((renpy|im)\.[a-zA-Z_]+)\(([a-zA-Z_ ,=]+)\)',
             bygroups(Renpy.Function.Builtin, Renpy.Function.Arguments)),
            include("screen_actions"),
            (r'\$', String.Symbol),
            (r'^(\s*)([rRuUbB]{,2})("""(?:.|\n)*?""")',
             bygroups(Text, String.Affix, String.Doc)),
            (r"^(\s*)([rRuUbB]{,2})('''(?:.|\n)*?''')",
             bygroups(Text, String.Affix, String.Doc)),
            (r'[^\S\n]+', Text),
            (r'\A#!.+$', Comment.Hashbang),
            (r'#.*$', Comment.Single),
            (r'[]{}:(),;[]', Punctuation),
            (r'\\\n', Text),
            (r'\\', Text),
            (r'(in|is|and|or|not)\b', Operator.Word),
            (r'!=|==|<<|>>|[-~+/*%=<>&^|.]', Operator),
            include('keywords'),
            include('special_labels'),
            (r'(def)((?:\s|\\\s)+)', bygroups(Keyword, Text), 'funcname'),
            (r'(class)((?:\s|\\\s)+)', bygroups(Keyword, Text), 'classname'),
            (r'(from)((?:\s|\\\s)+)', bygroups(Keyword.Namespace, Text),
             'fromimport'),
            (r'(import)((?:\s|\\\s)+)', bygroups(Keyword.Namespace, Text),
             'import'),
            include('builtins'),
            include('magicfuncs'),
            include('magicvars'),
            include('backtick'),
            ('([rR]|[uUbB][rR]|[rR][uUbB])(""")',
             bygroups(String.Affix, String.Double), 'tdqs'),
            ("([rR]|[uUbB][rR]|[rR][uUbB])(''')",
             bygroups(String.Affix, String.Single), 'tsqs'),
            ('([rR]|[uUbB][rR]|[rR][uUbB])(")',
             bygroups(String.Affix, String.Double), 'dqs'),
            ("([rR]|[uUbB][rR]|[rR][uUbB])(')",
             bygroups(String.Affix, String.Single), 'sqs'),
            ('([uUbB]?)(""")', bygroups(String.Affix, String.Double),
             combined('stringescape', 'tdqs')),
            ("([uUbB]?)(''')", bygroups(String.Affix, String.Single),
             combined('stringescape', 'tsqs')),
            ('([uUbB]?)(")', bygroups(String.Affix, String.Double),
             combined('stringescape', 'dqs')),
            ("([uUbB]?)(')", bygroups(String.Affix, String.Single),
             combined('stringescape', 'sqs')),
            include('name'),
            include('numbers'),
        ],
        'keywords': [
            (words((
                'assert', 'break', 'continue', 'del', 'elif', 'else', 'except',
                'exec', 'finally', 'for', 'global', 'if', 'lambda', 'pass',
                'print', 'raise', 'return', 'try', 'while', 'yield',
                'yield from', 'as', 'with'), suffix=r'\b'),
             Keyword),
            (words((
                'audio', 'scene', 'expression', 'play', 'queue', 'stop',
                'python', 'init', 'pause', 'jump', 'call', 'zorder',
                'show', 'hide', 'at', 'music', 'sound', 'voice',
            ), suffix=r'\b'), Renpy.Reserved),
            (words((
                'default', 'define', 'layeredimage', 'screen', 'transform',
                'label', 'menu', 'style', 'image'), suffix=r'\b'),
             Renpy.Declaration),
        ],
        'special_labels': [
            (words(('start', 'quit', 'after_load', 'splashscreen',
                    'before_main_menu', 'main_menu', 'after_warp',
                    ), prefix=r"label ", suffix=r'\b'), Renpy.Label.Reserved),
        ],
        'screen_lang': [
            (words(('add', 'bar', 'button', 'fixed', 'frame', 'grid',
                    'hbox', 'imagebutton', 'input', 'key',
                    'mousearea', 'null', 'side', 'text', 'textbutton',
                    'timer', 'vbar', 'vbox', 'viewport',
                    'vpgrid', 'window', 'imagemap', 'hotspot',
                    'hotbar', 'drag', 'draggroup', 'has', 'on', 'use',
                    'transclude', 'transform', 'label',
                    ), prefix=r'\s+', suffix=r'\b'), Renpy.Screen.Displayables),
        ],
        'properties': [  # renpy/tutorial/game/keywords.py
            # [u'(?:insensitive|keysym|layer|length|min_overlap|modal|mouse_drop|mousewheel|
            # pagekeys|pixel_width|predict|prefix|properties|range|repeat|rows|scope|scrollbars|
            # selected|selected_hover|selected_idle|selected_insensitive|sensitive|slow|slow_done|
            # pacing|style|style_group|style_prefix|style_suffix|substitute|suffix|text_style|
            # transpose|unhovered|value|variant|width|xadjustment|xinitial|yadjustment|yinitial|
            # zorder)', '(?:|activate_|hover_|idle_|insensitive_|selected_|selected_activate_|
            # selected_hover_|selected_idle_|selected_insensitive_)(?:additive|adjust_spacing
            # |align|alignaround|alpha|alt|anchor|angle|antialias|area|around|background|
            # bar_invert|bar_resizing|bar_vertical|base_bar|black_color|bold|bottom_bar|
            # bottom_gutter|bottom_margin|bottom_padding|box_layout|box_reverse|box_wrap|
            # box_wrap_spacing|caret|child|clipping|color|corner1|corner2|crop|crop_relative|
            # debug|delay|drop_shadow|drop_shadow_color|events|first_indent|first_spacing|
            # fit_first|focus_mask|font|foreground|hinting|hyperlink_functions|italic|
            # justify|kerning|key_events|keyboard_focus|language|layout|left_bar|left_gutter|
            # left_margin|left_padding|line_leading|line_spacing|margin|maximum|maxsize|min_width|
            # minimum|minwidth|mouse|nearest|newline_indent|offset|order_reverse|outline_scaling|
            # outlines|padding|pos|radius|rest_indent|right_bar|right_gutter|right_margin|
            # right_padding|rotate|rotate_pad|ruby_style|size|size_group|slow_abortable|
            # slow_cps|slow_cps_multiplier|sound|spacing|strikethrough|subpixel|text_align|
            # text_y_fudge|thumb|thumb_offset|thumb_shadow|tooltip|top_bar|top_gutter|top_margin|
            # top_padding|transform_anchor|underline|unscrollable|vertical|xalign|xanchor|
            # xanchoraround|xaround|xcenter|xfill|xfit|xmargin|xmaximum|xminimum|xoffset|xpadding|
            # xpan|xpos|xsize|xspacing|xtile|xysize|xzoom|yalign|yanchor|yanchoraround|yaround|
            # ycenter|yfill|yfit|ymargin|ymaximum|yminimum|yoffset|ypadding|ypan|ypos|ysize|
            # yspacing|ytile|yzoom|zoom)', '(?:vscrollbar_|scrollbar_)(?:|activate_|hover_|
            # idle_|insensitive_|selected_|selected_activate_|selected_hover_|selected_idle_|
            # selected_insensitive_)(?:align|alt|anchor|area|bar_invert|bar_resizing|bar_vertical|
            # base_bar|bottom_bar|bottom_gutter|clipping|debug|keyboard_focus|left_bar|left_gutter|
            # maximum|mouse|offset|pos|right_bar|right_gutter|thumb|thumb_offset|thumb_shadow|
            # tooltip|top_bar|top_gutter|unscrollable|xalign|xanchor|xcenter|xfill|xmaximum|
            # xoffset|xpos|xsize|xysize|yalign|yanchor|ycenter|yfill|ymaximum|yoffset|ypos|
            # ysize)', 'side_(?:|activate_|hover_|idle_|insensitive_|selected_|selected_activate_|
            # selected_hover_|selected_idle_|selected_insensitive_)(?:align|alt|anchor|area|clipping|
            # debug|maximum|offset|pos|spacing|tooltip|xalign|xanchor|xcenter|xfill|xmaximum|
            # xoffset|xpos|xsize|xysize|yalign|yanchor|ycenter|yfill|ymaximum|yoffset|ypos|
            # ysize)', 'text_(?:|activate_|hover_|idle_|insensitive_|selected_|selected_activate_|
            # selected_hover_|selected_idle_|selected_insensitive_)(?:adjust_spacing|align|alt|
            # anchor|antialias|area|black_color|bold|clipping|color|debug|drop_shadow|
            # drop_shadow_color|first_indent|font|hinting|hyperlink_functions|italic|justify|
            # kerning|language|layout|line_leading|line_spacing|maximum|min_width|minimum|minwidth|
            # newline_indent|offset|outline_scaling|outlines|pos|rest_indent|ruby_style|size|
            # slow_abortable|slow_cps|slow_cps_multiplier|strikethrough|text_align|text_y_fudge|
            # tooltip|underline|vertical|xalign|xanchor|xcenter|xfill|xmaximum|xminimum|xoffset|
            # xpos|xsize|xysize|yalign|yanchor|ycenter|yfill|ymaximum|yminimum|yoffset|ypos|
            # ysize)', 'viewport_(?:|activate_|hover_|idle_|insensitive_|selected_|
            # selected_activate_|selected_hover_|selected_idle_|selected_insensitive_)(?:align
            # |alt|anchor|area|clipping|debug|maximum|offset|pos|tooltip|xalign|xanchor|xcenter
            # |xfill|xmaximum|xoffset|xpos|xsize|xysize|yalign|yanchor|ycenter|yfill|ymaximum|
            # yoffset|ypos|ysize)']
            (words(("action", "activate_sound", "activated", "adjustment", "allow",
                    "alpha", "alternate", "alternate_keysym", "arguments", "arrowkeys",
                    "at", "auto", "cache", "caption", "changed", "child_size",
                    "clicked", "cols", "copypaste", "default", "drag_handle", "drag_joined",
                    "drag_name", "drag_offscreen", "drag_raise", "draggable", "dragged",
                    "drop_allowable", "droppable", "dropped", "edgescroll",
                    "exclude", "focus", "focus_mask", "ground", "height", "hover",
                    "hovered", "id", "idle", "image_style"), prefix=r"( {4}){2,}", suffix=r"\b"), Renpy.Properties)
        ],
        "screen_actions": [
            (words(("Call", "Hide", "Jump", "NullAction", "Return", "Show",
                    "ShowTransient", "ToggleScreen", "AddToSet", "RemoveFromSet",
                    "SetDict", "SetField", "SetLocalVariable", "SetScreenVariable",
                    "SetVariable", "ToggleDict", "ToggleField", "ToggleLocalVariable",
                    "ToggleScreenVariable", "ToggleSetMembership", "ToggleVariable",
                    "MainMenu", "Quit", "ShowMenu", "Start", "FileAction",
                    "FileDelete", "FileLoad", "FilePage", "FilePageNext",
                    "FileSave", "FileTakeScreenshot", "QuickLoad",
                    "QuickSave", "PauseAudio", "Play", "Queue", "SetMixer",
                    "SetMute", "Stop", "ToggleMute", "Confirm", "DisableAllInputValues",
                    "Function", "Help", "HideInterface", "If", "InvertSelected",
                    "MouseMove", "Notify", "OpenURL", "QueueEvent", "RestartStatement",
                    "RollForward", "Rollback", "RollbackToIdentifier",
                    "Screenshot", "Scroll", "SelectedIf", "SensitiveIf", "Skip",
                    "With", "AnimatedValue", "AudioPositionValue", "DictValue",
                    "FieldValue", "MixerValue", "ScreenVariableValue", "StaticValue",
                    "VariableValue", "XScrollValue", "YScrollValue", "DictInputValue",
                    "FieldInputValue", "FilePageNameInputValue", "ScreenVariableInputValue",
                    "VariableInputValue", "Preference", "GamepadCalibrate", "GamepadExists",
                    "FileCurrentPage", "FileCurrentScreenshot", "FileJson", "FileLoadable",
                    "FileNewest", "FilePageName", "FileSaveName", "FileScreenshot", "FileSlotName",
                    "FileTime", "FileUsedSlot", "SideImage", "GetTooltip"), prefix=r' ', suffix=r"\b"), Renpy.Screen.Actions)
        ],
        'builtins': [
            (words((
                '__import__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin',
                'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod',
                'cmp', 'coerce', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod',
                'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float',
                'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
                'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len',
                'list', 'locals', 'long', 'map', 'max', 'min', 'next', 'object',
                'oct', 'open', 'ord', 'pow', 'property', 'range', 'raw_input', 'reduce',
                'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
                'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
                'unichr', 'unicode', 'vars', 'xrange', 'zip'),
                prefix=r'(?<!\.)', suffix=r'\b'),
             Name.Builtin),
            (r'(?<!\.)(self|None|Ellipsis|NotImplemented|False|True|cls'
             r')\b', Name.Builtin.Pseudo),
            (words((
                'ArithmeticError', 'AssertionError', 'AttributeError',
                'BaseException', 'DeprecationWarning', 'EOFError', 'EnvironmentError',
                'Exception', 'FloatingPointError', 'FutureWarning', 'GeneratorExit',
                'IOError', 'ImportError', 'ImportWarning', 'IndentationError',
                'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError',
                'MemoryError', 'ModuleNotFoundError', 'NameError', 'NotImplemented', 'NotImplementedError',
                'OSError', 'OverflowError', 'OverflowWarning', 'PendingDeprecationWarning',
                'RecursionError', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError',
                'StopIteration', 'StopAsyncIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
                'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError',
                'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError',
                'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
                'ValueError', 'VMSError', 'Warning', 'WindowsError',
                'ZeroDivisionError'), prefix=r'(?<!\.)', suffix=r'\b'),
             Name.Exception),
        ],
        'magicfuncs': [
            (words((
                '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
                '__complex__', '__contains__', '__del__', '__delattr__', '__delete__',
                '__delitem__', '__delslice__', '__div__', '__divmod__', '__enter__',
                '__eq__', '__exit__', '__float__', '__floordiv__', '__ge__', '__get__',
                '__getattr__', '__getattribute__', '__getitem__', '__getslice__', '__gt__',
                '__hash__', '__hex__', '__iadd__', '__iand__', '__idiv__', '__ifloordiv__',
                '__ilshift__', '__imod__', '__imul__', '__index__', '__init__',
                '__instancecheck__', '__int__', '__invert__', '__iop__', '__ior__',
                '__ipow__', '__irshift__', '__isub__', '__iter__', '__itruediv__',
                '__ixor__', '__le__', '__len__', '__long__', '__lshift__', '__lt__',
                '__missing__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__',
                '__nonzero__', '__oct__', '__op__', '__or__', '__pos__', '__pow__',
                '__radd__', '__rand__', '__rcmp__', '__rdiv__', '__rdivmod__', '__repr__',
                '__reversed__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__',
                '__rop__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
                '__rtruediv__', '__rxor__', '__set__', '__setattr__', '__setitem__',
                '__setslice__', '__str__', '__sub__', '__subclasscheck__', '__truediv__',
                '__unicode__', '__xor__'), suffix=r'\b'),
             Name.Function.Magic),
        ],
        'magicvars': [
            (words((
                '__bases__', '__class__', '__closure__', '__code__', '__defaults__',
                '__dict__', '__doc__', '__file__', '__func__', '__globals__',
                '__metaclass__', '__module__', '__mro__', '__name__', '__self__',
                '__slots__', '__weakref__'),
                suffix=r'\b'),
             Name.Variable.Magic),
        ],
        'numbers': [
            (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
            (r'\d+[eE][+-]?[0-9]+j?', Number.Float),
            (r'0[0-7]+j?', Number.Oct),
            (r'0[bB][01]+', Number.Bin),
            (r'0[xX][a-fA-F0-9]+', Number.Hex),
            (r'\d+L', Number.Integer.Long),
            (r'\d+j?', Number.Integer)
        ],
        'backtick': [
            ('`.*?`', String.Backtick),
        ],
        'name': [
            (r'@[\w.]+', Name.Decorator),
            (r'[a-zA-Z_]\w*', Name),
        ],
        'funcname': [
            include('magicfuncs'),
            (r'[a-zA-Z_]\w*', Name.Function, '#pop'),
            default('#pop'),
        ],
        'classname': [
            (r'[a-zA-Z_]\w*', Name.Class, '#pop')
        ],
        'import': [
            (r'(?:[ \t]|\\\n)+', Text),
            (r'as\b', Keyword.Namespace),
            (r',', Operator),
            (r'[a-zA-Z_][\w.]*', Name.Namespace),
            default('#pop')  # all else: go back
        ],
        'fromimport': [
            (r'(?:[ \t]|\\\n)+', Text),
            (r'import\b', Keyword.Namespace, '#pop'),
            # if None occurs here, it's "raise x from None", since None can
            # never be a module name
            (r'None\b', Name.Builtin.Pseudo, '#pop'),
            # sadly, in "raise x from y" y will be highlighted as namespace too
            (r'[a-zA-Z_.][\w.]*', Name.Namespace),
            # anything else here also means "raise x from y" and is therefore
            # not an error
            default('#pop'),
        ],
        'stringescape': [
            (r'\\([\\abfnrtv"\']|\n|N\{.*?\}|u[a-fA-F0-9]{4}|'
             r'U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', String.Escape)
        ],
        'strings-single': innerstring_rules(String.Single),
        'strings-double': innerstring_rules(String.Double),
        'dqs': [
            (r'"', String.Double, '#pop'),
            (r'\\\\|\\"|\\\n', String.Escape),  # included here for raw strings
            include('strings-double')
        ],
        'sqs': [
            (r"'", String.Single, '#pop'),
            (r"\\\\|\\'|\\\n", String.Escape),  # included here for raw strings
            include('strings-single')
        ],
        'tdqs': [
            (r'"""', String.Double, '#pop'),
            include('strings-double'),
            (r'\n', String.Double)
        ],
        'tsqs': [
            (r"'''", String.Single, '#pop'),
            include('strings-single'),
            (r'\n', String.Single)
        ],
    }

    def analyse_text(text):
        return shebang_matches(text, r'pythonw?(2(\.\d)?)?') or \
            'import ' in text[:1000]


class RenpyConsoleLexer(Lexer):
    """
    For Renpy console output or doctests, such as:

    .. sourcecode:: rpycon

        >>> a = 'foo'
        >>> print a
        foo
        >>> 1 / 0
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        ZeroDivisionError: integer division or modulo by zero

        .. versionadded:: 0.1
    """
    name = 'Renpy console session'
    aliases = ['rpycon']

    def __init__(self, **options):
        Lexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        pylexer = RenpyLexer(**self.options)
        tblexer = RenpyTracebackLexer(**self.options)

        curcode = ''
        insertions = []
        curtb = ''
        tbindex = 0
        tb = 0
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith(u'>>> ') or line.startswith(u'... '):
                tb = 0
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, line[:4])]))
                curcode += line[4:]
            elif line.rstrip() == u'...' and not tb:
                # only a new >>> prompt can end an exception block
                # otherwise an ellipsis in place of the traceback frames
                # will be mishandled
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, u'...')]))
                curcode += line[3:]
            else:
                if curcode:
                    for item in do_insertions(
                            insertions,
                            pylexer.get_tokens_unprocessed(curcode)):
                        yield item
                    curcode = ''
                    insertions = []
                if (line.startswith(u'Traceback (most recent call last):') or
                        re.match(u'  File "[^"]+", line \\d+\\n$', line)):
                    tb = 1
                    curtb = line
                    tbindex = match.start()
                elif line == 'KeyboardInterrupt\n':
                    yield match.start(), Name.Class, line
                elif tb:
                    curtb += line
                    if not (line.startswith(' ') or line.strip() == u'...'):
                        tb = 0
                        for i, t, v in tblexer.get_tokens_unprocessed(curtb):
                            yield tbindex + i, t, v
                        curtb = ''
                else:
                    yield match.start(), Generic.Output, line
        if curcode:
            for item in do_insertions(insertions,
                                      pylexer.get_tokens_unprocessed(curcode)):
                yield item
        if curtb:
            for i, t, v in tblexer.get_tokens_unprocessed(curtb):
                yield tbindex + i, t, v


class RenpyTracebackLexer(RegexLexer):
    """
    For Renpy tracebacks.

    .. versionadded:: 0.1
    """

    name = 'Renpy Traceback'
    aliases = ['rpytb']
    filenames = ['*.rpytb']

    tokens = {
        'root': [
            # Cover both (most recent call last) and (innermost last)
            # The optional ^C allows us to catch keyboard interrupt signals.
            (r'^(\^C)?(Traceback.*\n)',
             bygroups(Text, Generic.Traceback), 'intb'),
            # SyntaxError starts with this.
            (r'^(?=  File "[^"]+", line \d+)', Generic.Traceback, 'intb'),
            (r'^.*\n', Other),
        ],
        'intb': [
            (r'^(  File )("[^"]+")(, line )(\d+)(, in )(.+)(\n)',
             bygroups(Text, Name.Builtin, Text, Number, Text, Name, Text)),
            (r'^(  File )("[^"]+")(, line )(\d+)(\n)',
             bygroups(Text, Name.Builtin, Text, Number, Text)),
            (r'^(    )(.+)(\n)',
             bygroups(Text, using(RenpyLexer), Text)),
            (r'^([ \t]*)(\.\.\.)(\n)',
             bygroups(Text, Comment, Text)),  # for doctests...
            (r'^([^:]+)(: )(.+)(\n)',
             bygroups(Generic.Error, Text, Name, Text), '#pop'),
            (r'^([a-zA-Z_]\w*)(:?\n)',
             bygroups(Generic.Error, Text), '#pop')
        ],
    }


class NullLexer(RegexLexer):
    name = 'Null'
    aliases = ['null']
    filenames = ['*.null']

    tokens = {
        'root': [
            (r' .*\n', Text),
        ]
    }
