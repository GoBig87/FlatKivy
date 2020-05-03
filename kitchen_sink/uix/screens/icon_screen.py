# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget
from flatkivy.uix.label import FlatColorIcon, FlatLabel, FlatIcon
from flatkivy.uix.button import FlatButton
from flatkivy.icon_definitions import flat_icons


class IconScreen(Screen):
    def __init__(self, **kwargs):
        super(IconScreen, self).__init__(name=kwargs.get('name'))
        return self.uix_layout()

    def uix_layout(self):
        layout = BoxLayout(orientation='vertical')

        self.scroll = ScrollView(do_scroll_x=False, size_hint=(1, None),
                                 size=(Window.width, Window.height))
        scroll_box = BoxLayout(orientation='vertical', size_hint_y=None,
                               padding=(dp(1), dp(60)), spacing=dp(60))
        scroll_box.bind(minimum_height=scroll_box.setter('height'))
        # Add more self.scrollbox.add_widget(MDLabel(text='')) to increase padding
        scroll_box.add_widget(FlatLabel(text=' '))
        scroll_box.add_widget(FlatLabel(text=' '))
        scroll_box.add_widget(FlatLabel(text=' '))

        count = 0
        # for icon in flat_icons:
        #     count = count + 1
        #     scroll_box.add_widget(FlatColorIcon(icon=icon))
        #     if count > 90:
        #         break
        for icon in flat_icons:
            _icon = flat_icons[icon]
            if len(_icon) == 1:
                scroll_box.add_widget(FlatIcon(code=_icon[0][1]))
            else:
                count = count + 1
                scroll_box.add_widget(FlatColorIcon(icon=icon))
            if count > 100:
                break

        self.scroll.add_widget(scroll_box)
        layout.add_widget(self.scroll)

        self.add_widget(layout)
