import random
import time
from pyfirmata import ArduinoMega, util, Board

class ArduinoClass:

    def __init__(self):
        self.iterationNum = 0
        # initialize board and COM Number
        self.board = ArduinoMega('COM10')

        ########### DIGITAL PINS ##############
        # 0 and 1 digital pins are for RX TX, so we start from pin 2
        self.stWheel = self.board.get_pin('d:2:i')

        self.seatSensor = self.board.get_pin('d:5:i')
        self.smoke = self.board.get_pin('d:6:i')

        # lights
        self.highBeam = self.board.get_pin('d:7:i')
        self.lowBeam = self.board.get_pin('d:8:i')
        self.leftBlinker = self.board.get_pin('d:3:i')
        self.rightBlinker = self.board.get_pin('d:4:i')

        # doors / trunk / hood
        self.leftDoorSensor = self.board.get_pin('d:9:i')
        self.rightDoorSensor = self.board.get_pin('d:10:i')

        self.trunkSensor = self.board.get_pin('d:11:i')
        self.hoodSensor = self.board.get_pin('d:12:i')

        self.seatBeltSensor = self.board.get_pin('d:13:i')

        ########### ANALOGUE PINS, check if they all need to be input or output###############
        self.ldr = self.board.get_pin('a:0:i')

        self.speed = self.board.get_pin('a:1:i')  # initialized to random number for now

        self.temperature = self.board.get_pin('a:2:i')  # initialized to random number for now

        self.oilLevel = self.board.get_pin('a:3:i')  # initialized to random number for now

        self.current = self.board.get_pin('a:4:i')  # initialized to random number for now
        # Current and volt from battery and get power
        self.voltage = self.board.get_pin('a:5:i')  # initialized to random number for now

        self.sensor = None

        #arduino mini layout
        miniLayout = {
            'digital': tuple(range(20)),  # Digital pins 0 to 19
            'analog': tuple(range(6)),  # Analog pins 0 to 5
            'pwm': (3, 5, 6, 9, 10, 11),  # PWM pins
            'use_ports': True,  # If ports are used
            'disabled': (0, 1),  # Disabled pins (usually RX and TX)]
        }

        #miniBoard = Board('COM10', layout=miniLayout) # to be used instead of mega board

        it = util.Iterator(self.board)
        it.start()


    #sensor setter and getter for dynamic changes [test here then move to sensors class and test]
    def setSensor(self,type,num,io):
        self.sensor = self.board.get_pin(f'{type}:{num}:{io}')

    def getSensor(self):
        return self.sensor


    ################# Getters for pin num and readings ################
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
        print(f"Digital Reading: {reading}")
        return reading

   #needs fixing and updating
    def getLDR(self):
        ldrValue = self.getAnaloguePinReading(self.getPIN(self.ldr)) * 1023  # intensity

        print(f"LDR Intensity: {ldrValue}")
        if ldrValue > 100:  # closer to 1023 is darkness
            print("Dark out, LED ON")
            # self.led.write(True)
            self.iterationNum += 1
            print(f"Iteration Num:{self.iterationNum}")  # just for debugging
        else:  # closer to 0 is light outside
            # self.led.write(False)
            print("Light out, LED OFF")
    #Calculations => Speed and distance travelled

    #for testing ONLYYY
    def randomChoice(self):
        return random.choice([0, 1])

    ################# Speed Functions and calculations ################
    def pulseCount(self):
        count = 0
        interval = 2  # seconds

        startTime = time.time()

        while time.time() - startTime < interval:
            #pulse = self.getDigitalPinReading(self.getPIN(self.speed))
            pulse = self.randomChoice()
            if (pulse == 1):
                count += 1

            time.sleep(0.1)  # Sleep for a short duration to prevent a tight loop

        return {'count': count, 'startTime': startTime}

    def calcSpeed(self):
        pulseCountRes = self.pulseCount()
        print(f"pulseCountRes: {pulseCountRes}")

        count = pulseCountRes['count']  # Extract the count from the dictionary
        print(f"Count: {count}")
        rpm = pulseCountRes['count']
        r = 43.18 / 2
        speed = (2 * 3.142 * r / 60) * rpm
        return speed

    def getSpeed(self):
        return self.calcSpeed()

    ################# Distance travelled ################
    def distanceTravelled(self):
        pulseCountRes = self.pulseCount()
        rpm = pulseCountRes['count']
        startTime = pulseCountRes['startTime']
        r = 43.18 / 2
        circumference = 2 * 3.142 * r
        timePassed= time.time() - startTime # do the actual eqn
        distTrav = circumference*rpm*timePassed
        return distTrav

    def getDistanceTravelled(self):
        return self.distanceTravelled()
    ############# Range Left #############
    def rangeLeft(self):
        batteryPercentage = self.getBatteryPercentage()
        # for now placeholder till a calc is given
        return batteryPercentage

    def getRangeLeft(self):
        return self.rangeLeft()


    ################ Battery Percentage ################
    def getBatteryPercentage(self):
        # get curent, volt and power as well as the capacity and milage
        # the *100 is placeholder till get ac equation
        batteryPercent = self.getAnaloguePinReading(self.voltage)
        return batteryPercent
    ################ Power ################
    def getPower(self):
        self.power = self.current * self.voltage
        return self.power

    def getCurrent(self):
        #return vc.get_current()
        return 0 # placeholder
    def getVoltage(self):
        return 0 # placeholder
        #return vc.get_voltage()