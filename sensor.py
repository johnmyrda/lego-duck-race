#Libraries
import RPi.GPIO as GPIO
import time

# HC-SR04 Ultrasonic Distance Sensor
class Sensor:

    def __init__(self, gpio_trigger: int, gpio_echo: int, name: str):
        self.trigger = gpio_trigger
        self.echo = gpio_echo
        self.name = name
        self.last_measurement_time: int = 0
        self.last_distance = -1
        max_distance_cm = 200.0
        self.max_sensor_wait_time = .01
        GPIO.setmode(GPIO.BCM) # Use Broadcom GPIO 00..nn numbers
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        print("Sensor " + name + " initialized")

    # Returns sensor distance, or previous sensor distance if
    # it's been too soon since the function has been called
    def distance(self) -> float:
        # Hack to make sure we don't read too often
        now = time.time_ns()
        elapsed_ns = now - self.last_measurement_time
        if (elapsed_ns < 200000000): # 200 milliseconds
            return self.last_distance

        self.last_measurement_time = time.time_ns()

        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
    

        TimeoutStartTime = time.time()
        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
            # print ("StartTime: " + str(StartTime))
            if ( StartTime - TimeoutStartTime ) > self.max_sensor_wait_time:
                return self.last_distance

        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
            if ( StopTime - TimeoutStartTime ) > self.max_sensor_wait_time:
                return self.last_distance

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        self.last_distance = distance

        return distance
 
    def distance_readout(self) -> str:
        distance = self.distance()
        return f"Sensor {self.name} Distance: {distance:.1f} cm"

if __name__ == '__main__':
    # Sensor A
    GPIO_TRIGGER_A = 23
    GPIO_ECHO_A = 24
    # Sensor B
    GPIO_TRIGGER_B = 25
    GPIO_ECHO_B = 5
    # Sensor C
    GPIO_TRIGGER_C = 6
    GPIO_ECHO_C = 12
    sensor_a = Sensor(GPIO_TRIGGER_A, GPIO_ECHO_A, "A")
    sensor_b = Sensor(GPIO_TRIGGER_B, GPIO_ECHO_B, "B")
    sensor_c = Sensor(GPIO_TRIGGER_C, GPIO_ECHO_C, "C")

    try:
        while True:
            dist_a = sensor_a.distance_readout()
            dist_b = sensor_b.distance_readout()
            dist_c = sensor_c.distance_readout()
            print("-"*len(dist_a))
            print(dist_a)
            print(dist_b)
            print(dist_c)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
