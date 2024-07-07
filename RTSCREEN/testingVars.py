class MyClass:
    def __init__(self):
        self.arduino = "value1"
        self.ard = "455"
        self.b = "value3"

# Create an instance of the class
my_instance = MyClass()

# Display all variable names
print(vars(my_instance).keys())

specificKey = 'ard'
if specificKey in vars(my_instance):
    specificValue = vars(my_instance)[specificKey]
    print(f"Sensor: {specificValue}")
else:
    print(f"{specificKey} does not exist in the instance")
