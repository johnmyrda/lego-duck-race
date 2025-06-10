#Libraries
import RPi.GPIO as GPIO
import time

class Sensor:

    def __init__(self, gpio_trigger: str, gpio_echo: str, name: str):
        self.trigger = gpio_trigger
        self.echo = gpio_echo
        self.name = name
        GPIO.setmode(GPIO.BCM) # Use Broadcom GPIO 00..nn numbers
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
 
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
 
    def distance_readout(self):
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
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
