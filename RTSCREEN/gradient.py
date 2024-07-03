from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder


kv = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient kivy_gradient.Gradient
<MDScreen>:
    canvas.before:
        Color:
            rgba: get_color_from_hex("062636")  # Top color
        Rectangle:
            pos: self.pos
            size: self.width, self.height * 2 / 3

        Color:
            rgba: get_color_from_hex("010B0F")  # Bottom color
        Rectangle:
            pos: self.x, self.y + self.height * 2 / 3
            size: self.width, self.height / 3

    # Rest of your screen content...
    # (Images, labels, etc.)

"""


class Test(App):
    Window.size = (1280, 720)
    def build(self):
        return Builder.load_string(kv)

    def on_stop(self):
        self.root.ids.box.export_to_png("gradient.png")


Test().run()
