import time
import threading
from threading import Thread
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.clock import Clock
from kivy.core.window import Window
from circularprogressbar import CircularProgressBar 
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

        print(f"Active Thread Count: {threading.active_count()}")
        print(f"Active Threads: {threading.enumerate()}")

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
            Clock.schedule_interval(self.update_progress, 0.1)
        
    def update_progress(self, dt):
        progress1 = self.run_app_screen.ids.circular_progress1
        progress2 = self.run_app_screen.ids.circular_progress2
        if progress1.value < 100 or progress2.value < 100:
            progress1.value += 1
            progress2.value += 1
        else:
            progress1.value = 0
            progress2.value = 0
    
    def change_screen(self, dt):
        self.screen_manager.current = "runApp"

    def StartArduinoThread(self):
        Thread(target=self.getArduinoValues).start()
        #Thread(target=self.getSpeed()).start()

    def getArduinoValues(self):
        while self.running:
            Clock.schedule_once(self.updateText, 0)
            time.sleep(0.25)

    def getSpeed(self):
        return self.mediator.getCalculatedSensor('speed')

    # gets ANALOG only, change to ask for analog or digital if needed
    def changeGUItext(self,sensorName):
        try:
            reading = self.mediator.getAnalogueSensor(f'{sensorName}')#change this
            transformedReading = self.mediator.transform(reading,100)
            text = str(transformedReading)
            text = f"{transformedReading:.2f}"
        except Exception as e:
            print(f"Error:{e}")

        id = self.run_app_screen.ids[f"{sensorName}" + "ID"]
        print(f"ID: {id}")
        id.text = text

    #gets DIGITAL only, change to ask for analog or digital if needed
    def changeGUIicons(self, sensorName):
        id = self.run_app_screen.ids[f"{sensorName}" + "ID"]
        value = self.mediator.getDigitalSensor(f'{sensorName}')
        # Ensure value is a boolean by converting from string
        valueStr = str(value).strip().lower()  # Normalize the string for comparison
        value2 = valueStr in ['true', '1', 'yes']  # Define the criteria for True

        # Change the onsrc depending on if it is critical (red img) or reg (blue img)
        onSrc = f"Images/{sensorName}Red.png"
        offSrc = f'Images/{sensorName}.png'

        if value2: #to check for the opp value write: if not value
            id.source = onSrc
        else:
            id.source = offSrc

    def updateText(self, dt):


        try:
            self.changeGUIicons('smoke')
        except Exception as e:
            print(f"Error:{e}. Couldn't get smoke reading")

        try:
            self.getSpeed()
        except Exception as e:
            print(f"Error:{e}. Couldn't get speed reading")



    def stop(self):
        self.running = False  # Stop the infinite loop

if __name__ == '__main__':

    runApp().run()