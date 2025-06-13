from controller import Controller, Direction
from sensor import Sensor
from ducklane import DuckLane, LaneState
import time

class Game:

    def __init__(self, controller: Controller, lanes: list[DuckLane]):
        self.update_period_ns = 10 * 1000000 # 1000000 ns per ms
        self.last_update_time: int = 0
        controller.debug_info()
        print("Starting Duck Race")
        self.controller = controller
        self.lanes = lanes
        self.joystick_direction = Direction.NONE
        self.selected_lane = 0
        self.last_winner = None

    # Controls are reversed due to joystick placement
    def update_joystick(self):
        joystick = self.controller.joystick
        cur_direction = self.joystick_direction
        new_direction = Direction.NONE
        if joystick.left:
            new_direction = Direction.LEFT
        elif joystick.right:
            new_direction = Direction.RIGHT
        elif joystick.up:
            new_direction = Direction.UP
        elif joystick.down:
            new_direction = Direction.DOWN
        direction_changed = False
        if cur_direction != new_direction:
            direction_changed = True
            self.joystick_direction = new_direction
            
        if new_direction == Direction.LEFT or new_direction == Direction.RIGHT:
            if joystick.down:
                for i in range(len(self.lanes)):
                    self.move_lane(i, new_direction)
            else:
                for i in range(len(self.lanes)):
                    if i == self.selected_lane:
                        self.move_lane(i, new_direction)
                    else:
                        self.lanes[i].stop()
                self.move_lane(self.selected_lane, new_direction)
            return # Return early to avoid changing lane while moving

        if direction_changed:
            if new_direction == Direction.NONE:
                if cur_direction == Direction.LEFT or cur_direction == Direction.RIGHT:
                    for lane in self.lanes:
                        lane.stop()
                    return # Return early to avoid changing lane while moving

            if new_direction == Direction.UP:
                self.selected_lane = max(self.selected_lane -1, 0)
            if new_direction == Direction.DOWN:
                self.selected_lane = min(self.selected_lane + 1, len(self.lanes) - 1)

    def move_lane(self, lane_index: int, direction: Direction):
        lane = self.lanes[lane_index]
        if direction == Direction.LEFT:
            lane.move_forward_override()
        elif direction == Direction.RIGHT:
            lane.move_backward_override()

    def _update(self):
        controller.update_state()
        for lane in self.lanes:
            lane.update()
        self.update_joystick()
        winner = self.get_winner()
        if winner != None and winner != self.last_winner:
            print(f"Winner: {winner.name}")
            self.last_winner = winner
            self.reset_all()

    def update(self):
        now = time.time_ns()
        elapsed_ns = now - self.last_update_time
        if (elapsed_ns > self.update_period_ns):
            self._update()
            self.last_update_time = time.time_ns()    

    def reset_all(self):
        for lane in self.lanes:
            if lane.status == LaneState.RESETTING:
                pass
            else:
                lane.reset()

    def get_winner(self) -> DuckLane | None:
        for lane in self.lanes:
            if lane.passed_finish_line():
                return lane
        else:
            return None

if __name__ == "__main__":
    controller = Controller()
    button_a = controller.get_button("k1")
    button_b = controller.get_button("k2")
    button_c = controller.get_button("k3")
    # Lane A
    GPIO_TRIGGER_A = 23
    GPIO_ECHO_A = 24
    sensor_a = Sensor(GPIO_TRIGGER_A, GPIO_ECHO_A, "A")
    lane_a = DuckLane("A", button_a, sensor_a, start_pos=47)
    # Lane B
    GPIO_TRIGGER_B = 25
    GPIO_ECHO_B = 5
    sensor_b = Sensor(GPIO_TRIGGER_B, GPIO_ECHO_B, "B")
    lane_b = DuckLane("B", button_b, sensor_b)
    # Lane C
    GPIO_TRIGGER_C = 6
    GPIO_ECHO_C = 12
    sensor_c = Sensor(GPIO_TRIGGER_C, GPIO_ECHO_C, "C")
    lane_c = DuckLane("C", button_c, sensor_c)
    game = Game(controller, [lane_a, lane_b, lane_c])
    while True:
        game.update()
