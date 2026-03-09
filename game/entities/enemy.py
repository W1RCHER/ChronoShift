import arcade

from game.config.settings import COLOR_ENEMY, ENEMY_HEIGHT, ENEMY_WIDTH


class Enemy(arcade.SpriteSolidColor):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        patrol_left: float,
        patrol_right: float,
        speed: float,
    ) -> None:
        super().__init__(
            width=ENEMY_WIDTH,
            height=ENEMY_HEIGHT,
            color=COLOR_ENEMY,
        )

        self.center_x = center_x
        self.center_y = center_y
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.move_speed = speed
        self.change_x = speed
        self.facing = 1

    def update_enemy(self) -> None:
        self.center_x += self.change_x

        if self.center_x <= self.patrol_left:
            self.center_x = self.patrol_left
            self.change_x = abs(self.move_speed)
            self.facing = 1

        elif self.center_x >= self.patrol_right:
            self.center_x = self.patrol_right
            self.change_x = -abs(self.move_speed)
            self.facing = -1