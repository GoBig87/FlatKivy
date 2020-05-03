# Kivy imports
from kivy.uix.screenmanager import Screen
from flatkivy.app import FlatApp
from flatkivy.uix.button import FlatButton
from flatkivy.uix.label import FlatColorIcon, FlatIcon


class ButtonScreen(Screen):
    def __init__(self, **kwargs):
        super(ButtonScreen, self).__init__(name=kwargs.get('name'))
        self.uix_layout()

    def uix_layout(self):
        fb = FlatButton()
        fb.theme_text_color = "Custom"
        fb.text_color = [1,1,1,1]
        fb.font_size = 24
        fb.flat_bg_color = FlatApp.get_running_app().theme_cls.primary_color
        fb.text = 'Hello there'
        self.add_widget(fb)

        fi = FlatColorIcon(icon='App-Amethyst')
        fi.font_size = 80
        self.add_widget(fi)
