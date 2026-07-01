from lego_duck_race.ducklane import DuckLane, LaneState
from lego_duck_race.game import Game
from lego_duck_race.interfaces.controller_base import Button, Direction
from lego_duck_race.sim.fakes import FakeController, FakeLimitSwitch, FakeMotor


def make_lane(name: str, finish_line_active: bool = False) -> tuple[DuckLane, FakeMotor]:
    motor = FakeMotor(name)
    lane = DuckLane(name, motor, Button(name), FakeLimitSwitch(finish_line_active))
    return lane, motor


def make_game(lanes: list[DuckLane]) -> Game:
    return Game(FakeController(), lanes)


def test_game_import_does_not_require_hardware() -> None:
    # Import is intentionally inside the test: this should not require buildhat, gpiozero, or hid.
    import lego_duck_race.game  # noqa: F401


def test_get_winner_returns_first_lane_past_finish() -> None:
    lane_a, _ = make_lane("A")
    lane_b, _ = make_lane("B", finish_line_active=True)
    game = make_game([lane_a, lane_b])

    assert game.get_winner() is lane_b


def test_get_winner_returns_none_while_any_lane_is_resetting() -> None:
    lane_a, _ = make_lane("A")
    lane_b, _ = make_lane("B", finish_line_active=True)
    lane_a.status = LaneState.RESETTING
    game = make_game([lane_a, lane_b])

    assert game.get_winner() is None


def test_selected_lane_moves_and_other_lanes_stop() -> None:
    lane_a, motor_a = make_lane("A")
    lane_b, motor_b = make_lane("B")
    controller = FakeController()
    game = Game(controller, [lane_a, lane_b])
    game.selected_lane = 1
    controller.joystick.left = True

    game.update_joystick()

    assert motor_a.speed == 0
    assert motor_a.stop_count == 1
    assert motor_b.speed == 100
    assert game.joystick_direction == Direction.LEFT


def test_down_plus_horizontal_moves_all_lanes() -> None:
    lane_a, motor_a = make_lane("A")
    lane_b, motor_b = make_lane("B")
    controller = FakeController()
    game = Game(controller, [lane_a, lane_b])
    controller.joystick.down = True
    controller.joystick.right = True

    game.update_joystick()

    assert [motor_a.speed, motor_b.speed] == [-100, -100]
