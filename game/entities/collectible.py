import arcade

from game.config.settings import COLOR_CORE, CORE_SIZE


class EnergyCore(arcade.SpriteSolidColor):
    def __init__(self, center_x: float, center_y: float) -> None:
        super().__init__(
            width=CORE_SIZE,
            height=CORE_SIZE,
            color=COLOR_CORE,
        )

        self.center_x = center_x
        self.center_y = center_y
        self.value = 100

    def collect(self) -> int:
        self.remove_from_sprite_lists()
        return self.value