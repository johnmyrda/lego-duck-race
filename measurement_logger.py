import time
from enum import IntEnum

class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    ERROR = 3

class MeasurementLogger:

    def __init__(self, max_frequency_ms: float, name: str, level: LogLevel = LogLevel.INFO):
        self.level = level
        self.name = name
        self.max_frequency_ns = max_frequency_ms * 1000000
        self.last_log_time: int = 0
        print("Creating logger at " + str(self.level))

    def debug(self, message):
        if self.level >= LogLevel.DEBUG:
            self.log(message)

    def info(self, message):
        if self.level >= LogLevel.INFO:
            self.log(message)

    def error(self, message):
        if self.level >= LogLevel.ERROR:
            self.log(message)

    # Only log if it's been long enough since the last log
    def log(self, message: str):
        now = time.time_ns()
        elapsed_ns = now - self.last_log_time
        if (elapsed_ns > self.max_frequency_ns):
            print(self.name + ": " + message)
            self.last_log_time = time.time_ns()
            return

if __name__ == '__main__':
    logger = MeasurementLogger(1000, "Test")

    try:
        while True:
            now = time.time_ns()
            elapsed_ns = now - logger.last_log_time
            logger.info("elapsed=" + str(elapsed_ns / 1000000000.0) + "s")

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Exiting...")
