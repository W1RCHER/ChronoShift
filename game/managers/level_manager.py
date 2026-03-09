from dataclasses import dataclass

import arcade

from game.config.settings import COLOR_EXIT, EXIT_HEIGHT, EXIT_WIDTH
from game.data.level_data import LEVELS
from game.entities.collectible import EnergyCore
from game.entities.enemy import Enemy


@dataclass
class RuntimeLevel:
    title: str
    spawn_x: float
    spawn_y: float
    platform_list: arcade.SpriteList
    enemy_list: arcade.SpriteList
    core_list: arcade.SpriteList
    exit_sprite: arcade.SpriteSolidColor


class LevelManager:
    def __init__(self) -> None:
        self.levels = LEVELS

    def get_level_count(self) -> int:
        return len(self.levels)

    def build_level(self, level_index: int) -> RuntimeLevel:
        level = self.levels[level_index]

        platform_list = arcade.SpriteList(use_spatial_hash=True)
        enemy_list = arcade.SpriteList()
        core_list = arcade.SpriteList()

        for block in level.platforms:
            platform = arcade.SpriteSolidColor(
                width=block.width,
                height=block.height,
                color=block.color,
            )
            platform.center_x = block.center_x
            platform.center_y = block.center_y
            platform_list.append(platform)

        for enemy_data in level.enemies:
            enemy = Enemy(
                center_x=enemy_data.center_x,
                center_y=enemy_data.center_y,
                patrol_left=enemy_data.patrol_left,
                patrol_right=enemy_data.patrol_right,
                speed=enemy_data.speed,
            )
            enemy_list.append(enemy)

        for core_data in level.cores:
            core = EnergyCore(
                center_x=core_data.center_x,
                center_y=core_data.center_y,
            )
            core_list.append(core)

        exit_sprite = arcade.SpriteSolidColor(
            width=EXIT_WIDTH,
            height=EXIT_HEIGHT,
            color=COLOR_EXIT,
        )
        exit_sprite.center_x = level.exit_x
        exit_sprite.center_y = level.exit_y

        return RuntimeLevel(
            title=level.title,
            spawn_x=level.spawn_x,
            spawn_y=level.spawn_y,
            platform_list=platform_list,
            enemy_list=enemy_list,
            core_list=core_list,
            exit_sprite=exit_sprite,
        )