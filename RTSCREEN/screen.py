import time
from threading import Thread
from multiprocessing import Process, Queue, Pool
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.clock import Clock
from kivy.core.window import Window
from MediatorModule import Mediator

smokeOffSrc = 'Images/smoke.png'
smokeOnSrc = 'Images/smokeRed.png'

doorSrc = 'Images/door.png'
doorOpenSrc = 'Images/doorsRed.png'

seatSrc = 'Images/seat.png'
seatOnSrc = 'Images/seatBlue.png'

seatBeltSrc = 'Images/seatBelt.png'
seatBeltOnSrc = 'Images/seatBeltRed.png'

daytimeSrc = 'Images/sun.png'
daytimeOnSrc = 'Images/sunBlue.png'

nighttimeSrc = 'Images/moon.png'
nighttimeOnSrc = 'Images/moonBlue.png'

stWheelSrc = 'Images/stWheel.png'
stWheelOnSrc = 'Images/stWheelRed.png'

class runApp(MDApp):
    Window.size = (1280, 720)
    screen_manager = ScreenManager(transition=SlideTransition(duration=1.5))
    # Load splashScreen.kv and runApp.kv files
    splash_screen = None
    run_app_screen = None
    #src must be in vars, slows down the function otherwise



    mediator = Mediator()

    def __init__(self, **kwargs):
        super(runApp, self).__init__(**kwargs)
        self.running = True  # Flag to control the loop
        self.StartGetArduinoValues()
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

    def StartGetArduinoValues(self):
        Thread(target=self.getArduinoValues).start()
    def getArduinoValues(self):
        while self.running:
            Clock.schedule_once(self.updateText, 0)
            time.sleep(0.25)

    def toggleIndicators(self, id, getterFunc, srcOff, srcOn):
        ID = id
        Value = getterFunc
        if (Value):
            ID.source = srcOn
        else:
            ID.source = srcOff

    def changeGUItext(self,sensorName):
        try:
            text = self.mediator.getSensor(f'{sensorName}') # get updated value
        except Exception as e:
            print(f"Error:{e}")

        id = self.run_app_screen.ids[f"{sensorName}" + "ID"]
        id.text = text

    def updateText(self, dt):
        self.changeGUItext('speed')




        #self.toggleIndicators(smokeID,smokeValue,smokeOffSrc,smokeOnSrc)
        #self.toggleIndicators(doorID,doorOpenValue,doorSrc,doorOpenSrc)
        #self.toggleIndicators(trunkID,trunkOpenValue,trunkSrc,trunkOpenSrc)
        #self.toggleIndicators(seatID,sittingValue,seatSrc,seatOnSrc)
        #self.toggleIndicators(seatBeltID,seatBeltValue,seatBeltSrc,seatBeltOnSrc)
        #self.toggleIndicators(stWheelID,stWheelValue,stWheelSrc,stWheelOnSrc)
        #self.toggleIndicators(moonID,timeValue,seatSrc,seatOnSrc) #sun/moon


    def stop(self):
        self.running = False  # Stop the infinite loop



if __name__ == '__main__':
    with Pool(processes=4) as pool:
        pass
    runApp().run()