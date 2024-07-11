import time
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from ArduinoClass import ArduinoClass

class Mediator:

    def __init__(self):
        self.arduino = ArduinoClass()
        self.arduinoList = []

    def getSensorName(self,name):
        if name in vars(self.arduino):
            print(f"Sensor: {name}")
        else:
            print(f"{name} does not exist in the instance")

        return name

    def getAnalogueSensor(self,sensorName):
        sensorDetails =  getattr(self.arduino, sensorName, None)
        PIN = self.arduino.getPIN(sensorDetails)
        sensorVal = self.arduino.getAnaloguePinReading(PIN)
        sensorStr = f"{sensorVal}"
        return sensorStr


    def getDigitalSensor(self,sensorName):
        sensorDetails =  getattr(self.arduino, sensorName, None)
        PIN = self.arduino.getPIN(sensorDetails)
        sensorVal = self.arduino.getDigitalPinReading(PIN)
        print(f"Sensor: {sensorVal}")
        sensorStr = f"{sensorVal}"
        self.arduino.calcSpeed()
        return sensorStr

    #####################################################################################
    def getCalculatedReading(self,sensorName):
        '''speed = self.arduino.calcSpeed()
        distanceTravelled = self.arduino.getDistanceTravelled()
        current = self.arduino.getCurrent()
        voltage = self.arduino.getVoltage()
        batteryPercentage = self.arduino.getBatteryPercentage()
       
        switch = {
            "speed": speed,
            "distanceTravelled": distanceTravelled,
            "current": current,
            "voltage": voltage,
            "batteryPercentage": batteryPercentage
        }
        print(f"SWITCH CASE{switch[sensorName]}")

        return switch[sensorName]'''
        
        sensorReadings = {}

        try: 
            speed = self.arduino.calcSpeed()
            if speed is not None:
                sensorReadings["speed"] = speed
        except Exception as e:
                    print(f"Error in getting speed: {e}")

        try: 
            distanceTravelled = self.arduino.getDistanceTravelled()
            if distanceTravelled is not None:
                sensorReadings["distanceTravelled"] = distanceTravelled
        except Exception as e:
                    print(f"Error in getting distance travelled: {e}")

        try: 
            voltage = self.arduino.getVoltage()
            if voltage is not None:
                sensorReadings["voltage"] = voltage
        except Exception as e:
                    print(f"Error in getting voltage: {e}")

        try: 
            current = self.arduino.getCurrent()
            if current is not None:
                sensorReadings["current"] = current
        except Exception as e:
                    print(f"Error in getting current: {e}")

        try: 
            batteryPercentage = self.arduino.getBatteryPercentage()
            if batteryPercentage is not None:
                sensorReadings["batteryPercentage"] = batteryPercentage
        except Exception as e:
                    print(f"Error in getting batterypercentage: {e}")

        print(f"Available sensor names: {sensorReadings.keys()}") #for debugging 
        #returns the ones retrieved by arduino object excluding ones with none
        print(f"SWITCH CASE: {sensorReadings[sensorName]}")
        return sensorReadings[sensorName]



        



    def getVoltage(self):
        return self.arduino.getVoltage()