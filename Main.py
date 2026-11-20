from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.clock import Clock
from jnius import autoclass, cast

# دسترسی به سرویس‌های اندروید
Context = autoclass('android.content.Context')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
activity = PythonActivity.mActivity

class FlashApp(App):
    def build(self):
        self.camera_manager = None
        self.camera_id = None
        self.flash_on = False
        self.flash_event = None
        self.interval = 0.5  # سرعت پیش‌فرض چشمک‌زن

        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.btn_toggle = Button(text='روشن', size_hint=(1, 0.3))
        self.btn_toggle.bind(on_press=self.toggle_flash)
        layout.add_widget(self.btn_toggle)

        self.slider = Slider(min=0.1, max=2.0, value=0.5, step=0.1)
        self.slider.bind(value=self.on_speed_change)
        layout.add_widget(self.slider)

        return layout

    def _init_camera_manager(self):
        if self.camera_manager is None:
            service = activity.getSystemService(Context.CAMERA_SERVICE)
            self.camera_manager = cast('android.hardware.camera2.CameraManager', service)
            self.camera_id = self.camera_manager.getCameraIdList()[0]

    def turn_on_light(self):
        self._init_camera_manager()
        self.camera_manager.setTorchMode(self.camera_id, True)
        self._light_state = True

    def turn_off_light(self):
        if self.camera_manager and self.camera_id:
            self.camera_manager.setTorchMode(self.camera_id, False)
            self._light_state = False

    def toggle_flash(self, instance):
        if not self.flash_on:
            self.flash_on = True
            self.btn_toggle.text = 'خاموش'
            self.flash_event = Clock.schedule_interval(self.blink, self.interval)
        else:
            self.flash_on = False
            self.btn_toggle.text = 'روشن'
            if self.flash_event:
                self.flash_event.cancel()
            self.turn_off_light()

    def blink(self, dt):
        if getattr(self, '_light_state', False):
            self.turn_off_light()
        else:
            self.turn_on_light()

    def on_speed_change(self, instance, value):
        self.interval = value
        if self.flash_event:
            self.flash_event.cancel()
            self.flash_event = Clock.schedule_interval(self.blink, self.interval)

if __name__ == '__main__':
    FlashApp().run()
