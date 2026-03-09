import arcade

from game.config.settings import (
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_SUCCESS,
    COLOR_TEXT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game.core.game_state import GameState


class ResultView(arcade.View):
    def __init__(self, state: GameState) -> None:
        super().__init__()
        self.state = state

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self) -> None:
        self.clear()

        title = "ПОБЕДА" if self.state.is_victory else "ПОРАЖЕНИЕ"
        title_color = COLOR_SUCCESS if self.state.is_victory else (255, 100, 100)

        best_score = self.window.save_manager.data.get("best_score", 0)

        arcade.draw_text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 140,
            title_color,
            40,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"Очки: {self.state.score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 60,
            COLOR_TEXT,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Собрано ядер: {self.state.collected_cores}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 20,
            COLOR_TEXT,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Смертей: {self.state.deaths}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 20,
            COLOR_TEXT,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Время: {self.state.elapsed_time:.2f} сек",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 60,
            COLOR_TEXT,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Лучший счёт: {best_score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            COLOR_TEXT,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            "R — начать заново | M — в меню",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 180,
            COLOR_ACCENT,
            18,
            anchor_x="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.R:
            from game.views.game_view import GameView

            self.window.game_state.reset_for_new_game()
            self.window.show_view(GameView())

        elif symbol == arcade.key.M:
            from game.views.menu_view import MenuView

            self.window.show_view(MenuView())