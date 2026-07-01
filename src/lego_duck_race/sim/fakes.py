from lego_duck_race.interfaces.controller_base import ControllerBase
from lego_duck_race.interfaces.motor_interface import MotorDirection, MotorInterface


class FakeMotor(MotorInterface):
    def __init__(self, name: str = "fake", direction: MotorDirection = MotorDirection.FORWARDS):
        super().__init__(name, direction)
        self.speed = 0
        self.reset_count = 0
        self.start_history: list[int] = []
        self.stop_count = 0

    def debug(self) -> str:
        return f"Speed: {self.speed}"

    def reset(self) -> None:
        self.reset_count += 1
        self.stop()

    def start(self, speed: int) -> None:
        self.speed = speed * self.direction
        self.start_history.append(self.speed)

    def stop(self) -> None:
        self.speed = 0
        self.stop_count += 1


class FakeLimitSwitch:
    def __init__(self, is_active: bool = False):
        self.is_active = is_active


class FakeController(ControllerBase):
    def update_state(self) -> None:
        pass
