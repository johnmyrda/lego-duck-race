from abc import ABC, abstractmethod
from enum import IntEnum

# When spun clockwise, which way does the duck go?
class MotorDirection(IntEnum):
    FORWARDS = 1
    BACKWARDS = -1

class MotorInterface(ABC):

    def __init__(self, name: str, direction: MotorDirection = MotorDirection.FORWARDS):
        self.name = name
        self.direction = direction

    @abstractmethod
    def debug(self) -> str:
        return "Not implemented"

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def start(self, speed: int) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    def print(self, message: str):
        print(f"Motor {self.name}: {message}")
