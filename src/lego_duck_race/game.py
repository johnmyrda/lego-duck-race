import time
from typing import Protocol

from lego_duck_race.ducklane import DuckLane, LaneState
from lego_duck_race.hardware.factory import build_hardware_lanes
from lego_duck_race.hardware.hid_controller import ArcadeController
from lego_duck_race.interfaces.controller_base import Direction, Joystick


class Controller(Protocol):
    joystick: Joystick

    def update_state(self) -> None:
        """Refresh controller state from its backing implementation."""
        ...


class Game:
    def __init__(self, controller: Controller, lanes: list[DuckLane]):
        self.update_period_ns = 10 * 1000000  # 1000000 ns per ms
        self.last_update_time: int = 0
        print("Starting Duck Race...")
        self.controller = controller
        self.lanes = lanes
        self.joystick_direction = Direction.NONE
        self.selected_lane = 0

    # Controls are reversed due to joystick placement
    def update_joystick(self) -> None:
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
                        self.lanes[i].motor.stop()
            return  # Return early to avoid changing lane while moving

        if direction_changed:
            if new_direction == Direction.NONE and (
                cur_direction == Direction.LEFT or cur_direction == Direction.RIGHT
            ):
                for lane in self.lanes:
                    lane.motor.stop()
                return  # Return early to avoid changing lane while moving

            if new_direction == Direction.UP:
                self.selected_lane = max(self.selected_lane - 1, 0)
            if new_direction == Direction.DOWN:
                self.selected_lane = min(self.selected_lane + 1, len(self.lanes) - 1)

    def move_lane(self, lane_index: int, direction: Direction) -> None:
        lane = self.lanes[lane_index]
        if direction == Direction.LEFT:
            lane.motor.start(100)
        elif direction == Direction.RIGHT:
            lane.motor.start(-100)

    def _update(self) -> None:
        self.controller.update_state()
        self.update_joystick()
        winner = self.get_winner()
        if winner is not None:
            print(f"Winner: {winner.name}")
            self.reset_all()

    def update(self) -> None:
        now = time.time_ns()
        elapsed_ns = now - self.last_update_time
        if elapsed_ns > self.update_period_ns:
            self._update()
            self.last_update_time = time.time_ns()

    def reset_all(self) -> None:
        for lane in self.lanes:
            if lane.status == LaneState.RESETTING:
                pass
            else:
                lane.reset()

    def get_winner(self) -> DuckLane | None:
        for lane in self.lanes:
            if lane.status == LaneState.RESETTING:
                return None
            if lane.passed_finish_line():
                return lane
        return None


def main() -> None:
    controller = ArcadeController()
    controller.debug_info()
    game = Game(controller, build_hardware_lanes(controller))
    print("Game initialized!")
    while True:
        game.update()
