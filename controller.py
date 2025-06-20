import hid # type: ignore
from typing import cast
import time
from controller_base import *

# Manufacturer: Baolian industry Co., Ltd
# Product: TS-UAIB-OP02
class Controller(ControllerBase):

    def __init__(self, min_period_ms: int = 1):
        super().__init__()
        self.__connect__()
        self.min_period_ns = min_period_ms * 1000000
        self.last_log_time: int = 0

    def __connect__(self):
        self.controller = hid.device() # type: ignore
        self.controller.open(self.vendor_id, self.product_id) # type: ignore
        self.controller.set_nonblocking(True) # type: ignore
        # Test for connection here?

    def update_state(self) -> None:
        now = time.time_ns()
        elapsed_ns = now - self.last_log_time
        if (elapsed_ns > self.min_period_ns):
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
