import time
from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    ERROR = 3


class Logger:
    def __init__(self, name: str, level: LogLevel = LogLevel.INFO):
        self.level = level
        self.name = name
        print(f"Creating logger {name} at {self.level.name}")

    def debug(self, message: str) -> None:
        self.log(message, LogLevel.DEBUG)

    def info(self, message: str) -> None:
        self.log(message, LogLevel.INFO)

    def error(self, message: str) -> None:
        self.log(message, LogLevel.ERROR)

    # Only log if it's been long enough since the last log
    def log(self, message: str, level: LogLevel) -> None:
        if self.level <= level:
            print(self.name + ": " + message)


class MeasurementLogger(Logger):
    def __init__(self, min_period_ms: float, name: str, level: LogLevel = LogLevel.INFO):
        Logger.__init__(self, name, level)
        self.min_period_ns = min_period_ms * 1000000
        self.last_log_time: int = 0
        print(f"Creating logger {name} at {self.level.name}")

    # Only log if it's been long enough since the last log
    def log(self, message: str, level: LogLevel) -> None:
        if self.level <= level:
            now = time.time_ns()
            elapsed_ns = now - self.last_log_time
            if elapsed_ns > self.min_period_ns:
                print(self.name + ": " + message)
                self.last_log_time = time.time_ns()
                return


if __name__ == "__main__":
    logger = MeasurementLogger(1000, "Test")

    try:
        while True:
            now = time.time_ns()
            elapsed_ns = now - logger.last_log_time
            logger.info("elapsed=" + str(elapsed_ns / 1000000000.0) + "s")

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Exiting...")
