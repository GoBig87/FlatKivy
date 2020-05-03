"""
Themes/Font Definitions
=======================

.. seealso::

   `Material Design spec, The type system <https://material.io/design/typography/the-type-system.html>`_
"""

from kivy.core.text import LabelBase

from flatkivy import fonts_path, icons_path

fonts = [
    {
        "name": "Lato",
        "fn_regular": fonts_path + "lato-regular.ttf",
        "fn_bolditalic": fonts_path + "lato-bolditalic.ttf",
        "fn_italic": fonts_path + "lato-italic.ttf",
    },
    {
        "name": "LatoBold",
        "fn_regular": fonts_path + "lato-bold.ttf",
    },
    {
        "name": "LatoLight",
        "fn_regular": fonts_path + "lato-light.ttf",
    },
    {
        "name": "LatoBlack",
        "fn_regular": fonts_path + "lato-black.ttf",
    },
    {
        "name": "Icons",
        "fn_regular": icons_path + "icomoon.ttf",
    },
]

for font in fonts:
    print(font)
    LabelBase.register(**font)

theme_font_styles = [
    "Header",
    "Subtitle",
    "Body",
    "Button",
    "Caption",
    "Icon",
]
