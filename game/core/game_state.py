from dataclasses import dataclass

from game.config.settings import MAX_PLAYER_HEALTH


@dataclass
class GameState:
    current_level_index: int = 0
    score: int = 0
    collected_cores: int = 0
    deaths: int = 0
    elapsed_time: float = 0.0

    player_health: int = MAX_PLAYER_HEALTH
    max_player_health: int = MAX_PLAYER_HEALTH

    shield_charges: int = 0
    shield_active: bool = False

    flight_charges: int = 0

    is_victory: bool = False
    is_finished: bool = False

    def reset_for_new_game(self) -> None:
        self.current_level_index = 0
        self.score = 0
        self.collected_cores = 0
        self.deaths = 0
        self.elapsed_time = 0.0

        self.player_health = MAX_PLAYER_HEALTH
        self.max_player_health = MAX_PLAYER_HEALTH

        self.shield_charges = 0
        self.shield_active = False
        self.flight_charges = 0

        self.is_victory = False
        self.is_finished = False