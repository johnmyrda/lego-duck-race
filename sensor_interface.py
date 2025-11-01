from abc import ABC, abstractmethod
import time

class SensorInterface(ABC):

    def __init__(self, name:str):
        self.name = name

    @abstractmethod
    def distance(self) -> float:
        pass

    def distance_readout(self) -> str:
        distance = self.distance()
        return f"Sensor {self.name} Distance: {distance:.1f} cm"


class FakeSensor(SensorInterface):

    def __init__(self, name: str):
        super().__init__(name)
        self.fake_distance = 25.0

    def distance(self) -> float:
        time.sleep(.0001)
        return self.fake_distance
