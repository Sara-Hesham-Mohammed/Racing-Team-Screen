import time
from concurrent.futures import ThreadPoolExecutor
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
    mediator = Mediator()

    def __init__(self, **kwargs):
        super(runApp, self).__init__(**kwargs)
        self.running = True  # Flag to control the loop
        self.threadPool = ThreadPoolExecutor(8)

    def build(self):
        self.title = "BUE RACING TEAM"
        self.splash_screen = Builder.load_file("splashScreen.kv")
        self.run_app_screen = Builder.load_file("runApp.kv")
        self.screen_manager.add_widget(self.splash_screen)
        self.screen_manager.add_widget(self.run_app_screen)
        return self.screen_manager

    def on_start(self):
        # Delay time for splash screen before transitioning to main screen
        Clock.schedule_once(self.change_screen, 3)
        Clock.schedule_interval(self.update_progress, 0.1)
        # Start updating Arduino values periodically
        Clock.schedule_interval(self.update_arduino_values, 0.5)

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

    def update_arduino_values(self, dt):
        # Submit tasks to the thread pool to avoid blocking the main thread
        self.threadPool.submit(self.getArduinoValues)

    def getArduinoValues(self):
        readings = {
            "speed": self.mediator.getCalculatedReading("speed"),
            "distanceTravelled": self.mediator.getCalculatedReading("distanceTravelled"),
            "current": self.mediator.getCalculatedReading("current"),
            "voltage": self.mediator.getCalculatedReading("voltage"),
            "batteryPercentage": self.mediator.getCalculatedReading("batteryPercentage"),
            "temperature": self.mediator.getDigitalSensor("temperature"),
            "seatSensor": self.mediator.getAnalogueSensor("seatSensor")
        }
        Clock.schedule_once(lambda dt: self.updateText(readings), 0)

    def updateText(self, readings):
        try:
            self.changeGUIicons('smoke')
        except Exception as e:
            print(f"Error: {e}. Couldn't get smoke reading")

        for sensorName, reading in readings.items():
            self.changeGUItext(sensorName, reading)

    def changeGUItext(self, sensorName, reading):
        try:
            if sensorName == "speed":
                transformedReading = float(reading) / 1000
                text = f"{transformedReading:.2f}"
            else:
                text = str(reading)
            id = self.run_app_screen.ids[f"{sensorName}ID"]
            id.text = text
        except Exception as e:
            print(f"Error in change GUI text: {e}")

    def changeGUIicons(self, sensorName):
        id = self.run_app_screen.ids[f"{sensorName}ID"]
        value = self.mediator.getDigitalSensor(f'{sensorName}')
        # Ensure value is a boolean by converting from string
        valueStr = str(value).strip().lower()  # Normalize the string for comparison
        value2 = valueStr in ['true', '1', 'yes']  # Define the criteria for True

        # Change the onsrc depending on if it is critical (red img) or reg (blue img)
        onSrc = f"Images/{sensorName}Red.png"
        offSrc = f'Images/{sensorName}.png'

        if value2:  # to check for the opp value write: if not value
            id.source = onSrc
        else:
            id.source = offSrc

    def stop(self):
        self.running = False  # Stop the infinite loop
        self.threadPool.shutdown(wait=True)  # Shutdown the thread pool

if __name__ == '__main__':
    runApp().run()
