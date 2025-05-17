from peripherals import detectMotor, detectSensor
import time
from buildhat import Motor, ColorDistanceSensor
from windowed_list import WindowedList
from gpiozero import Button

# hub.system.set_stop_button(None)

def print_debug(motor: Motor):
  data = motor.get()
  print("Speed, Pos, Apos: " + str(data))

def reset(motor: Motor):
  motor_started = False
  motor_started_forwards = False
  motor_stalled = False
  speed_window = WindowedList(5)
  while not motor_started and not motor_stalled:
    # print_debug(motor)
    speed_window.push(motor.get_speed())
    if speed_window.mean() < 0.0:
      motor_started = True
      print("Started Reset")
    if speed_window.mean() > 0:
      motor_started_forwards = True
      print("Started forwards")
    if speed_window.stalled() and not motor_started_forwards:
      motor_stalled = True
      print("Stalled")
    # Add time between readings
    time.sleep(.05)
    motor.start(-20)

  reset_completed = False
  while not reset_completed and not motor_stalled:
    print_debug(motor)
    speed_window.push(motor.get_speed())
    if speed_window.stalled():
      reset_completed = True
      print("Reset Complete!")
    time.sleep(.1)
    motor.start(-20)


  motor.stop()

# reset(motor)

# print("Moving forward")
# motor.run_for_degrees(180, 50)

# motor.start(50)
# time.sleep(1)
# motor.stop()

def move_forward(motor: Motor):
  print("Moving forward!")
  motor.run_for_degrees(180, 50)
  print("Done moving")

# Can detect speed in close to real time, check if stalled
# Window function useful but not necessary

def setup(button: Button, motor: Motor, sensor: ColorDistanceSensor):
  sensor.on()
  button.when_activated = lambda: move_forward(motor)
  button.when_held = lambda: reset(motor)

def main(button: Button, motor: Motor, sensor: ColorDistanceSensor):
  while True:
      distance = sensor.get_distance()
      print("Distance=" + str(distance))
      if (distance < 2):
          print("Resetting because distance=" + str(distance))
          button.when_activated = lambda: print("Button disabled during reset")
          reset(motor)
          button.when_activated = lambda: move_forward(motor)

          print("Reset complete")

if __name__ == "__main__":
  button = Button(26, hold_time=5)
  motor = detectMotor()
  sensor = detectSensor()
  setup(button, motor, sensor)
  main(button, motor, sensor)