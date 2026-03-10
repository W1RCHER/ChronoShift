import arcade

from game.config.player_config import MAIN_HERO_STATS, MAIN_HERO_VISUAL
from game.config.settings import PLAYER_RUN_MULTIPLIER


class Player(arcade.SpriteSolidColor):
    """Главный герой."""

    def __init__(self, center_x: float, center_y: float) -> None:
        super().__init__(
            width=MAIN_HERO_VISUAL.width,
            height=MAIN_HERO_VISUAL.height,
            color=MAIN_HERO_VISUAL.color,
        )

        self.center_x = center_x
        self.center_y = center_y

        self.max_health = MAIN_HERO_STATS.max_health
        self.health = MAIN_HERO_STATS.max_health

        self.base_move_speed = MAIN_HERO_STATS.move_speed
        self.move_speed = MAIN_HERO_STATS.move_speed
        self.run_multiplier = PLAYER_RUN_MULTIPLIER

        self.jump_speed = MAIN_HERO_STATS.jump_speed
        self.dash_speed = MAIN_HERO_STATS.dash_speed
        self.gravity_scale = MAIN_HERO_STATS.gravity_scale

        self.on_ground = False
        self.facing = 1
        self.is_running = False

    def move_left(self, run: bool = False) -> None:
        speed = self.base_move_speed * self.run_multiplier if run else self.base_move_speed
        self.change_x = -speed
        self.facing = -1
        self.is_running = run

    def move_right(self, run: bool = False) -> None:
        speed = self.base_move_speed * self.run_multiplier if run else self.base_move_speed
        self.change_x = speed
        self.facing = 1
        self.is_running = run

    def stop_horizontal(self) -> None:
        self.change_x = 0
        self.is_running = False

    def jump(self) -> None:
        if self.on_ground:
            self.change_y = self.jump_speed
            self.on_ground = False

    def take_damage(self, amount: int = 1) -> None:
        self.health = max(0, self.health - amount)

    def heal_full(self) -> None:
        self.health = self.max_health

    def respawn(self, center_x: float, center_y: float, full_heal: bool = False) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False
        self.is_running = False

        if full_heal:
            self.heal_full()

    def update_animation_state(self) -> None:
        pass