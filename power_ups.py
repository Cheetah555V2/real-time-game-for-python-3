# powerups.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, List
import random

# The callable applies the powerup to your player/engine
ApplyFn = Callable[["Player", "PygameGameEngine"], None]  # type: ignore

@dataclass(frozen=True)
class PowerUp:
    id: str
    name: str
    description: str
    color: str
    apply: ApplyFn

def get_all_powerups() -> List[PowerUp]:
    # Import inside to avoid circular import at module load time
    from game_object import Player  # noqa: F401
    from game_engine import PygameGameEngine  # noqa: F401

    return [
        PowerUp(
            id="atk_up",
            name="Attack Up",
            description="+20% bullet damage",
            color="orange",
            apply=lambda p, e: setattr(p, "bullet_damage", p.bullet_damage * 1.2),
        ),
        PowerUp(
            id="as_up",
            name="Faster Shots",
            description="-1 frame cooldown (min 2)",
            color="yellow",
            apply=lambda p, e: setattr(p, "base_shot_cooldown", max(2, p.base_shot_cooldown - 1)),
        ),
        PowerUp(
            id="hp_up",
            name="Max HP Up",
            description="+20 max HP and heal 20",
            color="green",
            apply=lambda p, e: (p.increase_max_health(20), p.heal(20)),
        ),
        PowerUp(
            id="heal",
            name="Heal",
            description="Heal 30 HP",
            color="lightgreen",
            apply=lambda p, e: p.heal(30),
        ),
        PowerUp(
            id="ms_up",
            name="Move Speed",
            description="+0.5 move speed",
            color="cyan",
            apply=lambda p, e: p.increase_move_speed(0.5),
        ),
        PowerUp(
            id="multi",
            name="Multishot",
            description="Shoot +2 arrows (3 total)",
            color="violet",
            apply=lambda p, e: p.enable_multishot(count=3, spread_deg=18),
        ),
    ]

def roll_powerups(k: int = 3) -> List[PowerUp]:
    pool = get_all_powerups()
    # If you later want “no duplicates across runs”, track picked IDs in engine.
    return random.sample(pool, k=min(k, len(pool)))