from pyfirmata import Arduino,util, ArduinoMega


class Arduino:

    iterationNum = 0
    #initialize board and COM Number
    #boardUno = Arduino('COM9')
    board = ArduinoMega('COM10')

    ########### DIGITAL PINS, check if they all need to be input or output###############
    #initialize pins(digital/pwm/analogue) and if they're input or output
    #led = board.get_pin('d::o')
    #ledPIN =

    # indicators
    # 1st  2 digital pins are for RX TX comms, so we start from pin 3
    stWheel = board.get_pin('d:2:i')
    stWheelPIN = 2

    leftBlinker = board.get_pin('d:3:i')
    leftBlinkerPIN = 3

    rightBlinker = board.get_pin('d:4:i')
    rightBlinkerPIN = 4

    # digital sensors
    seatSensor = board.get_pin('d:5:i')
    seatSensorPIN = 5

    smokeSensor = board.get_pin('d:6:i')
    smokeSensorPIN = 6

    # lights
    highBeam = board.get_pin('d:7:i')
    highBeamPIN = 7

    lowBeam = board.get_pin('d:8:i')
    lowBeamPIN = 8

    # doors / trunk / hood
    leftDoorSensor = board.get_pin('d:9:i')
    leftDoorSensorPIN = 9

    rightDoorSensor = board.get_pin('d:10:i')
    rightDoorSensorPIN = 10

    trunkSensor = board.get_pin('d:11:i')
    trunkSensorPIN = 11

    hoodSensor = board.get_pin('d:12:i')
    hoodSensorPIN = 12

    seatBeltSensor = board.get_pin('d:13:i')
    seatBeltSensorPIN = 13

    ########### ANALOGUE PINS, check if they all need to be input or output###############
    ldr = board.get_pin('a:0:i')
    ldrPIN = 0

    speed = board.get_pin('a:1:i') #initialized to random number for now
    speedPIN=1

    temperature = board.get_pin('a:2:i')  # initialized to random number for now
    tempPIN = 2

    oilLevel = board.get_pin('a:3:i')  # initialized to random number for now
    oilLevelPIN = 3

    #cuurent and volt same pin and calculated? or diff pins???
    current = board.get_pin('a:4:i')  # initialized to random number for now
    currentPIN = 4

    # Current and volt from battery and get power

    voltage = board.get_pin('a:5:i')  # initialized to random number for now
    voltPIN = 5

    #calculated from battery %
    power = None  # calculated from Current and volt
    batteryCapacity = None  # battery capacity left
    rangeLeft = None

    # starting iterator, necessary for analogue values?
    it = util.Iterator(board)
    it.start()

    # ANALOGUE values getter function
    def getAnalogueReading(self,sensorName,sensorPIN):
        self.board.analog[sensorPIN].enable_reporting()
        value = self.board.analog[sensorPIN].read()
        return value

    ######################################### ANALOGUE GETTER FUNCTIONS ###################################

    def getLDR(self):
        ldrValue = self.getAnalogueReading(self.ldr, self.ldrPIN)*1023 #intensity

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
        speedValue = self.getAnalogueReading(sensorName=self.speed,sensorPIN=self.speedPIN)
        print(f"Speed Intensity: {speedValue}")
        return speedValue*100

    def getBatteryCapacity(self):
        #get cuurent, volt and power as well as the capacity and milage
        #the *100 is placeholder till get ac equation
        batteryPercent = self.getVoltage()
        return int(batteryPercent*100)

    def getVoltage(self):
        voltValue = self.getAnalogueReading(sensorName=self.voltage,sensorPIN=self.voltPIN)
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
        currentValue = self.getAnalogueReading(self.current,self.currentPIN)
        return currentValue

    def getOilLevel(self):
        oilLvlVaL = self.getAnalogueReading(self.oilLevel,self.oilLevelPIN)
        return oilLvlVaL

    def getTemperature(self):
       tempVal =  self.getAnalogueReading(self.temperature,self.tempPIN)
       return tempVal

    ######################################### DIGITAL GETTER FUNCTIONS ###################################

    def getSmoke(self):
        smokeVal = self.board.digital[self.smokeSensorPIN].read()
        return smokeVal

    def getHighBeam(self):
        highBeamVal = self.board.digital[self.highBeamPIN].read()
        return highBeamVal

    def getLowBeam(self):
        lowBeamVal = self.board.digital[self.lowBeamPIN].read()
        return lowBeamVal

    def getSeatSensor(self):
        seatVal = self.board.digital[self.seatSensorPIN].read()
        return seatVal

    def getSeatBeltSensor(self):
        seatVal = self.board.digital[self.seatBeltSensorPIN].read()
        return seatVal

    def getRightDoorSensor(self):
        rightDoorVal = self.board.digital[self.rightDoorSensorPIN].read()
        return rightDoorVal

    def getLeftDoorSensor(self):
        leftDoorVal = self.board.digital[self.leftDoorSensorPIN].read()
        return leftDoorVal

    def getHoodSensor(self):
        hoodVal = self.board.digital[self.hoodSensorPIN].read()
        return hoodVal

    def getTrunkSensor(self):
        trunkVal = self.board.digital[self.trunkSensorPIN].read()
        return trunkVal

    def getStWheel(self):
        stWheelVal = self.board.digital[self.stWheelPIN].read()
        return stWheelVal