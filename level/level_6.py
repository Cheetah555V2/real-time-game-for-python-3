import math
import random
from game_object import *

player_start_position = (320, 500)

# Open arena with no obstacles
obstacles = [
    # Simple border
    Obstacle(0, 0, 640, 20),
    Obstacle(0, 0, 20, 640),
    Obstacle(620, 0, 20, 640),
    Obstacle(0, 620, 640, 20),
]

# Bullet hell enemies with different patterns
npcs = [
    # Top: Circle shooter
    NPC(320, 100, 0, 0, radius=15, max_health=120,
        is_shooting=True, bullet_cooldown=90, bullet_damage=3,
        bullet_pattern="circle", 
        pattern_params={"num_bullets": 12, "speed": 3},
        bullet_color="cyan"),
    
    # Left: Spread shooter
    NPC(100, 200, 0.5, 0, radius=12, max_health=80,
        is_shooting=True, bullet_cooldown=60, bullet_damage=4,
        bullet_pattern="spread",
        pattern_params={"num_bullets": 7, "spread_angle": 60, "speed": 4},
        bullet_color="orange"),
    
    # Right: Aimed spread
    NPC(540, 200, -0.5, 0, radius=12, max_health=80,
        is_shooting=True, bullet_cooldown=70, bullet_damage=4,
        bullet_pattern="aimed_spread",
        pattern_params={"num_bullets": 5, "spread_angle": 40, "speed": 5},
        bullet_color="magenta"),
    
    # Bottom-left: Spiral shooter
    NPC(150, 400, 0, 0.5, radius=10, max_health=60,
        is_shooting=True, bullet_cooldown=80, bullet_damage=3,
        bullet_pattern="spiral",
        pattern_params={"num_arms": 3, "bullets_per_arm": 4, "speed": 4},
        bullet_color="lime"),
    
    # Bottom-right: Spiral shooter
    NPC(490, 400, 0, -0.5, radius=10, max_health=60,
        is_shooting=True, bullet_cooldown=80, bullet_damage=3,
        bullet_pattern="spiral",
        pattern_params={"num_arms": 4, "bullets_per_arm": 3, "speed": 4},
        bullet_color="gold"),
]

texts = [
    Text("BULLET HELL: Pattern Recognition", (10, 40), font_size=24, color="lime"),
    Text("Different enemies use different bullet patterns:", (10, 70), font_size=16, color="lime"),
    Text("Cyan: Circle pattern - dodge through gaps", (10, 100), font_size=14, color="cyan"),
    Text("Orange: Spread pattern - move perpendicular", (10, 130), font_size=14, color="orange"),
    Text("Magenta: Aimed spread - unpredictable movement", (10, 160), font_size=14, color="magenta"),
    Text("Green/Yellow: Spiral patterns - find the rhythm", (10, 190), font_size=14, color="lime"),
    Text("Survive the bullet storm!", (10, 220), font_size=18, color="red"),
]