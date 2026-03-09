import arcade

from game.config.settings import (
    COLOR_BACKGROUND,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    UPDATE_RATE,
)
from game.core.game_state import GameState
from game.managers.audio_manager import AudioManager
from game.managers.save_manager import SaveManager


class GameWindow(arcade.Window):
    def __init__(self) -> None:
        super().__init__(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title=SCREEN_TITLE,
            resizable=False,
            update_rate=UPDATE_RATE,
        )

        self.game_state = GameState()
        self.save_manager = SaveManager()
        self.audio_manager = AudioManager()

        arcade.set_background_color(COLOR_BACKGROUND)