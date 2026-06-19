import threading
import time
from enum import Enum

from lego_duck_race.interfaces.limit_switch import get_limit_switch
from .interfaces.arcade_controller import ArcadeController
from .interfaces.controller_base import Button
from .interfaces.motor import LegoMotor
from .interfaces.motor_interface import MotorInterface
from gpiozero import Button as LimitSwitch


class LaneState(Enum):
    STOPPED = 1
    MOVING = 2
    RESETTING = 3


class DuckLane:
    def __init__(
        self,
        name: str,
        motor: MotorInterface,
        button: Button,
        limit_switch: LimitSwitch
    ):
        self.button = button
        self.name = name
        self.motor = motor
        self.limit_switch = limit_switch
        self.status = LaneState.STOPPED
        button.on_press(lambda: self.move_forward())  # type: ignore

    def _update_status(self, state: LaneState) -> None:
        self.print("Updating state to " + state.name)
        self.status = state

    def reset(self) -> None:
        if self.status != LaneState.RESETTING:
            self._update_status(LaneState.RESETTING)
            self.print("Resetting!")
            threading.Thread(target=self._reset, daemon=True).start()

    def _reset(self) -> None:
        self.button.on_press(lambda: self.print("Button disabled during reset"))
        self.motor.start(-100)
        self.motor.reset()
        self._update_status(LaneState.STOPPED)
        self.print("Reset Complete!")
        self.button.on_press(lambda: self.move_forward())

    def move_forward(self) -> None:
        if self.status == LaneState.STOPPED:
            self._update_status(LaneState.MOVING)
            threading.Thread(target=self._move_forward, daemon=True).start()

    def _move_forward(self) -> None:
        self.motor.start(50)
        time.sleep(2)
        self.motor.stop()
        self._update_status(LaneState.STOPPED)

    # Can detect speed in close to real time, check if stalled
    # Window function useful but not necessary

    def update(self) -> None:
        if self.passed_finish_line():
            self.reset()

    def print(self, message: str) -> None:
        print(f"Lane {self.name}: {message}")

    def passed_finish_line(self) -> bool:
        return self.limit_switch.is_active

def test():
    print("Ducklane starting...")
    controller = ArcadeController()
    controller.debug_info()
    button_a = controller.get_button("k1")
    button_b = controller.get_button("k2")
    button_c = controller.get_button("k3")
    # Lane A
    motor_a = LegoMotor("A")
    lane_a = DuckLane("A", motor_a, button_a, get_limit_switch("A"))
    # # Lane B
    motor_b = LegoMotor("B")
    lane_b = DuckLane("B", motor_b, button_b, get_limit_switch("B"))
    # # Lane C
    motor_c = LegoMotor("C")
    lane_c = DuckLane("C", motor_c, button_c, get_limit_switch("C"))
    print("Ducklane starting")
    while True:
        controller.update_state()
        lane_a.update()
        lane_b.update()
        lane_c.update()

if __name__ == "__main__":
    test()
