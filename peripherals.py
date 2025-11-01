from buildhat import Motor, ColorDistanceSensor, DeviceError
from buildhat.devices import Device
from typing import Callable
from windowed_list import WindowedList

ports = ['A','B','C','D']

def detectPeripheral(constructor: Callable[..., Device]):
    for port in ports:
        try:
            peripheral = constructor(port)
            print("Successfully initialized <{p.name}: {p.description}> on Port {port}".format(p=peripheral, port=str(port)))
            return peripheral
        except DeviceError as err:
            pass

def detectSensor() -> ColorDistanceSensor:
    return detectPeripheral(lambda port: ColorDistanceSensor(port))

def detectMotor() -> Motor:
    return detectPeripheral(lambda port: Motor(port))    
