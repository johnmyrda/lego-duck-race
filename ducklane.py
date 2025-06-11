from controller import Controller, Button
import time
from buildhat import Motor # type: ignore
from windowed_list import WindowedList
from sensor import Sensor
from measurement_logger import MeasurementLogger


class DuckLane:

    def __init__(self, motorPort: str, button: Button, sensor: Sensor, reset_distance: int = 5):
        self.button = button
        self.name = "Lane " + motorPort
        self.motor_port = motorPort
        self.motor = Motor(motorPort)
        self.sensor = sensor
        self.reset_distance = reset_distance
        self.logger = MeasurementLogger(1000, self.name)
        button.on_press(lambda: self.move_forward()) # type: ignore

    def print_debug(self):
        self.print("Speed, Pos, Apos: " + str(self.motor.get())) # type: ignore

    def reset(self) -> None:
        motor = self.motor
        motor_started = False
        motor_started_forwards = False
        motor_stalled = False
        speed_window = WindowedList(5)
        while not motor_started and not motor_stalled:
            motor.start(20) # type: ignore
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
            motor.start(20) # type: ignore

        motor.stop() # type: ignore

    def move_forward(self) -> None:
        self.print("Moving forward!")
        self.motor.run_for_degrees(-1000, 50)  # type: ignore
        self.print("Done moving")

# Can detect speed in close to real time, check if stalled
# Window function useful but not necessary

    def update_state(self) -> None:
        distance = self.sensor.distance()
        self.logger.info("Distance=" + str(distance))
        if (distance < self.reset_distance):
            self.print("Resetting because distance=" + str(distance))
            self.button.on_press(lambda: print("Button disabled during reset"))
            self.reset()
            self.button.on_press(lambda: self.move_forward()) # type: ignore

    def print(self, message: str):
        print(self.name + ": " + message)

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
        lane_a.update_state()
        lane_b.update_state()
        lane_c.update_state()
