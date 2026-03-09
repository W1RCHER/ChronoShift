import arcade

from game.config.settings import (
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class PauseView(arcade.View):
    """Экран паузы."""

    def __init__(self, game_view: arcade.View) -> None:
        super().__init__()
        self.game_view = game_view
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
            "ПАУЗА",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 80,
            COLOR_ACCENT,
            36,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "ESC — продолжить",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            "M — в меню",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)

        elif symbol == arcade.key.M:
            from game.views.menu_view import MenuView

            self.window.show_view(MenuView())