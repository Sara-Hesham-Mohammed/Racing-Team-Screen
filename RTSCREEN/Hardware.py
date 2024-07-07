import time
from pyfirmata import Arduino,util, ArduinoMega

class ArduinoClass:
    def __init__(self):
        self.comNum = None


    def setBoard(self,comNum):
        self.board = ArduinoMega(comNum)

    def getBoard(self):
        return self.board

    def setComNum(self,comNum):
        self.comNum = comNum

    def getComNum(self):
        return self.comNum





class Sensor:

    def __init__(self):
        self.board = None

    def setSensor(self, type, num, io):
        self.sensor = self.board.get_pin(f'{type}:{num}:{io}')

    def getSensor(self):
        return self.sensor