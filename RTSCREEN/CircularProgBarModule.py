from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout


class CircularProgressBar(AnchorLayout):
    text = StringProperty("0%")
    set_value = NumericProperty(0)
    value = NumericProperty(5)#percentage of completeness
    bar_color = ListProperty([75/255,199/255,217/255])#rgb colors
    bar_width = NumericProperty(5)#thickness of progress bar
    duration = NumericProperty(1.5)
    counter = 0

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    #function to increment and animate the progress bar and counter incrementation
    def animate(self,*args):
        # paran1 => CALLBACK = function that gets called every <timeout seconds>
        # paran1 => TIMEOUT = duration/value which is the current percentage (duration) divided by the overall total (value)
        Clock.schedule_interval(self.percent_counter,5)


    #function to increment the counter (just the counter var not the bar)
    def percent_counter(self,*args):
        if self.counter < self.value:
            self.counter +=1
            self.text = f"{self.counter}%"
            self.set_value = self.counter
        else:
            Clock.unschedule(self.percent_counter)

