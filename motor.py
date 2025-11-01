from motor_interface import MotorDirection, MotorInterface
from buildhat import Motor  # type: ignore
from typing import cast
from windowed_list import WindowedList
import time


class LegoMotor(MotorInterface):
    # Name must be Port number
    def __init__(self, name: str, direction: MotorDirection = MotorDirection.BACKWARDS):
        super().__init__(name, direction)
        self.motor = Motor(name)

    def debug(self) -> str:
        return "Speed, Pos, Apos: " + str(self.motor.get())  # type: ignore

    def reset(self) -> None:
        motor_started = False
        motor_started_forwards = False
        motor_stalled = False
        speed_window = WindowedList(8)
        reset_speed = -30
        self.stop()
        while not motor_started and not motor_stalled:
            self.start(reset_speed)
            print(self.debug())
            speed_window.push(self.speed())
            if speed_window.mean() < 0.0:
                motor_started = True
                self.print("Started Reset")
            if speed_window.mean() > 0:
                motor_started_forwards = True
                self.print("Started forwards")
            if speed_window.stalled() and not motor_started_forwards:
                motor_stalled = True
                self.print("Stalled")
            # Add time between readings
            time.sleep(0.05)

        reset_completed = False
        while not reset_completed and not motor_stalled:
            print(self.debug())
            speed_window.push(self.speed())
            if speed_window.stalled():
                reset_completed = True
                self.print("Reset Complete!")
            time.sleep(0.1)
            self.start(reset_speed)

        self.stop()

    def start(self, speed: int) -> None:
        self.motor.start(speed * self.direction)  # type: ignore

    def stop(self) -> None:
        self.motor.stop()

    def speed(self) -> int:
        return cast(int, (self.motor.get_speed() * self.direction))
