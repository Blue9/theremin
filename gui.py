import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from control import Controller

Config.set('graphics', 'width', 320)
Config.set('graphics', 'height', 240)

Builder.load_string("""
#: import NoTransition kivy.uix.screenmanager.NoTransition
#: import SlideTransition kivy.uix.screenmanager.SlideTransition

<LLabel@Label>:
    font_size: '40px'
    markup: True
    bold: True

<Butt@Button>:
    font_size: '50px'
    bold: True
    markup: True
    # background_color: (1, 2, 1, 1)

<ReturnButt@Butt>:
    background_color: (2, 0.5, 0.5, 1)

<MenuScreen>:
    BoxLayout:
        #size_hint: [0.9, 0.9]
        #pos_hint: { 'top' : .95, 'right': .95}
        orientation: 'vertical'
        font_size: '40sp'
        LLabel:
            text: 'Theremin 2.0'
            font_size: '60px'
        GridLayout:
            size_hint: [1, 2]
            cols: 2
            Butt:
                text: 'Tune'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'tune'
            Butt:
                text: 'Loop'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'loop'
            Butt:
                text: 'Select Sound'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'select_sound'
            Butt:
                text: 'Options'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'options'
        ReturnButt:
            text: 'Quit'
            on_press: root.controller.running = False; app.stop()

<LoopScreen>:
    BoxLayout:
        orientation: 'vertical'
        Butt:
            text: 'Start recording'
            on_press:
                root.controller.rec = 'start'
        Butt:
            text: 'Reset loops'
            on_press:
                root.controller.rec = 'reset'
        ReturnButt:
            text: 'Back'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'


<OptionsScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            LLabel:
                text: 'Octave shift: ' + str(round(octave.value))
            Slider:
                id: octave
                min: -2
                value: 0
                max: 2
                step: 1
                on_value: root.controller.octave_shift = self.value
        BoxLayout:
            LLabel:
                text: 'BPM: ' + str(round(bpm.value))
            Slider:
                id: bpm
                min: 60
                value: 140
                max: 200
                step: 10
                on_value: root.controller.bpm = self.value
        Butt:
            text: 'Toggle instrument loop'
            on_press:
                root.controller.repeat = not root.controller.repeat    
        Butt:
            text: 'Toggle fun mode'
            on_press:
                root.controller.fun_mode = not root.controller.fun_mode
        ReturnButt:
            text: 'Back'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'



<TuneScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            LLabel:
                text: 'Pitch near: ' + str(int(lps.value))
            Slider:
                id: lps
                min: 0
                value: 600
                max: 1000
                step: 10
                on_value: root.controller.pitch_low = self.value
        BoxLayout:
            LLabel:
                text: 'Pitch far: ' + str(int(hps.value))
            Slider:
                id: hps
                min: 0
                value: 60
                max: 1000
                step: 10
                on_value: root.controller.pitch_high = self.value
        BoxLayout:
            LLabel:
                text: 'Volume far: ' + str(int(maxs.value))
            Slider:
                id: maxs
                min: 0
                value: 600
                max: 1000
                step: 10
                on_value: root.controller.vol_high = self.value
        BoxLayout:
            LLabel:
                text: 'Volume near: ' + str(int(mins.value))
            Slider:
                id: mins
                min: 0
                value: 60
                max: 1000
                step: 10
                on_value: root.controller.vol_low = self.value
        ReturnButt:
            text: 'Back'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'


<SelectSoundScreen>:
    BoxLayout:
        orientation: 'vertical'
        TabbedPanel:
            size_hint: [1, 5]
            do_default_tab: False
            tab_width: self.parent.width / 3
            tab_height: '150px'
            TabbedPanelItem:
                text: 'Synths'
                font_size: '40px'
                GridLayout:
                    cols: 2
                    Butt:
                        text: 'Crunchy'
                        on_press: root.controller.set_sound('synth1')
                    Butt:
                        text: 'Smooth'
                        on_press: root.controller.set_sound('synth2')
                    Butt:
                        text: 'Soft'
                        on_press: root.controller.set_sound('synth3')
                    Butt:
                        text: 'Orchestra'
                        on_press: root.controller.set_sound('synth4')
            TabbedPanelItem:
                text: 'Drums'
                font_size: '40px'
                GridLayout:
                    cols: 2
                    Butt:
                        text: 'Kick'
                        on_press: root.controller.set_sound('kick')
                    Butt:
                        text: 'Clap'
                        on_press: root.controller.set_sound('clap')
                    Butt:
                        text: 'Hat'
                        on_press: root.controller.set_sound('hihat')
                    Butt:
                        text: 'Snare'
                        on_press: root.controller.set_sound('snare')
            TabbedPanelItem:
                text: 'Melody'
                font_size: '40px'
                GridLayout:
                    cols: 2
                    Butt:
                        text: 'Bell'
                        on_press: root.controller.set_sound('bell')
                    Butt:
                        text: 'Bell 2'
                        on_press: root.controller.set_sound('bell2')
                    Butt:
                        text: 'Guitar'
                        on_press: root.controller.set_sound('guitar')
                    Butt:
                        text: 'Bass'
                        on_press: root.controller.set_sound('bass')
                    Butt:
                        text: 'Lead'
                        on_press: root.controller.set_sound('lead')
        ReturnButt:
            text: 'Back'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'

""")


class MenuScreen(Screen):
    def __init__(self, sensor_controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = sensor_controller


class TuneScreen(Screen):
    def __init__(self, sensor_controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = sensor_controller


class LoopScreen(Screen):
    def __init__(self, sensor_controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = sensor_controller


class OptionsScreen(Screen):
    def __init__(self, sensor_controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = sensor_controller


class SelectSoundScreen(Screen):
    def __init__(self, sensor_controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = sensor_controller


class ThereminGUI(App):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.sensor_controller = controller

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(self.sensor_controller, name='menu'))
        sm.add_widget(TuneScreen(self.sensor_controller, name='tune'))
        sm.add_widget(LoopScreen(self.sensor_controller, name='loop'))
        sm.add_widget(SelectSoundScreen(self.sensor_controller, name='select_sound'))
        sm.add_widget(OptionsScreen(self.sensor_controller, name='options'))
        return sm


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 gui.py host')
    host = sys.argv[1]
    controller = Controller(host=host)
    thread = controller.main()
    ThereminGUI(controller).run()
