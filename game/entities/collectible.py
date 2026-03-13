import math

import arcade

from game.config.settings import (
    CORE_FLOAT_AMPLITUDE,
    CORE_FLOAT_SPEED,
    CORE_TEXTURE_SCALE,
    ITEMS_SPRITES_DIR,
)


class EnergyCore(arcade.Sprite):
    def __init__(self, center_x: float, center_y: float) -> None:
        super().__init__(
            str(ITEMS_SPRITES_DIR / "energy_core.png"),
            scale=CORE_TEXTURE_SCALE,
        )

        self.center_x = center_x
        self.center_y = center_y
        self.base_y = center_y
        self.float_time = 0.0
        self.value = 100

    def update(self, delta_time: float = 1 / 60) -> None:
        self.float_time += delta_time
        self.center_y = self.base_y + math.sin(self.float_time * CORE_FLOAT_SPEED * math.pi) * CORE_FLOAT_AMPLITUDE

    def collect(self) -> int:
        self.remove_from_sprite_lists()
        return self.value