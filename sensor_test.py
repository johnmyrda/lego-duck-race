import unittest

from sensor_interface import FakeSensor


class TestFakeSensor(unittest.TestCase):
    def test_check_distance(self):
        sensor = FakeSensor("Test Sensor")
        distance = sensor.distance()
        self.assertEqual(25.0, distance)

    def test_readout(self):
        sensor = FakeSensor("Testarooni")
        readout = sensor.distance_readout()
        print(readout)
        self.assertIn("Testarooni", readout)
        distance = sensor.distance()
        self.assertIn(str(distance), readout)
