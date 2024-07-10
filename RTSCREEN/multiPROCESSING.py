import multiprocessing
from multiprocessing import Pool
from Hardware import ArduinoClass, Sensor
import time

# Define a function to read from an Arduino and blink the built-in LED
def readArduino(port, lock):
    board = ArduinoClass()
    board.setBoard(port, 'mega')
    board.startIterator()
    analog_pin = board.getSensorPin()('a:0:i')  # Assuming you want to read from analog pin 0
    led_pin = board.getSensorPin()('d:13:o')   # Assuming digital pin 13 is the built-in LED

    while True:
        # Read the analog value
        with lock:
            value = analog_pin.read()
        if value is not None:
            print(f"Reading from {port}: {value}")

        # Blink the LED
        with lock:
            led_pin.write(1)  # Turn on the LED
        time.sleep(0.5)       # Adjust the sleep time as needed
        with lock:
            led_pin.write(0)  # Turn off the LED
        time.sleep(0.5)

# Define the main function to create processes
def main():
    startTime = time.time()
    lock = multiprocessing.Lock()
    arduinoPorts = ['COM10', 'COM3']  # Update with your actual ports
    processes = []

    # Create and start a process for each Arduino
    for port in arduinoPorts:
        p = multiprocessing.Process(target=readArduino, args=(port, lock))
        processes.append(p)
        p.start()

    # Join the processes to ensure they complete
    for p in processes:
        p.join()

    endTime = time.time() - startTime
    print(f"Time taken: {endTime}")

if __name__ == "__main__":
    main()
