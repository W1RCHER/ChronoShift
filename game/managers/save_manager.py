import json
from pathlib import Path

from game.config.settings import SAVE_FILE


class SaveManager:
    def __init__(self, save_path: str | Path = SAVE_FILE) -> None:
        self.save_path = Path(save_path)
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        self.data = {
            "best_score": 0,
            "best_time": 0.0,
            "games_played": 0,
        }

        self.load()

    def load(self) -> dict:
        if self.save_path.exists():
            try:
                with self.save_path.open("r", encoding="utf-8") as file:
                    self.data = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.data = {
                    "best_score": 0,
                    "best_time": 0.0,
                    "games_played": 0,
                }
        return self.data

    def save(self) -> None:
        with self.save_path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def update_after_game(self, score: int, elapsed_time: float) -> None:
        self.data["games_played"] += 1

        if score > self.data.get("best_score", 0):
            self.data["best_score"] = score

        best_time = self.data.get("best_time", 0.0)
        if best_time == 0.0 or elapsed_time < best_time:
            self.data["best_time"] = round(elapsed_time, 2)

        self.save()