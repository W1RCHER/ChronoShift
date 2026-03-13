from dataclasses import dataclass

import arcade

from game.config.settings import EXIT_HEIGHT, EXIT_WIDTH, PLATFORM_TEXTURE_PATH, PORTAL_TEXTURE_PATH
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
    exit_sprite: arcade.Sprite
    world_left: float
    world_right: float
    world_bottom: float
    world_top: float


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

        left_edges: list[float] = []
        right_edges: list[float] = []
        top_edges: list[float] = []

        for block in level.platforms:
            platform = arcade.Sprite(str(PLATFORM_TEXTURE_PATH))

            visual_height = max(int(block.height * 2.0), 52)
            platform.center_x = block.center_x
            platform.center_y = block.center_y - (visual_height - block.height) / 2
            platform.width = block.width
            platform.height = visual_height

            platform_list.append(platform)

            left_edges.append(block.center_x - block.width / 2)
            right_edges.append(block.center_x + block.width / 2)
            top_edges.append(block.center_y + block.height / 2)

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

        exit_sprite = arcade.Sprite(str(PORTAL_TEXTURE_PATH))
        exit_sprite.center_x = level.exit_x
        exit_sprite.center_y = level.exit_y
        exit_sprite.width = EXIT_WIDTH
        exit_sprite.height = EXIT_HEIGHT

        left_edges.append(level.spawn_x)
        right_edges.append(level.exit_x + EXIT_WIDTH / 2)
        top_edges.append(level.exit_y + EXIT_HEIGHT / 2)

        world_left = min(left_edges)
        world_right = max(right_edges)
        world_bottom = 0
        world_top = max(top_edges) + 160

        return RuntimeLevel(
            title=level.title,
            spawn_x=level.spawn_x,
            spawn_y=level.spawn_y,
            platform_list=platform_list,
            enemy_list=enemy_list,
            core_list=core_list,
            exit_sprite=exit_sprite,
            world_left=world_left,
            world_right=world_right,
            world_bottom=world_bottom,
            world_top=world_top,
        )