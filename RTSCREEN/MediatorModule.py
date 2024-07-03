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



    def updateArduinoVals(self):
        #get ALL Arduino Values
        #Speed Reading


        #self.getTemp()
        pass
        #self.getSensor("temperature", self.arduino.getPIN(self.arduino.speed))

    def getSensor(self,PIN):
        sensor = self.arduino.getAnalogueReading(PIN)
        sensorStr = f"{sensor}"
        return sensorStr

    def getTemp(self):
        temp = self.arduino.getAnalogueReading(self.arduino.getPIN(self.arduino.temperature))
        self.tempStr = f"{temp} C"
        return self.tempStr

    def getSpeed(self):
        speed = self.arduino.getSpeed()
        self.speedStr = f"{speed} KM/H"
        return self.speedStr

    def getVoltage(self):
        return self.voltsStr
    def getCurrent(self):
        return self.currentStr

    def getBatteryCapacity(self):
        return self.batteryStr
    def getDistanceTravelled(self):
        return self.distanceTravelledStr

    def getRange(self):
        return self.rangeLeftStr

    def getSmoke(self):
        return self.smoke

    def getDoorOpen(self):
        return self.doorOpen

    def getTrunkOpen(self):
        return self.trunkOpen

    def getHoodOpen(self):
        return self.hoodOpen

    def getSeatBelt(self):
        return self.seatBelt

    def getStWheel(self):
        return self.stWheel

    def getLDR(self):
        return self.LDR

    def getLowBattery(self):
        return self.lowBattery

    def getSitting(self):
        return self.sitting

    def getTime(self):
        return self.isNightTime


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