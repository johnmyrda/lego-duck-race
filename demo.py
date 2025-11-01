from arcade_controller import ArcadeController
from peripherals import detectMotor, detectSensor
import time
from buildhat import Motor, ColorDistanceSensor
from windowed_list import WindowedList

def print_debug(motor: Motor):
  data = motor.get()
  print("Speed, Pos, Apos: " + str(data))

def reset(motor: Motor):
  motor_started = False
  motor_started_forwards = False
  motor_stalled = False
  speed_window = WindowedList(5)
  while not motor_started and not motor_stalled:
    motor.start(20)
    # print_debug(motor)
    speed_window.push(motor.get_speed())
    if speed_window.mean() > 0.0:
      motor_started = True
      print("Started Reset")
    if speed_window.mean() < 0:
      motor_started_forwards = True
      print("Started forwards")
    if speed_window.stalled() and not motor_started_forwards:
      motor_stalled = True
      print("Stalled")
    # Add time between readings
    time.sleep(.05)

  reset_completed = False
  while not reset_completed and not motor_stalled:
    print_debug(motor)
    speed_window.push(motor.get_speed())
    if speed_window.stalled():
      reset_completed = True
      print("Reset Complete!")
    time.sleep(.1)
    motor.start(20)

  motor.stop()

def move_forward(motor: Motor):
  print("Moving forward!")
  motor.run_for_degrees(-500, 50)
  print("Done moving")

# Can detect speed in close to real time, check if stalled
# Window function useful but not necessary

def setup(controller: ArcadeController, motor: Motor, sensor: ColorDistanceSensor):
  sensor.on()
  controller.register_action('k1', lambda: move_forward(motor))

def main(controller: ArcadeController, motor: Motor, sensor: ColorDistanceSensor):
  while True:
      controller.update_state()
      distance = sensor.get_distance()
      # print("Distance=" + str(distance))
      if distance < 2:
          print("Resetting because distance=" + str(distance))
          controller.register_action('k1', lambda: print("Button disabled during reset"))
          reset(motor)
          controller.register_action('k1', lambda: move_forward(motor))

if __name__ == "__main__":
  controller = ArcadeController()
  controller.debug_info()
  motor = detectMotor()
  sensor = detectSensor()
  setup(controller, motor, sensor)
  main(controller, motor, sensor)
