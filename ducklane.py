from controller import Controller, Button
import time
import threading
from buildhat import Motor # type: ignore
from windowed_list import WindowedList
from sensor import Sensor
from measurement_logger import MeasurementLogger, LogLevel, Logger
from enum import Enum

class LaneState(Enum):
    STOPPED = 1
    MOVING = 2
    RESETTING = 3

class DuckLane:

    def __init__(self, motorPort: str, button: Button, sensor: Sensor, reset_distance: int = 5, start_pos: int = 36):
        self.button = button
        self.name = "Lane " + motorPort
        self.motor_port = motorPort
        self.motor = Motor(motorPort)
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

    def print_debug(self):
        self.print("Speed, Pos, Apos: " + str(self.motor.get())) # type: ignore

    def reset(self):
        if self.status != LaneState.RESETTING:
            self._update_status(LaneState.RESETTING)
            threading.Thread(target=self._reset_alt, daemon=True).start()

    def _reset_alt(self) -> None:
        self.logger.debug("Alternate Reset")
        while self.sensor.distance() < self.start_pos:
            self.move_backward_override()
            time.sleep(.1)
        self._reset()

    def _reset(self) -> None:
        self.logger.debug("Resetting because distance=" + str(self.sensor.distance))
        self.button.on_press(lambda: self.print("Button disabled during reset"))

        motor = self.motor
        motor_started = False
        motor_started_forwards = False
        motor_stalled = False
        speed_window = WindowedList(8)
        reset_speed = 30
        motor.stop()
        while not motor_started and not motor_stalled:
            motor.start(reset_speed) # type: ignore
            # print_debug(motor)
            speed_window.push(motor.get_speed()) # type: ignore
            if speed_window.mean() > 0.0:
                motor_started = True
                self.print("Started Reset")
            if speed_window.mean() < 0:
                motor_started_forwards = True
                self.print("Started forwards")
            if speed_window.stalled() and not motor_started_forwards:
                motor_stalled = True
                self.print("Stalled")
            # Add time between readings
            time.sleep(.05)

        reset_completed = False
        while not reset_completed and not motor_stalled:
            self.print_debug()
            speed_window.push(motor.get_speed())  # type: ignore
            if speed_window.stalled():
              reset_completed = True
              self.print("Reset Complete!")
            time.sleep(.1)
            motor.start(reset_speed) # type: ignore
            
        motor.stop() # type: ignore
        self._update_status(LaneState.STOPPED)
        self.button.on_press(lambda: self.move_forward()) # type: ignore

    def move_forward(self) -> None:
        if self.status == LaneState.STOPPED:
            self._update_status(LaneState.MOVING)
            threading.Thread(target=self._move_forward, daemon=True).start()

    def _move_forward(self) -> None:
        self.motor.start(-50)  # type: ignore
        # self.motor.run_for_degrees(720, -50)  # type: ignore
        time.sleep(2)
        self.motor.stop()
        self._update_status(LaneState.STOPPED)

    def move_forward_override(self):
        self.motor.start(-100)  # type: ignore

    def move_backward_override(self):
        self.motor.start(100)  # type: ignore

    def stop(self):
        self.motor.stop()

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
    lane_a = DuckLane("A", button_a, sensor_a)
    # Lane B
    GPIO_TRIGGER_B = 25
    GPIO_ECHO_B = 5
    sensor_b = Sensor(GPIO_TRIGGER_B, GPIO_ECHO_B, "B")
    lane_b = DuckLane("B", button_b, sensor_b)
    # Lane C
    GPIO_TRIGGER_C = 6
    GPIO_ECHO_C = 12
    sensor_c = Sensor(GPIO_TRIGGER_C, GPIO_ECHO_C, "C")
    lane_c = DuckLane("C", button_c, sensor_c)
    print("Ducklane starting")
    while True:
        controller.update_state()
        lane_a.update()
        lane_b.update()
        lane_c.update()
