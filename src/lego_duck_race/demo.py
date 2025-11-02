import time

from buildhat import ColorDistanceSensor, Motor

from .interfaces.arcade_controller import ArcadeController
from .interfaces.peripherals import detect_motor, detect_sensor
from .utils.windowed_list import WindowedList


def print_debug(motor: Motor):
    data = motor.get()
    print("Speed, Pos, Apos: " + str(data))


def reset(motor: Motor):
    motor_started = False
    motor_started_forwards = False
    motor_stalled = False
    speed_window = WindowedList(5)
    while not motor_started and not motor_stalled:
        motor.start(20)
        # print_debug(motor)
        speed_window.push(motor.get_speed())
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
        time.sleep(0.05)

    reset_completed = False
    while not reset_completed and not motor_stalled:
        print_debug(motor)
        speed_window.push(motor.get_speed())
        if speed_window.stalled():
            reset_completed = True
            print("Reset Complete!")
        time.sleep(0.1)
        motor.start(20)

    motor.stop()


def move_forward(motor: Motor):
    print("Moving forward!")
    motor.run_for_degrees(-500, 50)
    print("Done moving")


# Can detect speed in close to real time, check if stalled
# Window function useful but not necessary


def setup(controller: ArcadeController, motor: Motor, sensor: ColorDistanceSensor):
    sensor.on()
    controller.get_button("k1").on_press(lambda: move_forward(motor))


def loop(controller: ArcadeController, motor: Motor, sensor: ColorDistanceSensor):
    while True:
        controller.update_state()
        distance = sensor.get_distance()
        # print("Distance=" + str(distance))
        if distance < 2:
            print("Resetting because distance=" + str(distance))
            controller.get_button("k1").on_press(lambda: print("Button disabled during reset"))
            reset(motor)
            controller.get_button("k1").on_press(lambda: move_forward(motor))


def main():
    _controller = ArcadeController()
    _controller.debug_info()
    _motor = detect_motor()
    _sensor = detect_sensor()
    setup(_controller, _motor, _sensor)
    loop(_controller, _motor, _sensor)
