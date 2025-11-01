from typing import Callable
from enum import Enum
from abc import abstractmethod, ABC

class Button:

    def __init__(self, name: str):
        self.name = name
        self.on_press_function = lambda: print("You pressed: " + name)
        self.pressed = False

    def on_press(self, action: Callable[..., None]) -> None:
        self.on_press_function = action

    def press(self):
        self.on_press_function()

    def update_state(self, is_pressed: int) -> None:
        if self.pressed == False and is_pressed:
            self.press()
        self.pressed = is_pressed

class Direction(Enum):
    UP = "↑"
    DOWN = "↓"
    LEFT = "←"
    RIGHT = "→"
    NONE = "•"

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
class ControllerBase(ABC):

    def __init__(self):
        self.vendor_id = 0x32be
        self.product_id = 0x2000
        self.joystick = Joystick()
        self.button_map= dict[str, Button]()
        self.__setup_buttons__()

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

    @abstractmethod
    def update_state(self):
        pass

class FakeController(ControllerBase):

    def __init__(self):
        super().__init__()

    def update_state(self) -> None:
        raise NotImplementedError
