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


PLATFORM_COLOR = (120, 130, 150)

LEVELS: list[LevelDefinition] = [
    LevelDefinition(
        title="Уровень 1: Пробуждение",
        spawn_x=220,
        spawn_y=180,
        exit_x=2320,
        exit_y=520,
        platforms=[
            RectBlock(1160, 60, 2640, 40, PLATFORM_COLOR),
            RectBlock(350, 180, 220, 24, PLATFORM_COLOR),
            RectBlock(640, 270, 220, 24, PLATFORM_COLOR),
            RectBlock(950, 360, 220, 24, PLATFORM_COLOR),
            RectBlock(1260, 270, 220, 24, PLATFORM_COLOR),
            RectBlock(1560, 360, 220, 24, PLATFORM_COLOR),
            RectBlock(1860, 270, 220, 24, PLATFORM_COLOR),
            RectBlock(2100, 360, 220, 24, PLATFORM_COLOR),
            RectBlock(2320, 450, 220, 24, PLATFORM_COLOR),
        ],
        enemies=[
            EnemySpawn(540, 110, 300, 820, 2.0),
            EnemySpawn(1500, 110, 1320, 1760, 2.2),
            EnemySpawn(2160, 110, 1980, 2380, 2.4),
        ],
        cores=[
            CoreSpawn(350, 230),
            CoreSpawn(640, 320),
            CoreSpawn(950, 410),
            CoreSpawn(1560, 410),
            CoreSpawn(2320, 500),
        ],
    ),
    LevelDefinition(
        title="Уровень 2: Сбой фазы",
        spawn_x=120,
        spawn_y=180,
        exit_x=2640,
        exit_y=610,
        platforms=[
            RectBlock(1400, 60, 2800, 40, PLATFORM_COLOR),
            RectBlock(330, 190, 180, 24, PLATFORM_COLOR),
            RectBlock(620, 300, 200, 24, PLATFORM_COLOR),
            RectBlock(900, 420, 200, 24, PLATFORM_COLOR),
            RectBlock(1180, 300, 200, 24, PLATFORM_COLOR),
            RectBlock(1480, 420, 220, 24, PLATFORM_COLOR),
            RectBlock(1790, 540, 220, 24, PLATFORM_COLOR),
            RectBlock(2110, 420, 220, 24, PLATFORM_COLOR),
            RectBlock(2390, 540, 220, 24, PLATFORM_COLOR),
            RectBlock(2620, 540, 180, 24, PLATFORM_COLOR),
        ],
        enemies=[
            EnemySpawn(500, 110, 220, 760, 2.3),
            EnemySpawn(1380, 110, 1080, 1600, 2.6),
            EnemySpawn(2260, 110, 1980, 2580, 2.8),
        ],
        cores=[
            CoreSpawn(330, 240),
            CoreSpawn(900, 470),
            CoreSpawn(1480, 470),
            CoreSpawn(1790, 590),
            CoreSpawn(2390, 590),
        ],
    ),
    LevelDefinition(
        title="Уровень 3: Коридор охраны",
        spawn_x=180,
        spawn_y=180,
        exit_x=2980,
        exit_y=530,
        platforms=[
            RectBlock(1600, 60, 3200, 40, PLATFORM_COLOR),
            RectBlock(360, 150, 180, 24, PLATFORM_COLOR),
            RectBlock(610, 220, 180, 24, PLATFORM_COLOR),
            RectBlock(860, 290, 200, 24, PLATFORM_COLOR),
            RectBlock(1140, 360, 220, 24, PLATFORM_COLOR),
            RectBlock(1450, 440, 220, 24, PLATFORM_COLOR),
            RectBlock(1770, 360, 220, 24, PLATFORM_COLOR),
            RectBlock(2090, 260, 220, 24, PLATFORM_COLOR),
            RectBlock(2410, 340, 220, 24, PLATFORM_COLOR),
            RectBlock(2710, 430, 220, 24, PLATFORM_COLOR),
            RectBlock(2950, 450, 220, 24, PLATFORM_COLOR),
        ],
        enemies=[
            EnemySpawn(760, 110, 500, 980, 2.4),
            EnemySpawn(1710, 110, 1500, 1950, 2.7),
            EnemySpawn(2710, 110, 2450, 3020, 3.0),
        ],
        cores=[
            CoreSpawn(360, 200),
            CoreSpawn(860, 340),
            CoreSpawn(1450, 490),
            CoreSpawn(2410, 390),
            CoreSpawn(2950, 500),
        ],
    ),
    LevelDefinition(
        title="Уровень 4: Реакторный мост",
        spawn_x=120,
        spawn_y=180,
        exit_x=3400,
        exit_y=650,
        platforms=[
            RectBlock(1800, 60, 3600, 40, PLATFORM_COLOR),
            RectBlock(360, 180, 180, 24, PLATFORM_COLOR),
            RectBlock(650, 280, 180, 24, PLATFORM_COLOR),
            RectBlock(950, 380, 180, 24, PLATFORM_COLOR),
            RectBlock(1260, 500, 200, 24, PLATFORM_COLOR),
            RectBlock(1580, 380, 200, 24, PLATFORM_COLOR),
            RectBlock(1900, 260, 200, 24, PLATFORM_COLOR),
            RectBlock(2220, 380, 200, 24, PLATFORM_COLOR),
            RectBlock(2550, 500, 220, 24, PLATFORM_COLOR),

            RectBlock(2840, 580, 220, 24, PLATFORM_COLOR),
            RectBlock(3120, 630, 220, 24, PLATFORM_COLOR),
            RectBlock(3380, 590, 220, 24, PLATFORM_COLOR),
        ],
        enemies=[
            EnemySpawn(560, 110, 260, 840, 2.5),
            EnemySpawn(1680, 110, 1420, 1960, 2.8),
            EnemySpawn(2480, 110, 2200, 2750, 3.0),
            EnemySpawn(3200, 110, 2920, 3460, 3.2),
        ],
        cores=[
            CoreSpawn(650, 330),
            CoreSpawn(1260, 550),
            CoreSpawn(1900, 310),
            CoreSpawn(2550, 550),
            CoreSpawn(3120, 680),
        ],
    ),
    LevelDefinition(
        title="Уровень 5: Центральное ядро",
        spawn_x=120,
        spawn_y=180,
        exit_x=3900,
        exit_y=710,
        platforms=[
            RectBlock(2100, 60, 4200, 40, PLATFORM_COLOR),
            RectBlock(360, 190, 200, 24, PLATFORM_COLOR),
            RectBlock(670, 310, 200, 24, PLATFORM_COLOR),
            RectBlock(980, 430, 220, 24, PLATFORM_COLOR),
            RectBlock(1320, 550, 220, 24, PLATFORM_COLOR),
            RectBlock(1680, 430, 220, 24, PLATFORM_COLOR),
            RectBlock(2040, 310, 220, 24, PLATFORM_COLOR),
            RectBlock(2400, 430, 220, 24, PLATFORM_COLOR),
            RectBlock(2760, 550, 220, 24, PLATFORM_COLOR),
            RectBlock(3120, 670, 220, 24, PLATFORM_COLOR),
            RectBlock(3480, 550, 220, 24, PLATFORM_COLOR),
            RectBlock(3880, 650, 180, 24, PLATFORM_COLOR),
        ],
        enemies=[
            EnemySpawn(520, 110, 240, 820, 2.7),
            EnemySpawn(1520, 110, 1180, 1840, 3.0),
            EnemySpawn(2500, 110, 2200, 2820, 3.2),
            EnemySpawn(3600, 110, 3320, 3960, 3.4),
        ],
        cores=[
            CoreSpawn(360, 240),
            CoreSpawn(980, 480),
            CoreSpawn(1680, 480),
            CoreSpawn(2760, 600),
            CoreSpawn(3120, 720),
            CoreSpawn(3880, 700),
        ],
    ),
]