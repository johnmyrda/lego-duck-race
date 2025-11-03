#!/usr/bin/env python3

from asciimatics.effects import Effect, Sprite
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from lego_duck_race.assets.loader import load_asset


class Wave(Sprite):
    def __init__(
        self,
        screen: Screen,
        path: Path,
        colour: int = Screen.COLOUR_WHITE,
        start_frame: int = 0,
        stop_frame: int = 0,
    ):
        """
        See :py:obj:`.Sprite` for details.
        """
        super().__init__(
            screen,
            renderer_dict={"default": StaticRenderer(images=[load_asset("wave.txt") * 6])},
            path=path,
            colour=colour,
            start_frame=start_frame,
            stop_frame=stop_frame,
        )


class Duck(Sprite):
    def __init__(
        self,
        screen: Screen,
        path: Path,
        colour: int = Screen.COLOUR_WHITE,
        start_frame: int = 0,
        stop_frame: int = 0,
    ):
        """
        See :py:obj:`.Sprite` for details.
        """
        super().__init__(
            screen,
            renderer_dict={"default": StaticRenderer(images=[load_asset("duck.txt")])},
            path=path,
            colour=colour,
            start_frame=start_frame,
            stop_frame=stop_frame,
        )


def wave_path() -> Path:
    path = Path()
    path.jump_to(20, 25)
    return path


def duck_path() -> Path:
    path = Path()
    path.jump_to(20, 20)
    path.move_straight_to(70, 20, 30)
    return path


def demo(screen: Screen) -> None:
    effects: list[Effect] = [
        Wave(screen, wave_path(), Screen.COLOUR_BLUE, 0, 60),
        Duck(screen, duck_path(), Screen.COLOUR_YELLOW, 0, 60),
        # Stars(screen, (screen.width + screen.height) // 2)
    ]
    screen.play([Scene(effects, 500)])
