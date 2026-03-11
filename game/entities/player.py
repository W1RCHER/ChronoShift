from pathlib import Path

import arcade

from game.config.player_config import MAIN_HERO_STATS
from game.config.settings import (
    FLIGHT_ANIMATION_SPEED,
    HORIZONTAL_MOVE_DEADZONE,
    IDLE_ANIMATION_SPEED,
    LAND_ANIMATION_DURATION,
    PLAYER_RUN_MULTIPLIER,
    PLAYER_SPRITES_DIR,
    PLAYER_TEXTURE_SCALE,
    RUN_ANIMATION_SPEED,
    VERTICAL_MOVE_DEADZONE,
    WALK_ANIMATION_SPEED,
)


class Player(arcade.Sprite):
    def __init__(self, center_x: float, center_y: float) -> None:
        super().__init__(scale=PLAYER_TEXTURE_SCALE)

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
        self.is_flying = False

        self.texture_timer = 0.0
        self.animation_index = 0
        self.land_timer = 0.0
        self.was_on_ground = False

        self.idle_right, self.idle_left = self._load_sequence(
            [
                "hero_idle_01.png",
                "hero_idle_02.png",
                "hero_idle_03.png",
                "hero_idle_04.png",
                "hero_idle_05.png",
            ]
        )

        self.walk_right, self.walk_left = self._load_sequence(
            [
                "hero_walk_01.png",
                "hero_walk_02.png",
                "hero_walk_03.png",
                "hero_walk_04.png",
                "hero_walk_05.png",
            ]
        )

        self.run_right, self.run_left = self._load_sequence(
            [
                "hero_run_01.png",
                "hero_run_02.png",
                "hero_run_03.png",
                "hero_run_04.png",
                "hero_run_05.png",
            ]
        )

        self.jump_prepare_right, self.jump_prepare_left = self._load_single("hero_jump_prepare_01.png")
        self.jump_up_right, self.jump_up_left = self._load_single("hero_jump_up_01.png")
        self.jump_float_right, self.jump_float_left = self._load_single("hero_jump_float_01.png")
        self.fall_right, self.fall_left = self._load_single("hero_fall_01.png")
        self.land_right, self.land_left = self._load_single("hero_land_01.png")
        self.flight_start_right, self.flight_start_left = self._load_single("hero_flight_start_01.png")
        self.flight_end_right, self.flight_end_left = self._load_single("hero_flight_end_01.png")

        self.texture = self.idle_right[0]

    @staticmethod
    def _texture_path(filename: str) -> Path:
        return PLAYER_SPRITES_DIR / filename

    def _load_single(self, filename: str) -> tuple[arcade.Texture, arcade.Texture]:
        path = self._texture_path(filename)
        right = arcade.load_texture(str(path))
        left = arcade.load_texture(str(path), flipped_horizontally=True)
        return right, left

    def _load_sequence(self, filenames: list[str]) -> tuple[list[arcade.Texture], list[arcade.Texture]]:
        right_list: list[arcade.Texture] = []
        left_list: list[arcade.Texture] = []

        for filename in filenames:
            right, left = self._load_single(filename)
            right_list.append(right)
            left_list.append(left)

        return right_list, left_list

    def _get_directional_texture(
        self,
        right_texture: arcade.Texture,
        left_texture: arcade.Texture,
    ) -> arcade.Texture:
        return right_texture if self.facing >= 0 else left_texture

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

    def _set_single_texture(
        self,
        right_texture: arcade.Texture,
        left_texture: arcade.Texture,
    ) -> None:
        self.texture = self._get_directional_texture(right_texture, left_texture)

    def _reset_animation_cycle(self) -> None:
        self.texture_timer = 0.0
        self.animation_index = 0

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
        self.is_flying = False
        self.land_timer = 0.0
        self.was_on_ground = False
        self._reset_animation_cycle()
        self.texture = self.idle_right[0] if self.facing >= 0 else self.idle_left[0]

        if full_heal:
            self.heal_full()

    def set_flight_state(self, active: bool) -> None:
        if self.is_flying != active:
            self._reset_animation_cycle()
        self.is_flying = active

    def update_animation_state(self, delta_time: float) -> None:
        if self.change_x > HORIZONTAL_MOVE_DEADZONE:
            self.facing = 1
        elif self.change_x < -HORIZONTAL_MOVE_DEADZONE:
            self.facing = -1

        if self.on_ground and not self.was_on_ground:
            self.land_timer = LAND_ANIMATION_DURATION

        self.was_on_ground = self.on_ground

        if self.land_timer > 0:
            self.land_timer -= delta_time
            self._set_single_texture(self.land_right, self.land_left)
            return

        if self.is_flying:
            flight_textures = self._get_directional_sequence(
                [self.flight_start_right, self.jump_float_right, self.flight_end_right],
                [self.flight_start_left, self.jump_float_left, self.flight_end_left],
            )
            self._animate_sequence(flight_textures, delta_time, FLIGHT_ANIMATION_SPEED)
            return

        if not self.on_ground:
            if self.change_y > VERTICAL_MOVE_DEADZONE:
                self._set_single_texture(self.jump_up_right, self.jump_up_left)
            elif self.change_y < -VERTICAL_MOVE_DEADZONE:
                self._set_single_texture(self.fall_right, self.fall_left)
            else:
                self._set_single_texture(self.jump_float_right, self.jump_float_left)
            return

        if abs(self.change_x) > HORIZONTAL_MOVE_DEADZONE:
            if self.is_running:
                run_textures = self._get_directional_sequence(self.run_right, self.run_left)
                self._animate_sequence(run_textures, delta_time, RUN_ANIMATION_SPEED)
            else:
                walk_textures = self._get_directional_sequence(self.walk_right, self.walk_left)
                self._animate_sequence(walk_textures, delta_time, WALK_ANIMATION_SPEED)
            return

        idle_textures = self._get_directional_sequence(self.idle_right, self.idle_left)
        self._animate_sequence(idle_textures, delta_time, IDLE_ANIMATION_SPEED)