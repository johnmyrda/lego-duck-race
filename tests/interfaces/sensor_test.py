from src.lego_duck_race.interfaces.sensor_interface import FakeSensor


def test_check_distance_test() -> None:
    sensor = FakeSensor("Test Sensor")
    distance = sensor.distance()
    assert distance == 25.0


def test_readout_test() -> None:
    sensor = FakeSensor("Testarooni")
    readout = sensor.distance_readout()
    print(readout)
    assert "Testarooni" in readout
    distance = sensor.distance()
    sensor = FakeSensor("Testarooni")
    assert str(distance) in readout
