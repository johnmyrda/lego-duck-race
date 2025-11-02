from collections.abc import Callable
from typing import TypeVar, cast

from buildhat import ColorDistanceSensor, DeviceError, Motor
from buildhat.devices import Device

ports = ["A", "B", "C", "D"]
T = TypeVar("T")


def detect_peripheral(constructor: Callable[..., Device]) -> Device:
    for port in ports:
        try:
            peripheral = constructor(port)
            print(
                f"Successfully initialized <{peripheral.name}: "
                f"{peripheral.description}> on Port {str(port)}"
            )
            return peripheral
        except DeviceError:
            pass
    raise DeviceError("No peripheral found")


def detect_sensor() -> ColorDistanceSensor:
    return cast(ColorDistanceSensor, detect_peripheral(lambda port: ColorDistanceSensor(port)))


def detect_motor() -> Motor:
    return cast(Motor, detect_peripheral(lambda port: Motor(port)))
