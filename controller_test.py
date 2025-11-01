from controller_base import Button, FakeController, Joystick
from unittest.mock import Mock
import unittest

class TestController(unittest.TestCase):

    def test_button_press(self):
        button = Button("A")
        mock = Mock()
        button.on_press(mock)
        mock.assert_not_called()
        button.press()
        mock.assert_called_once()

    def test_controller_buttons(self):
        controller = FakeController()
        button = controller.get_button('k1')
        self.assertIsNotNone(button)
        self.assertEqual('k1', button.name)

    def test_joystick_direction(self):
        joy = Joystick()
        joy.up = True
        joy.right = True
        self.assertEqual("↗", joy.debug())

if __name__ == '__main__':
    unittest.main()
