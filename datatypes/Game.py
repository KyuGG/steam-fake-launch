from dataclasses import dataclass


@dataclass
class Game:
    """dataclass of json objects from config.json"""

    game_name: str
    exe_path: str
    fake_exe_path: str
