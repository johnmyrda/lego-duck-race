from buildhat import Motor, ColorDistanceSensor, DeviceError
from buildhat.devices import Device
from typing import Callable

ports = ["A", "B", "C", "D"]


def detect_peripheral(constructor: Callable[..., Device]):
    for port in ports:
        try:
            peripheral = constructor(port)
            print(
                "Successfully initialized <{p.name}: {p.description}> on Port {port}".format(
                    p=peripheral, port=str(port)
                )
            )
            return peripheral
        except DeviceError as err:
            pass


def detect_sensor() -> ColorDistanceSensor:
    return detect_peripheral(lambda port: ColorDistanceSensor(port))


def detect_motor() -> Motor:
    return detect_peripheral(lambda port: Motor(port))
