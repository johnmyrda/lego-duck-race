import time
from dataclasses import dataclass
from typing import cast

from buildhat import Motor  # type: ignore

from lego_duck_race.interfaces.motor_interface import MotorDirection, MotorInterface
from lego_duck_race.utils.windowed_list import WindowedList


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
        reset_speed = -50
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


def test_motor(motor: LegoMotor) -> None:
    print("  Testing motor: " + motor.name)
    print("  Starting motor with speed 100")
    motor.start(100)
    time.sleep(2)
    print("  " + motor.debug())
    time.sleep(2)
    print("  Stopping motor")
    motor.stop()
    time.sleep(1)
    print("  " + motor.debug())
    time.sleep(1)
    print("  Starting motor with speed -100")
    motor.start(-100)
    time.sleep(2)
    print("  " + motor.debug())
    time.sleep(2)
    print("  Stopping motor")
    motor.stop()
    print("  Done testing motor: " + motor.name)


@dataclass
class TestResult:
    port: str
    success: bool = False


def diagnose_motors() -> None:
    """Connect to Build HAT motors and verify basic forward/backward/stop operations."""
    print("Motor Test starting...")
    motor_tests = [
        TestResult("A"),
        TestResult("B"),
        TestResult("C"),
        # TestResult("D")
    ]
    max_connection_attempts = 100
    connection_attempts = 0
    while connection_attempts < max_connection_attempts and not all(t.success for t in motor_tests):
        for motor_test in motor_tests:
            if motor_test.success:
                continue
            print(
                f"Connecting to motor {motor_test.port} "
                f"(attempt {connection_attempts + 1}/{max_connection_attempts})"
            )
            try:
                motor = LegoMotor(motor_test.port)
                test_motor(motor)
                motor_test.success = True
                break
            except Exception as e:
                print("  Failed to initialize motor " + motor_test.port + ": " + str(e))
                time.sleep(1)
            connection_attempts += 1

    print("Test results")
    for motor_test in motor_tests:
        print(f"Motor {motor_test.port}: {'SUCCESS' if motor_test.success else 'FAIL'}")


if __name__ == "__main__":
    diagnose_motors()
