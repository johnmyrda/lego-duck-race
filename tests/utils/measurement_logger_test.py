import time

from lego_duck_race.utils.measurement_logger import MeasurementLogger


def test_measurement_logger() -> None:
    logger = MeasurementLogger(1000, "Test")
    logger.info("initial log")
    assert logger.last_log_time > 0
    first_log_time = logger.last_log_time
    time.sleep(0.1)
    logger.info("second log")
    assert logger.last_log_time == first_log_time


def test_measurement_logger_multiple() -> None:
    logger = MeasurementLogger(50, "Test")
    logger.info("initial log")
    assert logger.last_log_time > 0
    first_log_time = logger.last_log_time
    time.sleep(0.1)
    logger.info("second log")
    assert logger.last_log_time != first_log_time
