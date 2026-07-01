from gpiozero import Button as LimitSwitch

from lego_duck_race.config import DEFAULT_LANES


def get_limit_switch(gpio_pin: int) -> LimitSwitch:
    return LimitSwitch(gpio_pin)


def diagnose_limit_switches() -> None:
    """Wait for each configured limit switch and report when it is pressed."""
    print("Limit Switch Test starting...")
    for lane in DEFAULT_LANES:
        print(f"Press Limit Switch {lane.switch_name} on GPIO {lane.limit_switch_gpio} to test")
        limit_switch = get_limit_switch(lane.limit_switch_gpio)
        limit_switch.wait_for_press()
        print(f"Limit Switch {lane.switch_name} pressed!")
    print("Limit Switch Test finished")
