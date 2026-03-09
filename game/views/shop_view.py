import arcade

from game.config.settings import (
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_SUCCESS,
    COLOR_TEXT,
    FLIGHT_COST,
    HEALTH_RESTORE_COST,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_COST,
)
from game.views.game_view import GameView
from game.views.menu_view import MenuView


class ShopView(arcade.View):
    """Межуровневый магазин улучшений."""

    def __init__(self) -> None:
        super().__init__()
        self.ui_camera: arcade.Camera2D | None = None
        self.message = "Выберите улучшение или нажмите ENTER для продолжения."

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BACKGROUND)

        if self.ui_camera is None:
            self.ui_camera = arcade.Camera2D()

        self.ui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_draw(self) -> None:
        self.clear()

        if self.ui_camera is not None:
            self.ui_camera.use()

        state = self.window.game_state

        arcade.draw_text(
            "МАГАЗИН УЛУЧШЕНИЙ",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 130,
            COLOR_ACCENT,
            34,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"Следующий уровень: {state.current_level_index + 1}/5",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 180,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Очки: {state.score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 220,
            COLOR_SUCCESS,
            22,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"HP: {state.player_health}/{state.max_player_health}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 255,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Щиты: {state.shield_charges} | Активен: {'Да' if state.shield_active else 'Нет'}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 285,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Полеты: {state.flight_charges}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 315,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            f"H — Восстановление здоровья (+1 HP) — {HEALTH_RESTORE_COST} очков",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 390,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            f"S — Щит (1 защита, активация Ctrl) — {SHIELD_COST} очков",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 430,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            f"F — Полет (1 заряд на 2 сек, Shift + Up) — {FLIGHT_COST} очков",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 470,
            COLOR_TEXT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            "ENTER — продолжить | M — в меню",
            SCREEN_WIDTH / 2,
            150,
            COLOR_ACCENT,
            18,
            anchor_x="center",
        )

        arcade.draw_text(
            self.message,
            SCREEN_WIDTH / 2,
            100,
            COLOR_SUCCESS if "успешно" in self.message.lower() else COLOR_TEXT,
            16,
            anchor_x="center",
        )

    def buy_health(self) -> None:
        state = self.window.game_state

        if state.player_health >= state.max_player_health:
            self.message = "Здоровье уже максимальное."
            return

        if state.score < HEALTH_RESTORE_COST:
            self.message = "Недостаточно очков для восстановления здоровья."
            return

        state.score -= HEALTH_RESTORE_COST
        state.player_health += 1
        self.message = "Восстановление здоровья успешно куплено."

    def buy_shield(self) -> None:
        state = self.window.game_state

        if state.score < SHIELD_COST:
            self.message = "Недостаточно очков для покупки щита."
            return

        state.score -= SHIELD_COST
        state.shield_charges += 1
        self.message = "Щит успешно куплен."

    def buy_flight(self) -> None:
        state = self.window.game_state

        if state.score < FLIGHT_COST:
            self.message = "Недостаточно очков для покупки полета."
            return

        state.score -= FLIGHT_COST
        state.flight_charges += 1
        self.message = "Полет успешно куплен."

    def continue_game(self) -> None:
        self.window.show_view(GameView())

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.H:
            self.buy_health()

        elif symbol == arcade.key.S:
            self.buy_shield()

        elif symbol == arcade.key.F:
            self.buy_flight()

        elif symbol == arcade.key.ENTER:
            self.continue_game()

        elif symbol == arcade.key.M:
            self.window.show_view(MenuView())