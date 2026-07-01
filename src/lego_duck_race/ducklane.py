import threading
import time
from enum import Enum
from typing import Protocol

from lego_duck_race.interfaces.controller_base import Button
from lego_duck_race.interfaces.motor_interface import MotorInterface


class LimitSwitch(Protocol):
    @property
    def is_active(self) -> bool:
        """Return True when the lane finish/reset switch is active."""
        ...


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
        limit_switch: LimitSwitch,
    ):
        self.button = button
        self.name = name
        self.motor = motor
        self.limit_switch = limit_switch
        self.status = LaneState.STOPPED
        button.on_press(self.move_forward)

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
        self.button.on_press(self.move_forward)

    def move_forward(self) -> None:
        if self.status == LaneState.STOPPED:
            self._update_status(LaneState.MOVING)
            threading.Thread(target=self._move_forward, daemon=True).start()

    def _move_forward(self) -> None:
        self.motor.start(50)
        time.sleep(2)
        self.motor.stop()
        self._update_status(LaneState.STOPPED)

    def update(self) -> None:
        if self.passed_finish_line():
            self.reset()

    def print(self, message: str) -> None:
        print(f"Lane {self.name}: {message}")

    def passed_finish_line(self) -> bool:
        return self.limit_switch.is_active
