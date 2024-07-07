import time

from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from ArduinoClass import ArduinoClass



class Mediator:
    arduino = ArduinoClass()

    def __init__(self):
        pass

    def getSensorName(self,specificKey):
        if specificKey in vars(self.arduino):
            print(f"Sensor: {specificKey}")
        else:
            print(f"{specificKey} does not exist in the instance")

        return specificKey

    def getAnalogueSensor(self,sensorName):
        sensorDetails =  getattr(self.arduino, sensorName, None)
        PIN = self.arduino.getPIN(sensorDetails)
        sensorVal = self.arduino.getAnaloguePinReading(PIN)
        sensorStr = f"{sensorVal}"
        return sensorStr


    def getDigitalSensor(self,sensorName):
        sensorDetails =  getattr(self.arduino, sensorName, None)
        PIN = self.arduino.getPIN(sensorDetails)
        sensorVal = self.arduino.getDigitalPinReading(PIN)
        print(f"Sensor: {sensorVal}")
        sensorStr = f"{sensorVal}"
        return sensorStr

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

    def transform(self,reading,correctionFactor):
        transformedReading =float(reading)*correctionFactor
        return transformedReading

    def getCalculatedSensor(self,sensorName):
        switch = {
            'speed': self.arduino.getSpeed(),
            'rangeLeft': self.arduino.getRangeLeft(),
            'distanceTravelled': self.arduino.getDistanceTravelled(),
            'batteryPercentage': self.arduino.getBatteryPercentage(),
            'current':self.arduino.getCurrent(),
            'voltage':self.arduino.getVoltage()
        }
        return switch[sensorName]




    #####################################################################################