import hid
from typing import Callable, cast

class Button:

    def __init__(self, name: str):
        self.name = name
        self.on_press_function = lambda: print("You pressed: " + name)
        self.pressed = False

    def on_press(self, action: Callable[..., None]) -> None:
        self.on_press_function = action
    
    def update_state(self, is_pressed: int) -> None:
        if self.pressed == False and is_pressed:
            self.on_press_function()
        self.pressed = is_pressed

class Joystick:

    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def update_state(self, up: bool, down: bool, left: bool, right: bool):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    # Print ←↖↑↗→↘↓↙ when appropriate
    def debug(self):
        # ↖↑↗
        if self.up:
            if self.left:
                return "↖"
            elif self.right:
                return "↗"
            else:
                return "↑"
        # ↙↓↘
        if self.down:
            if self.left:
                return "↙"
            elif self.right:
                return "↘"
            else:
                return "↓"
        if self.left:
            return "←"
        if self.right:
            return "→"
        return "•"

# Manufacturer: Baolian industry Co., Ltd
# Product: TS-UAIB-OP02
class Controller:

    def __init__(self):
        self.controller = hid.device() # type: ignore
        self.vendor_id = 0x32be
        self.product_id = 0x2000
        self.__connect__()
        self.joystick = Joystick()
        self.button_map= dict[str, Button]()
        self.__setup_buttons__()

    def __connect__(self):
        self.controller.open(self.vendor_id, self.product_id) # type: ignore
        self.controller.set_nonblocking(True) # type: ignore
        # Test for connection here?

    def __setup_buttons__(self):
        buttons = [
            # K1-8 are in the first bitfield      
            'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8',
            # K9-13 are in the second bitfield      
            'k9', 'k10', 'k11', 'k12', 'k13'
        ]
        for name in buttons:
            self.button_map[name] = Button(name)

    def get_button(self, name: str) -> Button:
        return self.button_map[name]

    def register_action(self, button: str, action: Callable[..., None]) -> None:
        self.get_button(button).on_press(action)

    def update_state(self):
        report = cast(list[int], self.controller.read(8)) # type: ignore # Only 7 bytes needed
        if report:
            # print(report)
            buttons = self.button_map
            buttons['k1'].update_state(report[0] & 0b00000001)
            buttons['k2'].update_state(report[0] & 0b00000010)
            buttons['k3'].update_state(report[0] & 0b00000100)
            buttons['k4'].update_state(report[0] & 0b00001000)
            buttons['k5'].update_state(report[0] & 0b00010000)
            buttons['k6'].update_state(report[0] & 0b00100000)
            buttons['k7'].update_state(report[0] & 0b01000000)
            buttons['k8'].update_state(report[0] & 0b10000000)
            buttons['k9'].update_state(report[1] & 0b00000001)
            buttons['k10'].update_state(report[1] & 0b00000010)
            buttons['k11'].update_state(report[1] & 0b00000100)
            buttons['k12'].update_state(report[1] & 0b00001000)
            buttons['k13'].update_state(report[1] & 0b00010000)
            self.joystick.left = (report[3] == 0)
            self.joystick.right = (report[3] == 255)
            self.joystick.up = (report[4] == 0)
            self.joystick.down = (report[4] == 255)

    def debug_info(self):
        gamepad = self.controller # type: ignore
        print("Error: " + gamepad.error()) # type: ignore
        print("Manufacturer: " + gamepad.get_manufacturer_string()) # type: ignore
        print("Product: " + gamepad.get_product_string()) # type: ignore
        print("Serial Number: " + gamepad.get_serial_number_string()) # type: ignore
        print("HID Report Descriptor: " + str(gamepad.get_report_descriptor())) # type: ignore

# Simple test program to output input states
if __name__ == "__main__":
    # Initialize Gamepad
    controller = Controller()
    controller.debug_info()
    while True:
        controller.update_state()
        print(controller.joystick.debug(), end = "\r")
