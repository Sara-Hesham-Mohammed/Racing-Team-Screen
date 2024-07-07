from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string('''
<CircularProgressBar>:
    canvas:
        Color:
            rgba: self.color[0], self.color[1], self.color[2], 0.05
        Line:
            circle: (self.center_x, self.center_y, self.radius + 8, 180, 180 + self.angle)
            width: self.line_width + 16
        Color:
            rgba: self.color[0], self.color[1], self.color[2], 0.1
        Line:
            circle: (self.center_x, self.center_y, self.radius + 6, 180, 180 + self.angle)
            width: self.line_width + 12
        Color:
            rgba: self.color[0], self.color[1], self.color[2], 0.2
        Line:
            circle: (self.center_x, self.center_y, self.radius + 4, 180, 180 + self.angle)
            width: self.line_width + 8
        Color:
            rgba: self.color[0], self.color[1], self.color[2], 0.4
        Line:
            circle: (self.center_x, self.center_y, self.radius + 2, 180, 180 + self.angle)
            width: self.line_width + 4
        Color:
            rgba: self.color
        Line:
            circle: (self.center_x, self.center_y, self.radius, 180, 180 + self.angle)
            width: self.line_width
''')

class CircularProgressBar(Widget):
    value = NumericProperty(0) #progress from 0 to 100 value will change it to take input from
    #the speed and battery
    line_width = NumericProperty(2)
    color = [0.98,0.058,0.75,1]  #[252/255, 15/255, 192/255, 1] 
    #is RGB(252, 15, 192) converted to RGBA
    radius = NumericProperty(163)
    angle = NumericProperty(0)

    def __init__(self, **kwargs): #done like this rn calls update every interval of 0.1 to update
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_angle, 0.1)

    def update_angle(self, dt):
        # will just call the self.value which has a diff value now cz of speed
        self.angle = (self.value / 100) * 360
