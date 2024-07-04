from pyfirmata import Arduino,util, ArduinoMega
from multiprocessing import Queue

class Arduino:

    def __init__(self):
        pass

    iterationNum = 0
    #initialize board and COM Number\
    board = ArduinoMega('/dev/cu.IC-HB1129-SerialPort')

    ########### DIGITAL PINS ##############
    #initialize pins(digital/pwm/analogue) and if they're input or output

    # 0 and 1 digital pins are for RX TX, so we start from pin 2
    stWheel = board.get_pin('d:2:i')

    seatSensor = board.get_pin('d:5:i')
    smoke = board.get_pin('d:8:i')


    # lights
    highBeam = board.get_pin('d:7:i')


    leftBlinker = board.get_pin('d:3:i')
    rightBlinker = board.get_pin('d:4:i')

    #lowBeam = board.get_pin('d:8:i')

    # doors / trunk / hood
    leftDoorSensor = board.get_pin('d:9:i')
    rightDoorSensor = board.get_pin('d:10:i')

    trunkSensor = board.get_pin('d:11:i')
    hoodSensor = board.get_pin('d:12:i')

    seatBeltSensor = board.get_pin('d:13:i')


    ########### ANALOGUE PINS, check if they all need to be input or output###############
    ldr = board.get_pin('a:0:i')

    speed = board.get_pin('d:34:i') #initialized to random number for now

    temperature = board.get_pin('a:2:i')  # initialized to random number for now

    oilLevel = board.get_pin('a:3:i')  # initialized to random number for now

    current = board.get_pin('a:4:i')  # initialized to random number for now
    # Current and volt from battery and get power
    voltage = board.get_pin('a:5:i')  # initialized to random number for now



    def getPIN(self,sensor):
        sensorString = str(sensor)
        sensorPIN = sensorString[-1]
        return int(sensorPIN)

    # starting iterator, necessary for analogue values?
    it = util.Iterator(board)
    it.start()

    # ANALOGUE values getter function
    def getAnalogueReading(self,sensorPIN):
        self.board.analog[sensorPIN].enable_reporting()
        value = self.board.analog[sensorPIN].read()
        return value

    ######################################### ANALOGUE GETTER FUNCTIONS ###################################

    def getLDR(self):
        ldrValue = self.getAnaloguePinReading(self.getPIN(self.ldr))*1023 #intensity

        print(f"LDR Intensity: {ldrValue}")
        if ldrValue > 100:#closer to 1023 is darkness
            print("Dark out, LED ON")
            #self.led.write(True)
            self.iterationNum += 1
            print(f"Iteration Num:{self.iterationNum}") #just for debugging
        else:#closer to 0 is light outside
            #self.led.write(False)
            print("Light out, LED OFF")
    def getSpeed(self):
        # multiply by a factor
        speedValue = self.getAnaloguePinReading(self.getPIN(self.speed))
        return speedValue

    def getBatteryCapacity(self):
        #get cuurent, volt and power as well as the capacity and milage
        #the *100 is placeholder till get ac equation
        batteryPercent = self.getVoltage()
        return batteryPercent

    def getVoltage(self):
        voltValue = self.getAnaloguePinReading(self.getPIN(self.voltage))
        return voltValue

    def getDistanceTravelled(self):
        #add the distance calculations
        batteryCapacity = self.getBatteryCapacity()
        # assuming that 100 % will allow distance of 100km to be crossed
        distanceTravelled = 100 - batteryCapacity
        return distanceTravelled



    def getRangeLeft(self):
        batteryCapacity = self.getBatteryCapacity()
        #for now placeholder till a calc is given
        return batteryCapacity


    def getPower(self):
        self.power = self.current * self.voltage
        return self.power

    def getCurrent(self):
        # speed - needs to be multiplied by a factor cause the read() is from 0.0 to 1.0
        currentValue = self.getAnaloguePinReading(self.getPIN(self.current))
        return currentValue

    def getOilLevel(self):
        oilLvlVaL = self.getAnaloguePinReading(self.getPIN(self.oilLevel))
        return oilLvlVaL

    def getTemperature(self):
       tempVal =  self.getAnaloguePinReading(self.getPIN(self.temperature))
       return tempVal

    def getAnalogue(self):
        pass

    ######################################### DIGITAL GETTER FUNCTIONS ###################################


    #This reads from the Pins
    def getAnaloguePinReading(self,sensorPIN):
        self.board.analog[sensorPIN].enable_reporting()
        reading = self.board.analog[sensorPIN].read()
        return reading

    def getDigitalPinReading(self,sensorPIN):
        reading = self.board.digital[sensorPIN].read()
        return reading

    #the hard coded ones

    def getSmoke(self):
        smokeVal = self.board.digital[self.getPIN(self.smokeSensor)].read()
        return smokeVal

    def getHighBeam(self):
        highBeamVal = self.board.digital[self.getPIN(self.highBeam)].read()
        return highBeamVal

    def getLowBeam(self):
        lowBeamVal = self.board.digital[self.getPIN(self.lowBeam)].read()
        return lowBeamVal

    def getSeatSensor(self):
        seatVal = self.board.digital[self.getPIN(self.seatSensor)].read()
        return seatVal

    def getSeatBeltSensor(self):
        seatVal = self.board.digital[self.getPIN(self.seatBeltSensor)].read()
        return seatVal

    def getRightDoorSensor(self):
        rightDoorVal = self.board.digital[self.getPIN(self.rightDoorSensor)].read()
        return rightDoorVal
