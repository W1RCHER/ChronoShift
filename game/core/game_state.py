from dataclasses import dataclass


@dataclass
class GameState:
    current_level_index: int = 0
    score: int = 0
    collected_cores: int = 0
    deaths: int = 0
    elapsed_time: float = 0.0
    player_health: int = 3
    is_victory: bool = False
    is_finished: bool = False

    def reset_for_new_game(self) -> None:
        self.current_level_index = 0
        self.score = 0
        self.collected_cores = 0
        self.deaths = 0
        self.elapsed_time = 0.0
        self.player_health = 3
        self.is_victory = False
        self.is_finished = False