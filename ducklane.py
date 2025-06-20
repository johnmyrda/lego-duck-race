from controller import Controller, Button
import time
import threading
from buildhat import Motor # type: ignore
from motor import LegoMotor
from motor_interface import MotorInterface
from sensor import Sensor
from measurement_logger import MeasurementLogger, LogLevel, Logger
from enum import Enum

class LaneState(Enum):
    STOPPED = 1
    MOVING = 2
    RESETTING = 3

class DuckLane:

    def __init__(self, name: str, motor: MotorInterface, button: Button, sensor: Sensor, reset_distance: int = 5, start_pos: int = 36):
        self.button = button
        self.name = name
        self.motor = motor
        self.sensor = sensor
        self.reset_distance = reset_distance
        self.start_pos = start_pos
        self.sensor_logger = MeasurementLogger(2000, "Sensor " + self.name, LogLevel.DEBUG)
        self.logger = Logger(self.name, LogLevel.DEBUG)
        self.status = LaneState.STOPPED
        button.on_press(lambda: self.move_forward()) # type: ignore

    def _update_status(self, state: LaneState):
        self.print("Updating state to " + state.name)
        self.status = state

    def reset(self):
        if self.status != LaneState.RESETTING:
            self._update_status(LaneState.RESETTING)
            self.logger.debug("Resetting with distance=" + str(self.sensor.distance()))
            threading.Thread(target=self._reset, daemon=True).start()

    def _reset(self) -> None:
        self.button.on_press(lambda: self.print("Button disabled during reset"))
        while self.sensor.distance() < self.start_pos:
            self.motor.start(-100)
            time.sleep(.1)
        self.motor.reset()
        self._update_status(LaneState.STOPPED)
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

    def print(self, message: str):
        print(self.name + ": " + message)

    def passed_finish_line(self) -> bool:
        distance = self.sensor.distance()
        self.sensor_logger.debug(f"Distance={distance:.2f}cm")
        if distance < self.reset_distance:
            return True
        return False

if __name__ == "__main__":
    controller = Controller()
    controller.debug_info()
    button_a = controller.get_button("k1")
    button_b = controller.get_button("k2")
    button_c = controller.get_button("k3")
    # Lane A
    GPIO_TRIGGER_A = 23
    GPIO_ECHO_A = 24
    sensor_a = Sensor(GPIO_TRIGGER_A, GPIO_ECHO_A, "A")
    motor_a = LegoMotor("A")
    lane_a = DuckLane("Lane A", motor_a, button_a, sensor_a)
    # Lane B
    GPIO_TRIGGER_B = 25
    GPIO_ECHO_B = 5
    sensor_b = Sensor(GPIO_TRIGGER_B, GPIO_ECHO_B, "B")
    motor_b = LegoMotor("B")
    lane_b = DuckLane("Lane B", motor_b, button_b, sensor_b)
    # Lane C
    GPIO_TRIGGER_C = 6
    GPIO_ECHO_C = 12
    sensor_c = Sensor(GPIO_TRIGGER_C, GPIO_ECHO_C, "C")
    motor_c = LegoMotor("C")
    lane_c = DuckLane("Lane C", motor_c, button_c, sensor_c)
    print("Ducklane starting")
    while True:
        controller.update_state()
        lane_a.update()
        lane_b.update()
        lane_c.update()
