import arcade

from game.config.settings import (
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class MenuView(arcade.View):
    """Стартовый экран."""

    def __init__(self) -> None:
        super().__init__()
        self.ui_camera: arcade.Camera2D | None = None

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BACKGROUND)

        if self.ui_camera is None:
            self.ui_camera = arcade.Camera2D()

        self.ui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_draw(self) -> None:
        self.clear()

        if self.ui_camera is not None:
            self.ui_camera.use()

        arcade.draw_text(
            "ChronoShift",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 120,
            COLOR_ACCENT,
            42,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "Побег из лаборатории времени",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 70,
            COLOR_TEXT,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            "ENTER — начать игру",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            "ESC — выход",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ENTER:
            from game.views.game_view import GameView

            self.window.game_state.reset_for_new_game()
            self.window.show_view(GameView())

        elif symbol == arcade.key.ESCAPE:
            self.window.close()