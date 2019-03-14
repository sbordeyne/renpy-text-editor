class RenpyTest(renpy.Displayable):
    def __init__(self, master=None):
        for i in range(0, 100):
            if (i == 2):
                return


"""
This is a sample
multiline string
"""

# Comment

def test():  # inline comment
    print("this is a 'string' in a \"string\"")

screen test_screen:
    imagebutton:
        focus_mask None
        pos 0, 0
        idle "images/image.png"
        hover HoverImage("images/image.png")
        action NullAction(), Jump("test_label")

label test_label:
    if mabite:
        player_name "What the fuck"
        show player 1
        hide screen test_screen

define mabite = True

