import math
import random
from game_object import *

player_start_position = (320, 320)

# Arena with moving safe spots
obstacles = [
    # Four corner safe zones
    Obstacle(50, 50, 80, 80),
    Obstacle(510, 50, 80, 80),
    Obstacle(50, 510, 80, 80),
    Obstacle(510, 510, 80, 80),
    
    # Central rotating safe zone (conceptual)
    Obstacle(280, 280, 80, 80),
]

# Wave-based bullet hell
npcs = [
    # Wave 1: Surrounding circle shooters
    NPC(160, 160, 0, 0, radius=8, max_health=50,
        is_shooting=True, bullet_cooldown=120, bullet_damage=2,
        bullet_pattern="circle",
        pattern_params={"num_bullets": 16, "speed": 2.5, "random_offset": True},
        bullet_color="blue"),
    
    NPC(480, 160, 0, 0, radius=8, max_health=50,
        is_shooting=True, bullet_cooldown=120, bullet_damage=2,
        bullet_pattern="circle",
        pattern_params={"num_bullets": 16, "speed": 2.5, "random_offset": True},
        bullet_color="blue"),
    
    NPC(160, 480, 0, 0, radius=8, max_health=50,
        is_shooting=True, bullet_cooldown=120, bullet_damage=2,
        bullet_pattern="circle",
        pattern_params={"num_bullets": 16, "speed": 2.5, "random_offset": True},
        bullet_color="blue"),
    
    NPC(480, 480, 0, 0, radius=8, max_health=50,
        is_shooting=True, bullet_cooldown=120, bullet_damage=2,
        bullet_pattern="circle",
        pattern_params={"num_bullets": 16, "speed": 2.5, "random_offset": True},
        bullet_color="blue"),
    
    # Wave 2: Moving spiral shooters
    NPC(320, 100, 1.5, 0, radius=10, max_health=70,
        is_shooting=True, bullet_cooldown=100, bullet_damage=3,
        bullet_pattern="spiral",
        pattern_params={"num_arms": 5, "bullets_per_arm": 4, "speed": 3.5},
        bullet_color="pink"),
    
    NPC(100, 320, 0, 1.5, radius=10, max_health=70,
        is_shooting=True, bullet_cooldown=100, bullet_damage=3,
        bullet_pattern="spiral",
        pattern_params={"num_arms": 5, "bullets_per_arm": 4, "speed": 3.5},
        bullet_color="pink"),
    
    # Wave 3: Rapid fire aimed spread (boss-like)
    NPC(320, 320, 0, 0, radius=15, max_health=150,
        is_shooting=True, bullet_cooldown=40, bullet_damage=4,
        bullet_pattern="aimed_spread",
        pattern_params={"num_bullets": 9, "spread_angle": 90, "speed": 6},
        bullet_color="red"),
]

texts = [
    Text("BULLET HELL GAUNTLET", (10, 40), font_size=24, color="lime"),
]