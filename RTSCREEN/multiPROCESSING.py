import multiprocessing
from Hardware import ArduinoClass, Sensor
import time

# Define a function to read from an Arduino

def readArduino(port):
    nanoBoardA = ArduinoClass()
    nanoBoardA.setBoard(port,'nano')


    analog_pin = nanoBoardA.getSensorPin()('a:0:i')  # Assuming you want to read from analog pin 0

    while True:
        value = analog_pin.read()
        if value is not None:
            print(f"Reading from {port}: {value}")
        time.sleep(1)  # Adjust the sleep time as needed

# Define the main function to create processes
def main():
    arduinoPorts = ['COM9', 'COM10', 'COM11', 'COM12']  # Update with your actual ports
    processes = []

    # Create and start a process for each Arduino
    for port in arduinoPorts:
        p = multiprocessing.Process(target=readArduino, args=(port,))
        processes.append(p)
        p.start()

    # Join the processes to ensure they complete
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
