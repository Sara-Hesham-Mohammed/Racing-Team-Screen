import time
from threading import Thread
from multiprocessing import Process, Queue, Pool
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.clock import Clock
from kivy.core.window import Window
from MediatorModule import Mediator

class runApp(MDApp):
    Window.size = (1280, 720)
    screen_manager = ScreenManager(transition=SlideTransition(duration=1.5))
    # Load splashScreen.kv and runApp.kv files
    splash_screen = None
    run_app_screen = None
    mediator = Mediator()

    def __init__(self, **kwargs):
        super(runApp, self).__init__(**kwargs)
        self.running = True  # Flag to control the loop
        self.StartArduinoThread()
        self.splash_screen = Builder.load_file("splashScreen.kv")
        self.run_app_screen = Builder.load_file("runApp.kv")

    def build(self):
        self.title = "BUE RACING TEAM"
        self.screen_manager = ScreenManager(transition=SlideTransition(duration=4))

        # Add screens to the screen manager
        self.screen_manager.add_widget(self.splash_screen)

        self.screen_manager.add_widget(self.run_app_screen)

        # Print screen names for debugging (optional)
        print(self.screen_manager.screen_names)

        return self.screen_manager
    def on_start(self):
        # Delay time for splash screen before transitioning to main screen
            Clock.schedule_once(self.change_screen, 12)
    def change_screen(self, dt):
        self.screen_manager.current = "runApp"

    def StartArduinoThread(self):
        Thread(target=self.getArduinoValues).start()
    def getArduinoValues(self):
        while self.running:
            Clock.schedule_once(self.updateText, 0)
            time.sleep(0.25)

    def changeGUItext(self,sensorName):
        try:
            textInit = self.mediator.getSensor(f'{sensorName}') # get updated value
            temp =float(textInit)*100
            text = str(temp)
            text = f"{temp:.2f}"
        except Exception as e:
            print(f"Error:{e}")

        id = self.run_app_screen.ids[f"{sensorName}" + "ID"]
        id.text = text


    def changeGUIicons(self,sensorName):
        id = self.run_app_screen.ids[f"{sensorName}" + "ID"]
        value = self.mediator.getSensor(f'{sensorName}')
        print(f"Smoke Value:{value}")
        onSrc=f'Images/{sensorName}Red.png'
        offSrc =f'Images/{sensorName}.png'
        if (value):
            id.source = onSrc
        else:
            id.source = offSrc

    def updateText(self, dt):
        try:
            self.changeGUItext('speed')
        except Exception as e:
            print(f"Error:{e}. Couldn't get speed reading")

        try:
            self.changeGUItext('temperature')
        except Exception as e:
            print(f"Error:{e}. Couldn't get temperature reading")

        self.changeGUIicons('smoke')
    def stop(self):
        self.running = False  # Stop the infinite loop

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        pass
    runApp().run()