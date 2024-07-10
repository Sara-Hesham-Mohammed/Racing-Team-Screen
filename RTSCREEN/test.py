import multiprocessing
from pyfirmata import ArduinoMega, ArduinoNano, Arduino, util
import time

class ArduinoClass:
    def __init__(self):
        self.board = None
        self.sensors = []

    def setBoard(self, comNum, board_type):
        if board_type == "nano":
            self.board = ArduinoNano(comNum)
        elif board_type == "mega":
            self.board = ArduinoMega(comNum)
        elif board_type == "uno":
            self.board = Arduino(comNum)
        else:
            raise ValueError("Invalid board type. Choose nano, mega, or uno.")

    def getBoard(self):
        return self.board

    def startIterator(self):
        if self.board is not None:
            it = util.Iterator(self.board)
            it.start()
        else:
            raise ValueError("Board not set.")

    def addSensor(self, sensor):
        if isinstance(sensor, Sensor):
            self.sensors.append(sensor)
        else:
            raise ValueError("Only Sensor objects can be added")

    def getAnalogPinReading(self, sensor_pin):
        if self.board is not None:
            self.board.analog[sensor_pin].enable_reporting()
            return self.board.analog[sensor_pin].read()
        else:
            raise ValueError("Board not set.")

    def getDigitalPinReading(self, sensor_pin):
        if self.board is not None:
            return self.board.digital[sensor_pin].read()
        else:
            raise ValueError("Board not set.")

class Sensor:
    def __init__(self, arduino, pin_type, pin_num, io):
        self.arduino = arduino
        self.pin_type = pin_type
        self.pin_num = pin_num
        self.io = io
        self.sensor = None

    def setup(self):
        board = self.arduino.getBoard()
        self.sensor = board.get_pin(f"{self.pin_type}:{self.pin_num}:{self.io}")

    def read(self):
        if self.pin_type == 'a':
            return self.arduino.getAnalogPinReading(self.pin_num)
        else:
            return self.arduino.getDigitalPinReading(self.pin_num)

def readArduino(port, board_type, sensor_configs, lock):
    arduino = ArduinoClass()
    arduino.setBoard(port, board_type)
    arduino.startIterator()

    sensors = []
    for config in sensor_configs:
        sensor = Sensor(arduino, config['pin_type'], config['pin_num'], config['io'])
        sensor.setup()
        arduino.addSensor(sensor)
        sensors.append(sensor)

    while True:
        with lock:
            for sensor in sensors:
                value = sensor.read()
                if value is not None:
                    print(f"Reading from {port} (Pin {sensor.pin_num}): {value}")
        time.sleep(0.5)

def main():
    lock = multiprocessing.Lock()
    arduinos = [
        {'port': 'COM10', 'board_type': 'mega', 'sensors': [{'pin_type': 'a', 'pin_num': 0, 'io': 'i'}, {'pin_type': 'd', 'pin_num': 13, 'io': 'o'}]},
        {'port': 'COM3', 'board_type': 'mega', 'sensors': [{'pin_type': 'a', 'pin_num': 1, 'io': 'i'}, {'pin_type': 'd', 'pin_num': 12, 'io': 'i'}]}
    ]
    processes = []

    for arduinoConfig in arduinos:
        p = multiprocessing.Process(target=readArduino, args=(arduinoConfig['port'], arduinoConfig['board_type'], arduinoConfig['sensors'], lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
