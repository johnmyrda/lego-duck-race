from unittest.mock import Mock

from src.lego_duck_race.interfaces.controller_base import Button, FakeController, Joystick


def test_button_press() -> None:
    button = Button("A")
    mock = Mock()
    button.on_press(mock)
    mock.assert_not_called()
    button.press()
    mock.assert_called_once()


def test_controller_buttons() -> None:
    controller = FakeController()
    button = controller.get_button("k1")
    assert button is not None
    assert button.name == "k1"


def test_joystick_direction() -> None:
    joy = Joystick()
    joy.up = True
    joy.right = True
    assert joy.debug() == "↗"
