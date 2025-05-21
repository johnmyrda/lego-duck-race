import hid
from typing import Callable

class Button:

    def __init__(self, name: str):
        self.name = name
        self.on_press_function = lambda: print("You pressed: " + name)
        self.pressed = False

    def on_press(self, action: Callable):
        self.on_press_function = action
    
    def update_state(self, is_pressed: bool):
        if self.pressed == False and is_pressed:
            self.on_press_function()
        self.pressed = is_pressed

# Manufacturer: Baolian industry Co., Ltd
# Product: TS-UAIB-OP02
class Controller:

    def __init__(self):
        self.controller = hid.device()
        self._update_thread = None
        self.vendor_id = 0x32be
        self.product_id = 0x2000
        self.button_map = dict()
        self.__connect__()
        self.__setup_buttons__()

    def __connect__(self):
        self.controller.open(self.vendor_id, self.product_id)
        self.controller.set_nonblocking(True)
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

    def get_button(self, name) -> Button:
        return self.button_map[name]

    def register_action(self, button: str, action: callable):
        self.get_button(button).on_press(action)

    def update_state(self):
        report = self.controller.read(8) # Only 7 bytes needed
        if report:
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

    def debug_info(self):
        gamepad = self.controller
        print("Error: " + gamepad.error())
        print("Manufacturer: " + gamepad.get_manufacturer_string())
        print("Product: " + gamepad.get_product_string())
        print("Serial Number: " + gamepad.get_serial_number_string())
        print("HID Report Descriptor: " + str(gamepad.get_report_descriptor()))

# Simple test program to output input states
if __name__ == "__main__":
    # Initialize Gamepad
    controller = Controller()
    controller.debug_info()
    while True:
        controller.update_state()
