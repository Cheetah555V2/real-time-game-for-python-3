import math
import random
from game_object import *

player_start_position = (320, 500)

# Open arena for bullet hell boss
obstacles = [
    # Simple border only
    Obstacle(0, 0, 640, 20),
    Obstacle(0, 0, 20, 640),
    Obstacle(620, 0, 20, 640),
    Obstacle(0, 620, 640, 20),
]

# Create bullet hell boss with enhanced patterns
boss = BossNPC(320, 150, radius=30, max_health=400, 
               bullet_cooldown=20, bullet_damage=5)

# Update boss phase attributes for bullet hell
boss.phase_attributes = {
    1: {"bullet_cooldown": 20, "bullet_damage": 5, "color": "red", 
        "pattern": "circle", "pattern_params": {"num_bullets": 24, "speed": 3}},
    2: {"bullet_cooldown": 15, "bullet_damage": 6, "color": "orange", 
        "pattern": "spread", "pattern_params": {"num_bullets": 11, "spread_angle": 120, "speed": 4}},
    3: {"bullet_cooldown": 10, "bullet_damage": 7, "color": "yellow", "is_moving": True,
        "pattern": "spiral", "pattern_params": {"num_arms": 8, "bullets_per_arm": 5, "speed": 4}},
    4: {"bullet_cooldown": 5, "bullet_damage": 8, "color": "white", "is_moving": True,
        "pattern": "aimed_spread", "pattern_params": {"num_bullets": 13, "spread_angle": 180, "speed": 6}}
}

# Add a 4th phase at 50 HP
boss.phase_health_thresholds = [300, 200, 100, 50]

npcs = [boss]

texts = [
    Text("ULTIMATE BOSS", (10, 40), font_size=24, color="gold"),
]