"""
Themes/Theming
==============

.. seealso::

   `Flat UI Design spec https://designmodo.com/flat-free/

Flat UI App
------------

The main class of your application, which in `Kivy` inherits from the App class,
in `FlatKivy` must inherit from the `FlatApp` class. The `FlatApp` class has
properties that allow you to control application properties
such as :attr:`color/style/font` of interface elements and much more.

Control flat ui properties
---------------------------

The main application class inherited from the `FlatApp` class has the :attr:`flat_theme_cls`
attribute, with which you control the flat ui properties of your application.
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    OptionProperty,
    AliasProperty,
    ObjectProperty,
    StringProperty,
    ListProperty,
    BooleanProperty,
    DictProperty,
)
from kivy.event import EventDispatcher
from kivy.utils import get_color_from_hex

from flatkivy.color_definitions import colors, palette
from flatkivy.flat_resources import DEVICE_TYPE, DEVICE_IOS


class ThemeManager(EventDispatcher):
    p = StringProperty()
    r = StringProperty()
    i = StringProperty()
    m = StringProperty()
    a = StringProperty()
    r = StringProperty()
    y = StringProperty()
    _ = StringProperty()

    primary_palette = OptionProperty("Turquoise", options=palette)
    """
    The name of the color scheme that the application will use.
    All major `material` components will have the color
    of the specified color theme.

    Available options are: `'Turquoise'`, `'Green Sea'`, `'Emerald'`, `'Nephritis'`,
    `'Peter River'`, `'Belize Hole'`, `'Amthyst'`, `'WISTERIA'`,`'Wet Asphalt'`, `'Midnight'`, `'Sun Flower'`,
    `'Orange'`, `'Carrot'`, `'Pumpkin'`, `'Alizarin'`, `'Pomegranate'`, `'Clouds'`,
    `'Silver'`, `'Concrete'`, `'Asbestos'`.

    To change the color scheme of an application:

    .. code-block:: python

        from kivy.uix.screenmanager import Screen

        from flatkivy.app import FlatApp
        from flatkivy.uix.button import FlatButton


        class MainApp(FlatApp):
            def build(self):
                self.theme_cls.primary_palette = "Turquois"  # "Green Sea", "Emerald"

                screen = Screen()
                screen.add_widget(
                    FlatButton(
                        text="Hello, World",
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                    )
                )
                return screen


        MainApp().run()

    :attr:`primary_palette` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'Blue'`.
    """


    def _get_primary_color(self):
        return get_color_from_hex(
            colors[self.primary_palette]['BASE']
        )

    primary_color = AliasProperty(
        _get_primary_color, bind=("primary_palette", "primary_palette")
    )

    accent_palette = OptionProperty("Silver", options=palette)
    """
    The color of the current application theme in ``rgba`` format.

    :attr:`primary_color` is an :class:`~kivy.properties.AliasProperty` that
    returns the value of the current application theme, property is readonly.
    """

    def _get_accent_color(self):
        return get_color_from_hex(colors[self.accent_palette])

    accent_color = AliasProperty(
        _get_accent_color, bind=["accent_palette"]
    )
    """Similar to :attr:`primary_color`,
    but returns a value for :attr:`accent_color`.

    :attr:`accent_color` is an :class:`~kivy.properties.AliasProperty` that
    returns the value in ``rgba`` format for :attr:`accent_color`,
    property is readonly.
    """

    theme_style = OptionProperty("Light", options=["Light", "Dark"])
    """App theme style.

    .. code-block:: python

        from kivy.uix.screenmanager import Screen

        from kivymd.app import MDApp
        from kivymd.uix.button import MDRectangleFlatButton


        class MainApp(MDApp):
            def build(self):
                self.theme_cls.theme_style = "Dark"  # "Light"

                screen = Screen()
                screen.add_widget(
                    MDRectangleFlatButton(
                        text="Hello, World",
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                    )
                )
                return screen


        MainApp().run()

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/theme-style.png

    :attr:`theme_style` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'Light'`.
    """

    def _get_theme_style(self, opposite):
        if opposite:
            return "Light" if self.theme_style == "Dark" else "Dark"
        else:
            return self.theme_style

    def _get_bg_color(self, opposite=False):
        theme_style = self._get_theme_style(opposite)
        if theme_style == "Light":
            return get_color_from_hex(colors["Clouds"]["BASE"])
        elif theme_style == "Dark":
            return get_color_from_hex(colors["Midnight Blue"]["BASE"])

    bg_color = AliasProperty(_get_bg_color, bind=["theme_style", "theme_style"])
    """
    Similar to :attr:`bg_dark`,
    but the color values ​​are a tone lower (darker) than :attr:`bg_dark`.

    .. code-block:: python

        KV = '''
        <Box@BoxLayout>:
            bg: 0, 0, 0, 0

            canvas:
                Color:
                    rgba: root.bg
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:

            Box:
                bg: app.theme_cls.bg_light
            Box:
                bg: app.theme_cls.bg_normal
            Box:
                bg: app.theme_cls.bg_dark
            Box:
                bg: app.theme_cls.bg_darkest
        '''

        from kivy.lang import Builder

        from kivymd.app import MDApp


        class MainApp(MDApp):
            def build(self):
                self.theme_cls.theme_style = "Dark"  # "Light"
                return Builder.load_string(KV)


        MainApp().run()

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/bg-normal-dark-darkest.png

    :attr:`bg_darkest` is an :class:`~kivy.properties.AliasProperty` that
    returns the value in ``rgba`` format for :attr:`bg_darkest`,
    property is readonly.
    """

    def _get_bg_accent(self, opposite=False):
        theme_style = self._get_theme_style(opposite)
        if theme_style == "Light":
            return get_color_from_hex(colors["Silver"]["BASE"])
        elif theme_style == "Dark":
            return get_color_from_hex(colors["Wet Asphalt"]["BASE"])

    bg_accent = AliasProperty(_get_bg_accent, bind=["theme_style"])
    """
    Similar to :attr:`bg_normal`,
    but the color values ​​are one tone lower (darker) than :attr:`bg_normal`.

    :attr:`bg_dark` is an :class:`~kivy.properties.AliasProperty` that
    returns the value in ``rgba`` format for :attr:`bg_dark`,
    property is readonly.
    """



    """
    Similar to :attr:`bg_light`,
    but the color values ​​are one tone lower (darker) than :attr:`bg_light`.

    :attr:`bg_normal` is an :class:`~kivy.properties.AliasProperty` that
    returns the value in ``rgba`` format for :attr:`bg_normal`,
    property is readonly.
    """

    def _get_ripple_color(self):
        return self._ripple_color

    def _set_ripple_color(self, value):
        self._ripple_color = value

    var = colors['Silver']
    _ripple_color = ListProperty(get_color_from_hex(colors["Silver"]['BASE']))
    """Private value."""

    ripple_color = AliasProperty(
        _get_ripple_color, _set_ripple_color, bind=["_ripple_color"]
    )
    """
    Color of ripple effects.

    :attr:`ripple_color` is an :class:`~kivy.properties.AliasProperty` that
    returns the value in ``rgba`` format for :attr:`ripple_color`,
    property is readonly.
    """

    def _determine_device_orientation(self, _, window_size):
        if window_size[0] > window_size[1]:
            self.device_orientation = "landscape"
        elif window_size[1] >= window_size[0]:
            self.device_orientation = "portrait"

    device_orientation = StringProperty("")
    """
    Device orientation.

    :attr:`device_orientation` is an :class:`~kivy.properties.StringProperty`.
    """

    def _get_standard_increment(self):
        if DEVICE_TYPE == "mobile":
            if self.device_orientation == "landscape":
                return dp(48)
            else:
                return dp(56)
        else:
            return dp(64)

    standard_increment = AliasProperty(
        _get_standard_increment, bind=["device_orientation"]
    )
    """
    Value of standard increment.

    :attr:`standard_increment` is an :class:`~kivy.properties.AliasProperty`
    that returns the value in ``rgba`` format for :attr:`standard_increment`,
    property is readonly.
    """

    def _get_horizontal_margins(self):
        if DEVICE_TYPE == "mobile":
            return dp(16)
        else:
            return dp(24)

    horizontal_margins = AliasProperty(_get_horizontal_margins)
    """
    Value of horizontal margins.

    :attr:`horizontal_margins` is an :class:`~kivy.properties.AliasProperty`
    that returns the value in ``rgba`` format for :attr:`horizontal_margins`,
    property is readonly.
    """

    def on_theme_style(self, instance, value):
        if (
            hasattr(App.get_running_app(), "theme_cls")
            and App.get_running_app().theme_cls == self
        ):
            self.set_clearcolor_by_theme_style(value)

    set_clearcolor = BooleanProperty(True)

    def set_clearcolor_by_theme_style(self, theme_style):
        if not self.set_clearcolor:
            return
        if theme_style == "Light":
            Window.clearcolor = get_color_from_hex(
                colors["Clouds"]["BASE"]
            )
        elif theme_style == "Dark":
            Window.clearcolor = get_color_from_hex(colors["Wet Asphalt"]["BASE"])

    # font name, size (sp), always caps, letter spacing (sp)
    font_styles = DictProperty(
        {
            "Header": ["LatoBold", 96, False, -1.5],
            "Subtitle": ["LatoLight", 24, False, 0.15],
            "Body": ["Lato", 40, False, 0.5],
            "Button": ["LatoLight", 24, True, 1.25],
            "Icon": ["Icons", 60, False, 0],
        }
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self.on_theme_style(0, self.theme_style))
        self._determine_device_orientation(None, Window.size)
        Window.bind(size=self._determine_device_orientation)


class ThemableBehavior(EventDispatcher):
    theme_cls = ObjectProperty()
    """
    Instance of :class:`~ThemeManager` class.

    :attr:`theme_cls` is an :class:`~kivy.properties.ObjectProperty`.
    """

    device_ios = BooleanProperty(DEVICE_IOS)
    """
    ``True`` if device is ``iOS``.

    :attr:`device_ios` is an :class:`~kivy.properties.BooleanProperty`.
    """

    opposite_colors = BooleanProperty(False)

    def __init__(self, **kwargs):
        if self.theme_cls is not None:
            pass
        else:
            try:
                if not isinstance(
                    App.get_running_app().property("theme_cls", True),
                    ObjectProperty,
                ):
                    raise ValueError(
                        "KivyMD: App object must be inherited from "
                        "`kivymd.app.MDApp`. See "
                        "https://github.com/HeaTTheatR/KivyMD/blob/master/README.md#api-breaking-changes"
                    )
            except AttributeError:
                raise ValueError(
                    "KivyMD: App object must be initialized before loading "
                    "root widget. See "
                    "https://github.com/HeaTTheatR/KivyMD/wiki/Modules-Material-App#exceptions"
                )
            self.theme_cls = App.get_running_app().theme_cls
        super().__init__(**kwargs)
