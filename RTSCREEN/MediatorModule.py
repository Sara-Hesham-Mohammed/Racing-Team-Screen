from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
import Arduino



class Mediator:
    arduino = Arduino.Arduino()
    doorOpen = False
    trunkOpen = False
    hoodOpen = False
    isNightTime = False
    sitting = False
    seatBelt = False
    highBeam = False
    lowBeam = False
    lowBattery = False
    smoke = False
    stWheel = False
    LDR=0



    def __init__(self):
        self.speedStr = ''
        self.voltsStr = ''
        self.currentStr = ''
        self.batteryStr = ''
        self.distanceTravelledStr = ''
        self.rangeLeftStr = ''

    def getSensor(self,sensorName):
        sensor = getattr(self.arduino, sensorName, None)
        PIN = self.arduino.getPIN(sensor)
        sensorVal = self.arduino.getAnaloguePinReading(PIN)
        sensorStr = f"{sensorVal}"
        print(f"Sensor:{sensor}. Sensor String:{sensorStr}. Sensor Value:{sensorVal}")
        return sensorStr


    def getDigitalSensor(self,sensorName):
        sensor = getattr(self.arduino, sensorName, None)
        print(sensor)
        PIN = self.arduino.getPIN(sensor)
        sensorVal = self.arduino.getAnalogueReading(PIN)
        sensorStr = f"{sensorVal}"
        return sensorStr

    def getStWheel(self):
        return self.stWheel

    def toggleLights(self):
        # just transform the pic, actual logic is in Arduino class
        if self.LDR > 70:
            isNighttime = BooleanProperty(True)
            isDaytime = BooleanProperty(False)
            # img src = moon
        else:
            isNighttime = BooleanProperty(False)
            isDaytime = BooleanProperty(True)
            # img src = sun

    #####################################################################################