from lego_duck_race.config import DEFAULT_LANES, LaneConfig
from lego_duck_race.ducklane import DuckLane
from lego_duck_race.hardware.buildhat_motor import LegoMotor, diagnose_motors
from lego_duck_race.hardware.hid_controller import ArcadeController, diagnose_controller
from lego_duck_race.hardware.limit_switch import diagnose_limit_switches, get_limit_switch


def build_hardware_lanes(
    controller: ArcadeController,
    configs: list[LaneConfig] | None = None,
) -> list[DuckLane]:
    """Build lanes backed by the real arcade controller, motors, and GPIO switches."""
    lanes = []
    for config in configs or DEFAULT_LANES:
        lanes.append(
            DuckLane(
                config.name,
                LegoMotor(config.motor_port),
                controller.get_button(config.button_name),
                get_limit_switch(config.limit_switch_gpio),
            )
        )
    return lanes


def diagnose_all() -> None:
    """Run interactive diagnostics for all hardware used by the full game."""
    print("Starting controller diagnostic. Press Ctrl+C when done.")
    try:
        diagnose_controller()
    except KeyboardInterrupt:
        print("\nController diagnostic stopped.")

    print("Starting motor diagnostic.")
    diagnose_motors()

    print("Starting limit switch diagnostic.")
    diagnose_limit_switches()
