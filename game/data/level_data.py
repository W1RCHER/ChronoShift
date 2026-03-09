from dataclasses import dataclass


@dataclass(frozen=True)
class RectBlock:
    center_x: float
    center_y: float
    width: int
    height: int
    color: tuple[int, int, int]


@dataclass(frozen=True)
class EnemySpawn:
    center_x: float
    center_y: float
    patrol_left: float
    patrol_right: float
    speed: float


@dataclass(frozen=True)
class CoreSpawn:
    center_x: float
    center_y: float


@dataclass(frozen=True)
class LevelDefinition:
    title: str
    spawn_x: float
    spawn_y: float
    exit_x: float
    exit_y: float
    platforms: list[RectBlock]
    enemies: list[EnemySpawn]
    cores: list[CoreSpawn]


LEVELS: list[LevelDefinition] = [
    LevelDefinition(
        title="Уровень 1: Пробуждение",
        spawn_x=120,
        spawn_y=180,
        exit_x=1100,
        exit_y=180,
        platforms=[
            RectBlock(640, 60, 1280, 40, (120, 130, 150)),
            RectBlock(350, 180, 220, 24, (120, 130, 150)),
            RectBlock(650, 280, 220, 24, (120, 130, 150)),
            RectBlock(950, 380, 220, 24, (120, 130, 150)),
        ],
        enemies=[
            EnemySpawn(550, 110, 450, 800, 2.0),
        ],
        cores=[
            CoreSpawn(350, 230),
            CoreSpawn(650, 330),
            CoreSpawn(950, 430),
        ],
    ),
    LevelDefinition(
        title="Уровень 2: Сбой фазы",
        spawn_x=100,
        spawn_y=180,
        exit_x=1170,
        exit_y=500,
        platforms=[
            RectBlock(640, 60, 1280, 40, (120, 130, 150)),
            RectBlock(250, 180, 180, 24, (120, 130, 150)),
            RectBlock(470, 280, 180, 24, (120, 130, 150)),
            RectBlock(720, 380, 180, 24, (120, 130, 150)),
            RectBlock(970, 500, 180, 24, (120, 130, 150)),
        ],
        enemies=[
            EnemySpawn(300, 110, 180, 520, 2.5),
            EnemySpawn(900, 110, 760, 1150, 2.5),
        ],
        cores=[
            CoreSpawn(250, 230),
            CoreSpawn(470, 330),
            CoreSpawn(720, 430),
            CoreSpawn(970, 550),
        ],
    ),
    LevelDefinition(
        title="Уровень 3: Центральное ядро",
        spawn_x=100,
        spawn_y=180,
        exit_x=1180,
        exit_y=610,
        platforms=[
            RectBlock(640, 60, 1280, 40, (120, 130, 150)),
            RectBlock(280, 180, 180, 24, (120, 130, 150)),
            RectBlock(500, 300, 180, 24, (120, 130, 150)),
            RectBlock(760, 420, 180, 24, (120, 130, 150)),
            RectBlock(1030, 540, 180, 24, (120, 130, 150)),
            RectBlock(1180, 610, 120, 24, (120, 130, 150)),
        ],
        enemies=[
            EnemySpawn(350, 110, 150, 550, 3.0),
            EnemySpawn(860, 110, 650, 1120, 3.0),
        ],
        cores=[
            CoreSpawn(280, 230),
            CoreSpawn(500, 350),
            CoreSpawn(760, 470),
            CoreSpawn(1030, 590),
        ],
    ),
]