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
        '''''

        #LDR Value
       # LDR = arduino.getLDR()   ##this func returns the iteration num
        #speed = arduino.getSpeed()

        
        #battery reading

        battery = arduino.getBatteryCapacity()
        batteryStr = f"{battery}%"
        batteryPercentageTxt = StringProperty(batteryStr)  ##gets sent to GUI

        if battery < 25:
            print("Low battery, head to charging station")
            # battery img source change
'''''
        ##############################################

        #Speed Reading
        speed = self.arduino.getSpeed()
        self.speedStr = f"{speed} KM/H"

        volts = self.arduino.getVoltage()
        self.voltsStr = f"{volts} V"

        current = self.arduino.getVoltage()
        self.currentStr = f"{current} A"

        battery = self.arduino.getBatteryCapacity()
        self.batteryStr = f"{battery} %"

        rangeLeft = self.arduino.getRange()
        self.rangeLeftStr = f"{rangeLeft} KM"

        distanceTravelled = self.arduino.getDistanceTravelled()
        self.distanceTravelledStr = f"{distanceTravelled} KM"



        #smoke sensor
        self.smoke = self.arduino.getSmoke()

        #door
        self.doorOpen = self.arduino.getRightDoorSensor() | self.arduino.getLeftDoorSensor()
        #self.doorOpen = self.arduino.getRightDoorSensor()
        #trunk
        self.trunkOpen = self.arduino.getTrunkSensor()

        self.seatBelt = self.arduino.getSeatBeltSensor()

        self.sitting = self.arduino.getSeatSensor()
       # self.isNightTime = self.arduino.getLDR()
        self.stWheel = self.arduino.getStWheel()


    def getTemp(self):
        temp = self.arduino.getAnalogueReading("temperature",self.arduino.tempPIN)
        self.tempStr = f"{temp} Cvbnm"
        return self.tempStr

    def getSpeed(self):
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