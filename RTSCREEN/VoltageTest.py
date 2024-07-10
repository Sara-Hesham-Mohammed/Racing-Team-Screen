from pyfirmata import ArduinoMega, util
from serial import SerialException

try:

    board = ArduinoMega('COM10')
    board.sp.timeout = 2

    print("Serial port opened successfully.")

    # Flush input and output buffers
    board.sp.flushInput()
    board.sp.flushOutput()

    # Your code to interact with the board
    # Example: Reading a voltage value from an analog pin
    it = util.Iterator(board)
    it.start()
    analog_pin = board.get_pin('a:0:i')  # Adjust pin as needed

    while True:
        voltage = analog_pin.read()
        if voltage is not None:
            print(f"Voltage Reading: {voltage * 5.0} V")
        board.pass_time(1)  # Adjust the delay as needed

except SerialException as e:
    print(f"Failed to open serial port: {e}")
