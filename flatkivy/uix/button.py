__all__ = (
    "FlatButton",
)

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, RoundedRectangle
from kivy.graphics.stencil_instructions import (
    StencilPush,
    StencilUse,
    StencilPop,
    StencilUnUse,
)
from kivy.properties import (
    StringProperty,
    BoundedNumericProperty,
    ListProperty,
    AliasProperty,
    BooleanProperty,
    NumericProperty,
    OptionProperty,
    ObjectProperty,
    DictProperty,
)

from flatkivy.theming import ThemableBehavior
from flatkivy.uix.label import FlatLabel
from flatkivy.uix.behaviors import (
    SpecificBackgroundColorBehavior,
    RectangularRippleBehavior,
)

Builder.load_string(
    """

<BaseButton>
    size_hint: (None, None)
    anchor_x: 'center'
    anchor_y: 'center'
<BaseFlatButton>

<BaseRectangularButton>
    canvas:
        Clear
        Color:
            rgba: self._current_button_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: (1.5*root._radius, )
    lbl_txt: lbl_txt
    height: dp(36) if not root._height else root._height
    width: lbl_txt.texture_size[0] + root.increment_width
    padding: (dp(8), 0)
    theme_text_color: 'Primary' if not root.text_color else 'Custom'
    markup: False
    
    FlatLabel:
        id: lbl_txt
        text: root.text if root.button_label else ''
        font_size: sp(root.font_size)
        font_name: root.font_name if root.font_name is not None else self.font_name
        can_capitalize: root.can_capitalize
        size_hint_x: None
        text_size: (None, root.height)
        height: self.texture_size[1]
        theme_text_color: root.theme_text_color
        text_color: root.text_color
        markup: root.markup
        disabled: root.disabled
        valign: 'middle'
        halign: 'center'
        opposite_colors: root.opposite_colors
    """
)


class BaseButton(
    ThemableBehavior,
    ButtonBehavior,
    SpecificBackgroundColorBehavior,
    AnchorLayout,
    Widget,
):
    """
    Abstract base class for all Flat Kivy buttons. This class handles the button's
    colors (disabled/down colors handled in children classes as those depend on
    type of button) as well as the disabled state.
    """

    theme_text_color = OptionProperty(
        None,
        allownone=True,
        options=[
            "Primary",
            "Secondary",
            "Error",
            "Custom",
            "ContrastParentBackground",
        ],
    )
    """
    Button text type. Available options are: (`"Primary"`, `"Secondary"`,
    `"Error"`, `"Custom"`, `"ContrastParentBackground"`).
    :attr:`theme_text_color` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `None`.
    """

    text_color = ListProperty(None, allownone=True)
    """
    Text color in ``rgba`` format.
    :attr:`text_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    """

    font_name = StringProperty(None)
    """
    Font name.
    :attr:`font_name` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    font_size = NumericProperty(14)
    """
    Font size.
    :attr:`font_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `14`.
    """

    user_font_size = NumericProperty()
    """Custom font size for :class:`~MDIconButton`.

    :attr:`user_font_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """

    opposite_colors = BooleanProperty(False)

    _flat_bg_color_down = ListProperty(None, allownone=True)
    _flat_bg_color_disabled = ListProperty(None, allownone=True)
    _current_button_color = ListProperty([0.0, 0.0, 0.0, 0.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self._update_color()

    def on_flat_bg_color(self, instance, value):
        self._update_color()

    def _update_color(self):
        if not self.disabled:
            self._current_button_color = self.flat_bg_color
        else:
            self._current_button_color = self.flat_bg_color_disabled

    def _call_get_bg_color_down(self):
        return self._get_flat_bg_color_down()

    def _get_flat_bg_color_down(self):
        if self._flat_bg_color_down:
            return self._flat_bg_color_down
        else:
            raise NotImplementedError

    def _set_flat_bg_color_down(self, value):
        self._flat_bg_color_down = value

    flat_bg_color_down = AliasProperty(
        _call_get_bg_color_down, _set_flat_bg_color_down
    )
    """
    Value of the current button background color.
    :attr:`md_bg_color_down` is an :class:`~kivy.properties.AliasProperty`
    that returns the value in ``rgba`` format for :attr:`md_bg_color_down`,
    property is readonly.
    """

    def _call_get_bg_color_disabled(self):
        return self._get_flat_bg_color_disabled()

    def _get_flat_bg_color_disabled(self):
        if self._flat_bg_color_disabled:
            return self._flat_bg_color_disabled
        else:
            raise NotImplementedError

    def _set_flat_bg_color_disabled(self, value):
        self._flat_bg_color_disabled = value

    flat_bg_color_disabled = AliasProperty(
        _call_get_bg_color_disabled, _set_flat_bg_color_disabled
    )
    """
    Value of the current button disabled color.
    :attr:`md_bg_color_disabled` is an :class:`~kivy.properties.AliasProperty`
    that returns the value in ``rgba`` format for :attr:`md_bg_color_disabled`,
    property is readonly.
    """

    def on_disabled(self, instance, value):
        if self.disabled:
            self._current_button_color = self.flat_bg_color_disabled
        else:
            self._current_button_color = self.flat_bg_color


class BaseFlatButton(BaseButton):
    """
    Abstract base class for flat buttons which do not elevate from material.
    Enforces the recommended down/disabled colors for flat buttons
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flat_bg_color = (0.0, 0.0, 0.0, 0.0)

    def _get_flat_bg_color_down(self):
        if self.theme_cls.theme_style == "Dark":
            c = get_color_from_hex("cccccc")
            c[3] = 0.25
        else:
            c = get_color_from_hex("999999")
            c[3] = 0.4
        return c

    def _get_flat_bg_color_disabled(self):
        bg_c = self.flat_bg_color
        if bg_c[3] == 0:  # transparent background
            c = bg_c
        else:
            if self.theme_cls.theme_style == "Dark":
                c = (1.0, 1.0, 1.0, 0.12)
            else:
                c = (0.0, 0.0, 0.0, 0.12)
        return c


class BasePressedButton(BaseButton):
    """
    Abstract base class for those button which fade to a background color on
    press.
    """

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        elif not self.collide_point(touch.x, touch.y):
            return False
        elif self in touch.ud:
            return False
        elif self.disabled:
            return False
        else:
            self.fade_bg = Animation(
                duration=0.5, _current_button_color=self.flat_bg_color_down
            )
            self.fade_bg.start(self)
            return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.fade_bg.stop_property(self, "_current_button_color")
            Animation(
                duration=0.05, _current_button_color=self.flat_bg_color
            ).start(self)
        return super().on_touch_up(touch)


class BaseRectangularButton(RectangularRippleBehavior, BaseButton):
    """
    Abstract base class for all rectangular buttons, bringing in the
    appropriate on-touch behavior. Also maintains the correct minimum width
    as stated in guidelines.
    """

    width = BoundedNumericProperty(
        88, min=88, max=None, errorhandler=lambda x: 88
    )
    text = StringProperty("")
    """Button text.
    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    increment_width = NumericProperty("32dp")
    """
    Button extra width value.
    :attr:`increment_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'32dp'`.
    """

    button_label = BooleanProperty(True)
    """
    If ``False`` the text on the button will not be displayed.
    :attr:`button_label` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    can_capitalize = BooleanProperty(True)

    _radius = NumericProperty("2dp")
    _height = NumericProperty(0)


class FlatButton(BaseRectangularButton, BaseFlatButton, BasePressedButton):
    pass
