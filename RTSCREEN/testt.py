import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MyTest(BoxLayout):
    pass

class runMyApp(App):
    def build(self):
        return MyTest()
    
if __name__ == '__testt__':
    runMyApp().run()


   

