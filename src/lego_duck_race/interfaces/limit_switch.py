from gpiozero import Button as LimitSwitch

switch_map = {
    "A": 27,
    "B": 5,
    "C": 26,
}

def get_limit_switch(name: str) -> LimitSwitch:
    return LimitSwitch(switch_map[name])

def test():
    print("Limit Switch Test starting...")
    for switch_name in switch_map.keys():
        print(f"Press Limit Switch {switch_name} to test")
        limit_switch = get_limit_switch(switch_name)
        limit_switch.wait_for_press()
        print(f"Limit Switch {switch_name} pressed!")
    print("Limit Switch Test finished")
