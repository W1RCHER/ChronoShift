import arcade

from game.config.settings import (
    CAMERA_SPEED,
    CAMERA_Y_OFFSET,
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    GRAVITY,
    HUD_MARGIN,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WORLD_BOTTOM_DEATH_Y,
)
from game.entities.player import Player
from game.managers.level_manager import LevelManager


class GameView(arcade.View):
    """Основной игровой экран."""

    def __init__(self) -> None:
        super().__init__()

        self.level_manager = LevelManager()

        self.player: Player | None = None
        self.platform_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.core_list = arcade.SpriteList()
        self.exit_sprite: arcade.SpriteSolidColor | None = None

        self.left_pressed = False
        self.right_pressed = False

        self.current_level_title = ""
        self.spawn_x = 100
        self.spawn_y = 180

        self.camera: arcade.Camera2D | None = None

        self.world_left = 0.0
        self.world_right = float(SCREEN_WIDTH)
        self.world_bottom = 0.0
        self.world_top = float(SCREEN_HEIGHT)

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BACKGROUND)

        # Не перезагружаем уровень каждый раз при возврате из паузы
        if self.player is None:
            self.load_level(self.window.game_state.current_level_index)

    def load_level(self, level_index: int) -> None:
        runtime_level = self.level_manager.build_level(level_index)

        self.current_level_title = runtime_level.title
        self.spawn_x = runtime_level.spawn_x
        self.spawn_y = runtime_level.spawn_y

        self.platform_list = runtime_level.platform_list
        self.enemy_list = runtime_level.enemy_list
        self.core_list = runtime_level.core_list
        self.exit_sprite = runtime_level.exit_sprite

        self.world_left = runtime_level.world_left
        self.world_right = runtime_level.world_right
        self.world_bottom = runtime_level.world_bottom
        self.world_top = runtime_level.world_top

        self.player = Player(self.spawn_x, self.spawn_y)
        self.window.game_state.player_health = self.player.health

        self.left_pressed = False
        self.right_pressed = False

        self.setup_camera()
        self.setup_particles()
        self.setup_physics()

    def setup_camera(self) -> None:
        self.camera = arcade.Camera2D()
        self.update_camera(snap=True)

    def setup_particles(self) -> None:
        """Заготовка под частицы."""
        pass

    def setup_physics(self) -> None:
        """Заготовка под физический движок."""
        pass

    def on_draw(self) -> None:
        self.clear()

        if self.camera is not None:
            self.camera.use()

        self.platform_list.draw()
        self.enemy_list.draw()
        self.core_list.draw()

        if self.exit_sprite is not None:
            arcade.draw_sprite(self.exit_sprite)

        if self.player is not None:
            arcade.draw_sprite(self.player)

        self.draw_hud()

    def draw_hud(self) -> None:
        state = self.window.game_state
        camera_left, camera_bottom = self.get_camera_view_origin()

        arcade.draw_text(
            self.current_level_title,
            camera_left + HUD_MARGIN,
            camera_bottom + SCREEN_HEIGHT - HUD_MARGIN - 10,
            COLOR_ACCENT,
            20,
            bold=True,
        )

        arcade.draw_text(
            f"Очки: {state.score}",
            camera_left + HUD_MARGIN,
            camera_bottom + SCREEN_HEIGHT - HUD_MARGIN - 40,
            COLOR_TEXT,
            16,
        )

        arcade.draw_text(
            f"Ядра: {state.collected_cores}",
            camera_left + HUD_MARGIN,
            camera_bottom + SCREEN_HEIGHT - HUD_MARGIN - 65,
            COLOR_TEXT,
            16,
        )

        arcade.draw_text(
            f"HP: {state.player_health}",
            camera_left + HUD_MARGIN,
            camera_bottom + SCREEN_HEIGHT - HUD_MARGIN - 90,
            COLOR_TEXT,
            16,
        )

        arcade.draw_text(
            f"Время: {state.elapsed_time:.1f}",
            camera_left + SCREEN_WIDTH - 170,
            camera_bottom + SCREEN_HEIGHT - HUD_MARGIN - 10,
            COLOR_TEXT,
            16,
        )

        arcade.draw_text(
            f"Уровень: {state.current_level_index + 1}/{self.level_manager.get_level_count()}",
            camera_left + SCREEN_WIDTH - 220,
            camera_bottom + SCREEN_HEIGHT - HUD_MARGIN - 35,
            COLOR_TEXT,
            16,
        )

        if len(self.core_list) > 0:
            arcade.draw_text(
                "Соберите все ядра, чтобы открыть выход",
                camera_left + SCREEN_WIDTH / 2,
                camera_bottom + SCREEN_HEIGHT - 35,
                COLOR_TEXT,
                16,
                anchor_x="center",
            )
        else:
            arcade.draw_text(
                "Выход открыт",
                camera_left + SCREEN_WIDTH / 2,
                camera_bottom + SCREEN_HEIGHT - 35,
                COLOR_ACCENT,
                16,
                anchor_x="center",
                bold=True,
            )

    def on_update(self, delta_time: float) -> None:
        if self.player is None:
            return

        self.window.game_state.elapsed_time += delta_time

        self.apply_input()
        self.apply_gravity()
        self.move_player_x()
        self.move_player_y()

        self.update_enemies()
        self.process_collectibles()
        self.process_enemy_collisions()
        self.process_level_exit()
        self.check_fall_out_of_world()

        self.window.game_state.player_health = self.player.health
        self.player.update_animation_state()
        self.update_camera()
        self.update_particles()

    def apply_input(self) -> None:
        if self.player is None:
            return

        if self.left_pressed and not self.right_pressed:
            self.player.move_left()
        elif self.right_pressed and not self.left_pressed:
            self.player.move_right()
        else:
            self.player.stop_horizontal()

    def apply_gravity(self) -> None:
        if self.player is None:
            return

        self.player.change_y -= GRAVITY * self.player.gravity_scale

    def move_player_x(self) -> None:
        if self.player is None:
            return

        self.player.center_x += self.player.change_x
        hit_list = arcade.check_for_collision_with_list(self.player, self.platform_list)

        for wall in hit_list:
            if self.player.change_x > 0:
                self.player.right = wall.left
            elif self.player.change_x < 0:
                self.player.left = wall.right

    def move_player_y(self) -> None:
        if self.player is None:
            return

        self.player.on_ground = False
        self.player.center_y += self.player.change_y

        hit_list = arcade.check_for_collision_with_list(self.player, self.platform_list)

        for wall in hit_list:
            if self.player.change_y > 0:
                self.player.top = wall.bottom
            elif self.player.change_y < 0:
                self.player.bottom = wall.top
                self.player.on_ground = True

            self.player.change_y = 0

    def update_enemies(self) -> None:
        for enemy in self.enemy_list:
            enemy.update_enemy()

    def process_collectibles(self) -> None:
        if self.player is None:
            return

        collected = arcade.check_for_collision_with_list(self.player, self.core_list)
        for core in collected:
            self.window.game_state.score += core.collect()
            self.window.game_state.collected_cores += 1
            self.window.audio_manager.play_pickup()

    def process_enemy_collisions(self) -> None:
        if self.player is None:
            return

        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        if hit_list:
            self.window.audio_manager.play_damage()
            self.player.take_damage(1)

            if self.player.health <= 0:
                self.respawn_player(full_reset=True)
            else:
                self.respawn_player(full_reset=False)

    def process_level_exit(self) -> None:
        if self.player is None or self.exit_sprite is None:
            return

        if len(self.core_list) > 0:
            return

        if arcade.check_for_collision(self.player, self.exit_sprite):
            self.complete_level()

    def check_fall_out_of_world(self) -> None:
        if self.player is None:
            return

        if self.player.top < WORLD_BOTTOM_DEATH_Y:
            self.respawn_player(full_reset=False)

    def respawn_player(self, full_reset: bool) -> None:
        if self.player is None:
            return

        self.window.game_state.deaths += 1
        self.player.respawn(self.spawn_x, self.spawn_y, full_heal=full_reset)
        self.window.game_state.player_health = self.player.health
        self.update_camera(snap=True)

    def complete_level(self) -> None:
        self.window.game_state.current_level_index += 1

        if self.window.game_state.current_level_index >= self.level_manager.get_level_count():
            self.finish_game(victory=True)
            return

        self.load_level(self.window.game_state.current_level_index)

    def finish_game(self, victory: bool) -> None:
        from game.views.result_view import ResultView

        self.window.game_state.is_finished = True
        self.window.game_state.is_victory = victory

        self.window.save_manager.update_after_game(
            score=self.window.game_state.score,
            elapsed_time=self.window.game_state.elapsed_time,
        )

        if victory:
            self.window.audio_manager.play_win()
        else:
            self.window.audio_manager.play_lose()

        self.window.show_view(ResultView(self.window.game_state))

    def update_camera(self, snap: bool = False) -> None:
        if self.player is None or self.camera is None:
            return

        target_x = self.player.center_x
        target_y = self.player.center_y + CAMERA_Y_OFFSET

        half_width = SCREEN_WIDTH / 2
        half_height = SCREEN_HEIGHT / 2

        min_x = self.world_left + half_width
        max_x = self.world_right - half_width

        min_y = self.world_bottom + half_height
        max_y = self.world_top - half_height

        if min_x > max_x:
            target_x = (self.world_left + self.world_right) / 2
        else:
            target_x = self.clamp(target_x, min_x, max_x)

        if min_y > max_y:
            target_y = (self.world_bottom + self.world_top) / 2
        else:
            target_y = self.clamp(target_y, min_y, max_y)

        target_position = (target_x, target_y)

        if snap:
            self.camera.position = target_position
        else:
            self.camera.position = arcade.math.lerp_2d(
                self.camera.position,
                target_position,
                CAMERA_SPEED,
            )

    def update_particles(self) -> None:
        """Заготовка под частицы."""
        pass

    def get_camera_view_origin(self) -> tuple[float, float]:
        if self.camera is None:
            return 0.0, 0.0

        return (
            self.camera.position[0] - SCREEN_WIDTH / 2,
            self.camera.position[1] - SCREEN_HEIGHT / 2,
        )

    @staticmethod
    def clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(value, maximum))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.player is None:
            return

        if symbol in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = True

        elif symbol in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = True

        elif symbol in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            self.player.jump()

        elif symbol == arcade.key.ESCAPE:
            from game.views.pause_view import PauseView

            self.window.show_view(PauseView(self))

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = False

        elif symbol in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = False