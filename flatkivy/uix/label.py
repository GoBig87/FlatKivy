__all__ = (
    "FlatLabel",
)

from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import (
    OptionProperty,
    ListProperty,
    BooleanProperty,
    StringProperty,
    AliasProperty,
    NumericProperty,
)
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg
from kivy.graphics import Scale

from flatkivy.font_definitions import theme_font_styles
from flatkivy.theming import ThemableBehavior
from flatkivy.icon_definitions import flat_icons

Builder.load_string(
    """
#:import flat_icons flatkivy.icon_definitions.flat_icons    
    
<FlatLabel>
    disabled_color: [1,1,1,1]
    text_size: self.width, None
    pos_hint: {"center_x": .5, "center_y": .5}
    
<FlatIcon>:
    font_style: "Icon"
    text: self.code
    canvas:
        Color:
            rgba: (0, 0, 0, 0)
        Rectangle:
            pos:  self.pos
            size: self.size
            
<FlatColorIcon>  

<FlatSvgIcon>:
    do_rotation: False

"""
)


class FlatLabel(ThemableBehavior, Label):
    font_style = OptionProperty("Body", options=theme_font_styles)
    """
    Label font style.

    Available options are: `'H1'`, `'H2'`, `'H3'`, `'H4'`, `'H5'`, `'H6'`,
    `'Subtitle1'`, `'Subtitle2'`, `'Body1'`, `'Body2'`, `'Button'`,
    `'Caption'`, `'Overline'`, `'Icon'`.
    :attr:`font_style` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'Body1'`.
    """

    _capitalizing = BooleanProperty(False)

    def _get_text(self):
        if self._capitalizing:
            return self._text.upper()
        return self._text

    def _set_text(self, value):
        self._text = value

    _text = StringProperty()

    text = AliasProperty(_get_text, _set_text, bind=["_text", "_capitalizing"])
    """Text of the label."""

    # theme_text_color = OptionProperty(
    #     None,
    #     allownone=True,
    #     options=[
    #         "Primary",
    #         "Secondary",
    #         "Hint",
    #         "Error",
    #         "Custom",
    #         "ContrastParentBackground",
    #     ],
    # )
    """
    Label color scheme name.
    Available options are: `'Primary'`, `'Secondary'`, `'Hint'`, `'Error'`,
    `'Custom'`, `'ContrastParentBackground'`.
    :attr:`theme_text_color` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `None`.
    """

    text_color = ListProperty(None, allownone=True)
    """Label text color in ``rgba`` format.
    :attr:`text_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    """

    parent_background = ListProperty(None, allownone=True)

    _currently_bound_property = {}

    can_capitalize = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = OptionProperty(
            None,
            allownone=True,
            options=[
                "Primary",
                "Secondary",
                "Hint",
                "Error",
                "Custom",
                "ContrastParentBackground",
            ],
        )
        self.bind(
            font_style=self.update_font_style,
            can_capitalize=self.update_font_style,
        )
        self.on_theme_text_color(None, self.theme_text_color)
        self.update_font_style()
        self.on_opposite_colors(None, self.opposite_colors)

    def update_font_style(self, *args):
        font_info = self.theme_cls.font_styles[self.font_style]
        self.font_name = font_info[0]
        self.font_size = sp(font_info[1])
        if font_info[2] and self.can_capitalize:
            self._capitalizing = True
        else:
            self._capitalizing = False
        # TODO: Add letter spacing change
        # self.letter_spacing = font_info[3]

    def on_theme_text_color(self, instance, value):
        t = self.theme_cls
        op = self.opposite_colors
        setter = self.setter("color")
        t.unbind(**self._currently_bound_property)
        attr_name = {
            "Primary": "text_color" if not op else "opposite_text_color",
            "Secondary": "secondary_text_color"
            if not op
            else "opposite_secondary_text_color",
            "Hint": "disabled_hint_text_color"
            if not op
            else "opposite_disabled_hint_text_color",
            "Error": "error_color",
        }.get(value, None)
        if attr_name:
            c = {attr_name: setter}
            t.bind(**c)
            self._currently_bound_property = c
            self.color = getattr(t, attr_name)
        else:
            # 'Custom' and 'ContrastParentBackground' lead here, as well as the
            # generic None value it's not yet been set
            if value == "Custom" and self.text_color:
                self.color = self.text_color
            else:
                self.color = [0, 0, 0, 1]

    def on_text_color(self, *args):
        if self.theme_text_color == "Custom":
            self.color = self.text_color

    def on_opposite_colors(self, instance, value):
        self.on_theme_text_color(self, self.theme_text_color)


class FlatIcon(FlatLabel):
    icon = StringProperty("android")
    code = StringProperty(u"\uE900")
    """
    Label icon name.
    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'android'`.
    """

    source = StringProperty(None, allownone=True)
    """
    Path to icon.
    :attr:`source` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    text_color = ListProperty(None, allownone=True)
    """Label text color in ``rgba`` format.
    :attr:`text_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    """


class FlatColorIcon(FlatLabel, FloatLayout):
    icon = StringProperty("android")

    def __init__(self, **kwargs):
        super(FlatColorIcon, self).__init__(**kwargs)
        self.font_name = 'Icon'
        icon_stack = flat_icons[self.icon]
        for layer in icon_stack:
            color = layer[0]
            code = layer[1]
            icon_layer = FlatIcon(code=code)
            icon_layer.theme_text_color = 'Custom'
            icon_layer.text_color = color
            self.add_widget(icon_layer)


class FlatSvgIcon(FlatLabel, Scatter):
    filename = StringProperty(None)
    """Filename that includes the path to your SVG icon.
    :attr:`filename` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    def __init__(self, **kwargs):
        super(FlatSvgIcon, self).__init__(**kwargs)
        with self.canvas:
            self._scale = Scale(1.)
            self.svg = Svg(self.filename)
        self.size = self.svg.width, self.svg.height
        self.size_hint = (None, None)
        self.bind(size=self._do_scale)

    def _do_scale(self, *args):
        if [self.svg.width, self.svg.height] != self.size:
            self._scale.xyz = ( (self.width / self.svg.width),
                                (self.height / self.svg.height),
                              1)