from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from control import Controller

Config.set('graphics', 'width', 320)
Config.set('graphics', 'height', 240)

Builder.load_string("""
#: import NoTransition kivy.uix.screenmanager.NoTransition

<LLabel@Label>:
    font_size: '40px'
    markup: True
    bold: True

<Butt@Button>:
    font_size: '50px'
    bold: True
    markup: True

<MenuScreen>:
    BoxLayout:
        #size_hint: [0.9, 0.9]
        #pos_hint: { 'top' : .95, 'right': .95}
        orientation: 'vertical'
        font_size: '40sp'
        LLabel:
            size_hint: [1, 2]
            text: 'Theremin 2.0'
            font_size: '60px'
        Butt:
            text: 'Tune'
            on_press:
                root.manager.transition = NoTransition()
                root.manager.current = 'tune'
        Butt:
            text: 'Quit'
            on_press: app.stop()

<TuneScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            LLabel:
                text: 'Low pitch: ' + str(int(lps.value))
            Slider:
                id: lps
                min: 0
                value: 300
                max: 400
                step: 1
                on_value: root.controller.pitch_low = self.value
        BoxLayout:
            LLabel:
                text: 'High pitch: ' + str(int(hps.value))
            Slider:
                id: hps
                min: 0
                value: 60
                max: 400
                step: 1
                on_value: root.controller.pitch_high = self.value
        BoxLayout:
            LLabel:
                text: 'Max volume: ' + str(int(maxs.value))
            Slider:
                id: maxs
                min: 0
                value: 300
                max: 400
                step: 1
                on_value: root.controller.vol_high = self.value
        BoxLayout:
            LLabel:
                text: 'Min volume: ' + str(int(mins.value))
            Slider:
                id: mins
                min: 0
                value: 60
                max: 400
                step: 1
                on_value: root.controller.vol_low = self.value
        Butt:
            text: 'Back'
            on_press:
                root.manager.transition = NoTransition()
                root.manager.current = 'menu'
""")


class MenuScreen(Screen):
    pass


class TuneScreen(Screen):
    def __init__(self, sensor_controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = sensor_controller


class ThereminGUI(App):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.sensor_controller = controller

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TuneScreen(self.sensor_controller, name='tune'))
        return sm


if __name__ == '__main__':
    controller = Controller()
    ThereminGUI(controller).run()
