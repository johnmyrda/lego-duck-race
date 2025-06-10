from controller import Controller, Button
import time
from buildhat import Motor # type: ignore
from windowed_list import WindowedList
from sensor import Sensor


class DuckLane:

    def __init__(self, motorPort: str, button: Button, sensor: Sensor):
        self.button = button
        self.motor_port = motorPort
        self.motor = Motor(motorPort)
        self.sensor = sensor
        button.on_press(lambda: self.move_forward(motor)) # type: ignore

    def print_debug(self):
        print("Speed, Pos, Apos: " + str(self.motor.get())) # type: ignore

    def reset(self) -> None:
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
                print("Started Reset")
            if speed_window.mean() < 0:
                motor_started_forwards = True
                print("Started forwards")
            if speed_window.stalled() and not motor_started_forwards:
                motor_stalled = True
                print("Stalled")
            # Add time between readings
            time.sleep(.05)

        reset_completed = False
        while not reset_completed and not motor_stalled:
            self.print_debug()
            speed_window.push(motor.get_speed())  # type: ignore
            if speed_window.stalled():
              reset_completed = True
              print("Reset Complete!")
            time.sleep(.1)
            motor.start(20) # type: ignore

        motor.stop() # type: ignore

    def move_forward(self) -> None:
        print("Moving forward!")
        self.motor.run_for_degrees(-500, 50)  # type: ignore
        print("Done moving")

# Can detect speed in close to real time, check if stalled
# Window function useful but not necessary

    def update_state(self) -> None:
        distance = self.sensor.distance()
        # print("Distance=" + str(distance))
        if (distance < 2):
            print("Resetting because distance=" + str(distance))
            self.button.on_press(lambda: print("Button disabled during reset"))
            self.reset()
            self.button.on_press(lambda: self.move_forward(motor)) # type: ignore

if __name__ == "__main__":
    controller = Controller()
    controller.debug_info()
    button = controller.get_button("k1")
    # Sensor A
    GPIO_TRIGGER_A = 23
    GPIO_ECHO_A = 24
    sensor = Sensor(GPIO_TRIGGER_A, GPIO_ECHO_A, "A")
    lane = DuckLane("A", button, sensor)
    while True:
        controller.update_state()
        lane.update_state()
