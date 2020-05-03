import ast
import os
import sys

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition

from .flatkivy.app import FlatApp

from kitchen_sink.uix.screens.button_screen import ButtonScreen
from kitchen_sink.uix.screens.icon_screen import IconScreen


class KitchenSinkApp(FlatApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Turquoise"
        self.theme_cls.theme_style = 'Dark'

    def build(self):
        return KitchenSinkLayout()


class KitchenSinkLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(KitchenSinkLayout, self).__init__()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')
        self.content = ScreenManager()
        self.content.transition = NoTransition()

        self.content.add_widget(IconScreen(name='icon'))
        self.content.add_widget(ButtonScreen(name='welcome'))

        self.screens.add_widget(self.content)

        self.add_widget(self.screens)



if __name__ == "__main__":
    KitchenSinkApp().run()