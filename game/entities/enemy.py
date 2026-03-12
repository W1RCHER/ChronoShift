import random
from pathlib import Path

import arcade

from game.config.settings import (
    ENEMY_ATTACK_ANIMATION_SPEED,
    ENEMY_ATTACK_TRIGGER_X,
    ENEMY_ATTACK_TRIGGER_Y,
    ENEMY_SPRITES_DIR,
    ENEMY_TEXTURE_SCALE,
    ENEMY_WALK_ANIMATION_SPEED,
)


class Enemy(arcade.Sprite):
    """Враг со случайным выбором типа: spider или crab."""

    ENEMY_TYPES = ("spider", "crab")

    def __init__(
        self,
        center_x: float,
        center_y: float,
        patrol_left: float,
        patrol_right: float,
        speed: float,
    ) -> None:
        super().__init__(scale=ENEMY_TEXTURE_SCALE)

        self.center_x = center_x
        self.center_y = center_y

        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.move_speed = speed
        self.change_x = speed
        self.facing = 1

        self.enemy_type = random.choice(self.ENEMY_TYPES)

        self.texture_timer = 0.0
        self.animation_index = 0
        self.is_attacking = False

        self.walk_right, self.walk_left = self._load_sequence(
            [
                f"enemy_{self.enemy_type}_walk_01.png",
                f"enemy_{self.enemy_type}_walk_02.png",
                f"enemy_{self.enemy_type}_walk_03.png",
                f"enemy_{self.enemy_type}_walk_04.png",
                f"enemy_{self.enemy_type}_walk_05.png",
            ]
        )

        self.attack_right, self.attack_left = self._load_sequence(
            [
                f"enemy_{self.enemy_type}_attack_01.png",
                f"enemy_{self.enemy_type}_attack_02.png",
                f"enemy_{self.enemy_type}_attack_03.png",
                f"enemy_{self.enemy_type}_attack_04.png",
                f"enemy_{self.enemy_type}_attack_05.png",
            ]
        )

        self.texture = self.walk_right[0]

    @staticmethod
    def _texture_path(filename: str) -> Path:
        return ENEMY_SPRITES_DIR / filename

    def _load_single(self, filename: str) -> tuple[arcade.Texture, arcade.Texture]:
        path = self._texture_path(filename)
        right = arcade.load_texture(str(path))
        left = right.flip_left_right()
        return right, left

    def _load_sequence(self, filenames: list[str]) -> tuple[list[arcade.Texture], list[arcade.Texture]]:
        right_list: list[arcade.Texture] = []
        left_list: list[arcade.Texture] = []

        for filename in filenames:
            right, left = self._load_single(filename)
            right_list.append(right)
            left_list.append(left)

        return right_list, left_list

    def _get_directional_sequence(
        self,
        right_textures: list[arcade.Texture],
        left_textures: list[arcade.Texture],
    ) -> list[arcade.Texture]:
        return right_textures if self.facing >= 0 else left_textures

    def _animate_sequence(self, textures: list[arcade.Texture], delta_time: float, speed: float) -> None:
        self.texture_timer += delta_time

        if self.texture_timer >= speed:
            self.texture_timer = 0.0
            self.animation_index = (self.animation_index + 1) % len(textures)

        self.texture = textures[self.animation_index]

    def _reset_animation(self) -> None:
        self.texture_timer = 0.0
        self.animation_index = 0

    def _check_attack_state(self, player: arcade.Sprite | None) -> bool:
        if player is None:
            return False

        close_x = abs(player.center_x - self.center_x) <= ENEMY_ATTACK_TRIGGER_X
        close_y = abs(player.center_y - self.center_y) <= ENEMY_ATTACK_TRIGGER_Y
        return close_x and close_y

    def update_enemy(self, player: arcade.Sprite | None, delta_time: float) -> None:
        should_attack = self._check_attack_state(player)

        if should_attack:
            if not self.is_attacking:
                self._reset_animation()

            self.is_attacking = True

            if player is not None:
                self.facing = 1 if player.center_x >= self.center_x else -1

            attack_textures = self._get_directional_sequence(self.attack_right, self.attack_left)
            self._animate_sequence(attack_textures, delta_time, ENEMY_ATTACK_ANIMATION_SPEED)
            return

        if self.is_attacking:
            self._reset_animation()

        self.is_attacking = False

        self.center_x += self.change_x

        if self.center_x <= self.patrol_left:
            self.center_x = self.patrol_left
            self.change_x = abs(self.move_speed)
            self.facing = 1

        elif self.center_x >= self.patrol_right:
            self.center_x = self.patrol_right
            self.change_x = -abs(self.move_speed)
            self.facing = -1

        walk_textures = self._get_directional_sequence(self.walk_right, self.walk_left)
        self._animate_sequence(walk_textures, delta_time, ENEMY_WALK_ANIMATION_SPEED)