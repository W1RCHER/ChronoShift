from dataclasses import dataclass

from game.config.settings import (
    COLOR_PLAYER,
    PLAYER_DASH_SPEED,
    PLAYER_HEIGHT,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVE_SPEED,
    PLAYER_WIDTH,
)


@dataclass(frozen=True)
class HeroStats:
    max_health: int
    move_speed: float
    jump_speed: float
    dash_speed: float
    gravity_scale: float


@dataclass(frozen=True)
class HeroVisual:
    width: int
    height: int
    color: tuple[int, int, int]


MAIN_HERO_STATS = HeroStats(
    max_health=3,
    move_speed=PLAYER_MOVE_SPEED,
    jump_speed=PLAYER_JUMP_SPEED,
    dash_speed=PLAYER_DASH_SPEED,
    gravity_scale=1.0,
)

MAIN_HERO_VISUAL = HeroVisual(
    width=PLAYER_WIDTH,
    height=PLAYER_HEIGHT,
    color=COLOR_PLAYER,
)