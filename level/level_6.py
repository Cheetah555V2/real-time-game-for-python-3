import math
import random
from game_object import *

player_start_position = (320, 500)

# Arena with cover spots
obstacles = [
    # Cover spots
    Obstacle(100, 100, 60, 20),
    Obstacle(480, 100, 60, 20),
    Obstacle(100, 500, 60, 20),
    Obstacle(480, 500, 60, 20),
    Obstacle(280, 300, 80, 20),
]

# Create boss with high health
boss = BossNPC(320, 150, radius=25, max_health=500, 
               bullet_cooldown=15, bullet_damage=8)

# Mini-boss helpers
npcs = [
    boss,
    NPC(150, 150, 1, 1, is_shooting=True, bullet_cooldown=50, 
        bullet_damage=5, max_health=100, radius=12),
    NPC(490, 150, -1, 1, is_shooting=True, bullet_cooldown=50, 
        bullet_damage=5, max_health=100, radius=12),
]

texts = [
    Text("FINAL LEVEL: THE BOSS", (10, 40), font_size=20, color="darkred"),
    Text("Use cover strategically and watch for minions!", (10, 70), font_size=16, color="darkred")
]