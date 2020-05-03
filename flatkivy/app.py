"""
Themes/Material App
===================

This module contains :class:`MDApp` class that is inherited from
:class:`~kivy.app.App`. :class:`MDApp` has some properties needed for ``KivyMD``
library (like :attr:`~MDApp.theme_cls`).

You can turn on the monitor displaying the current ``FPS`` value in your application:

.. code-block:: python

    KV = '''
    Screen:

        MDLabel:
            text: "Hello, World!"
            halign: "center"
    '''

    from kivy.lang import Builder

    from kivymd.app import MDApp


    class MainApp(MDApp):
        def build(self):
            return Builder.load_string(KV)

        def on_start(self):
            self.fps_monitor_start()


    MainApp().run()

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/fps-monitor.png
    :width: 350 px
    :align: center

"""

__all__ = ("FlatApp",)

from kivy.app import App
from kivy.properties import ObjectProperty

from flatkivy.theming import ThemeManager


class FlatApp(App):
    theme_cls = ObjectProperty(ThemeManager())
    """
    Instance of :class:`~ThemeManager` class.

    .. Warning:: The :attr:`~theme_cls` attribute is already available
        in a class that is inherited from the :class:`~MDApp` class.
        The following code will result in an error!

    .. code-block:: python

        class MainApp(MDApp):
            theme_cls = ThemeManager()
            theme_cls.primary_palette = "Teal"

    .. Note:: Correctly do as shown below!

    .. code-block:: python

        class MainApp(MDApp):
            def build(self):
                self.theme_cls.primary_palette = "Teal"

    :attr:`theme_cls` is an :class:`~kivy.properties.ObjectProperty`.
    """
