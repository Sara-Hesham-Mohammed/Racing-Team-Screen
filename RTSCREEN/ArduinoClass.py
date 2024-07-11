import random
import time
import threading
from threading import Thread
from pyfirmata import ArduinoMega, util, Board, ArduinoNano, Arduino

class ArduinoClass:

    def __init__(self):

        priority: int
        self.iterationNum = 0 #smth for LDR
        # initialize board and COM Number
        self.board = ArduinoMega('COM10')

        ########### DIGITAL PINS ##############
        # 0 and 1 digital pins are for RX TX, so we start from pin 2
        self.stWheel = self.board.get_pin('d:2:i')

        self.seatSensor = self.board.get_pin('d:5:i')
        self.smoke = self.board.get_pin('d:6:i')

        # lights
        self.leftBlinker = self.board.get_pin('d:3:i')
        self.rightBlinker = self.board.get_pin('d:4:i')
        self.highBeam = self.board.get_pin('d:7:i')
        self.lowBeam = self.board.get_pin('d:8:i')

        # doors / trunk / hood
        self.leftDoorSensor = self.board.get_pin('d:9:i')
        self.rightDoorSensor = self.board.get_pin('d:10:i')

        self.trunkSensor = self.board.get_pin('d:11:i')
        self.hoodSensor = self.board.get_pin('d:12:i')

        self.seatBeltSensor = self.board.get_pin('d:13:i')

        ########### ANALOGUE PINS, check if they all need to be input or output###############
        self.ldr = self.board.get_pin('a:0:i')

        #self.speed = self.board.get_pin('a:1:i')  # initialized to random number for now
        self.speed = self.board.get_pin('d:31:i')  # initialized to random number for now

        self.temperature = self.board.get_pin('a:2:i')  # initialized to random number for now

        self.oilLevel = self.board.get_pin('a:3:i')  # initialized to random number for now

        self.current = self.board.get_pin('a:4:i')  # initialized to random number for now
        # Current and volt from battery and get power
        self.voltage = self.board.get_pin('a:5:i')  # initialized to random number for now

        self.sensor = None

        it = util.Iterator(self.board)
        it.start()

        print(f"Active Thread Count: {threading.active_count()}")

        try:
            pulseCountThread =  threading.Thread(target=self.pulseCount, name="Pulse Count Thread")
            pulseCountThread.daemon = True
            pulseCountThread.start()

        except Exception as e:
            print(f"Could not start thread: {e}")

    #sensor setter and getter for dynamic changes [test here then move to sensors class and test]
    def setSensor(self,type,num,io):
        self.sensor = self.board.get_pin(f'{type}:{num}:{io}')

    def getSensor(self):
        return self.sensor


    ################# Getters for pin num and readings ################
    # PROBLEMonly gets the last digit of the pin
    def getPIN(self,sensor):
        sensorString = str(sensor)
        sensorPIN = sensorString[-1]
        return int(sensorPIN)
    #This reads from the Pins
    def getAnaloguePinReading(self,sensorPIN):
        self.board.analog[sensorPIN].enable_reporting()
        reading = self.board.analog[sensorPIN].read()
        return reading

    def getDigitalPinReading(self,sensorPIN):
        reading = self.board.digital[sensorPIN].read()
        #print(f"Digital Reading: {reading}")
        return reading



    #Calculations => Speed and distance travelled
    ################# Speed Functions and calculations ################
    def pulseCount(self):
        count = 0
        interval = 2  # seconds

        startTime = time.time()

        while time.time() - startTime < interval:
            pulse = self.getDigitalPinReading(31)
            if (pulse == 1):
                count += 1
# Sleep for a short duration to prevent a tight loop
        time.sleep(0.1)
        return count

    def calcSpeed(self):
        pulseCountRes = self.pulseCount()
        print(f"pulseCountRes: {pulseCountRes}")
  # Extract the count from the dictionary
        rpm = pulseCountRes
        r = 43.18 / 2
        calcSpeed = (2 * 3.142 * r / 60) * rpm
        return calcSpeed

    ################# Distance travelled ################

    def getDistanceTravelled(self):
        pulseCountRes = self.pulseCount()
        rpm = pulseCountRes
        startTime = time.time()
        r = 43.18 / 2
        circumference = 2 * 3.142 * r
        timePassed = time.time() - startTime  # do the actual eqn
        distTrav = circumference * rpm * timePassed
        return distTrav
    ############# Range Left #############
    def getRangeLeft(self):
        batteryPercentage = self.getBatteryPercentage()
        # for now placeholder till a calc is given
        return batteryPercentage


    ################ Battery Percentage ################
    def getBatteryPercentage(self):
        # each battery capacity 80 AH so 160 total
        # ask how to get total V and the current capacity (or used capacity ay 7aga)
        currentCapacity = 1
        fullCapacity = 160 # Ah (ampere hours)
        totalVoltage = 56
        remainingCapacity = fullCapacity - currentCapacity
        voltage = self.getVoltage() # needs correction factor
        totalEnergy = totalVoltage * fullCapacity
        remainingEnergy = voltage * remainingCapacity #Wh (watt hours)
        batteryPercent =(remainingEnergy / totalEnergy) * 100 # chat GPT's calc

        batteryPercentage = (voltage/totalVoltage) * 100

        return batteryPercentage # OR batteryPercentage
    ################ Power ################
    def getPower(self):
        current = self.getCurrent()
        voltage = self.getVoltage()
        self.power = current * voltage
        return self.power

    def getCurrent(self):
        correctionFactor = 1  # to be given later
        pin = self.getPIN(self.current)
        reading = self.getAnaloguePinReading(pin)
        current = reading * correctionFactor
        return current  # placeholder




    def getVoltage(self):
        print("Getting Voltage.....")
        correctionFactor = 65.625 # to be given later
        pin = self.getPIN(self.voltage)
        reading = self.getAnaloguePinReading(pin)
        print(f"Voltage Reading: {reading}")
        voltage = float(reading) * correctionFactor

        print(f"Voltage: {voltage}")
        return voltage