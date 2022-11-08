from dataclasses import dataclass


@dataclass
class Game:
    """dataclass of json objects from config.json"""

    game_name: str
    game_id: int
    exe_path: str
    fake_exe_path: str
