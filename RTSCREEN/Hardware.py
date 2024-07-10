import time
from pyfirmata import Arduino,util, ArduinoMega, ArduinoNano

class ArduinoClass:
    def __init__(self):
        self.comNum: int
        self.board = Arduino(None)


    def setBoard(self,comNum, type):

        if type == "nano":
            self.board = ArduinoNano(comNum)
        elif type == "mega":
            self.board = ArduinoMega(comNum)
        elif type == "uno":
            self.board = Arduino(comNum)
        else:
            print("Invalid. Choose nano, mega or uno.")

    def getBoard(self):
        return self.board
    def startIterator(self):
        if self.board is not None:
            it = util.Iterator(self.board)
            it.start()

        else:
            print("Board not set")
            return
    def setComNum(self,comNum):
        self.comNum = comNum

    def getComNum(self):
        return self.comNum
    def setSensorPin(self,type,num,io):
        self.sensorPin = self.board.get_pin(f'{type}:{num}:{io}')
    def getSensorPin(self):
        return self.sensorPin

    def getPIN(self, sensor):
        sensorString = str(sensor)
        sensorPIN = sensorString[-1]
        return int(sensorPIN)
        # This reads from the Pins

    def getAnaloguePinReading(self, sensorPIN):
        self.board.analog[sensorPIN].enable_reporting()
        reading = self.board.analog[sensorPIN].read()
        return reading

    def getDigitalPinReading(self, sensorPIN):
        reading = self.board.digital[sensorPIN].read()
        # print(f"Digital Reading: {reading}")
        return reading


class Sensor:

    def __init__(self):
        self.board = ArduinoClass()

    def setSensor(self, type, num, io):
        self.sensor = self.board.setSensorPin(type, num, io)

    def getSensor(self):
        return self.sensor

    def setBoard(self,comNum, type):
        self.board.setBoard(comNum, type)

    def getBoard(self):
        return self.board




