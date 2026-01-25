import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (320, 320)

# Cover obstacles
obstacles = [
    Obstacle(100, 100, 50, 10),
    Obstacle(200, 200, 50, 10),
    Obstacle(300, 100, 50, 10),
    Obstacle(400, 200, 50, 10),
    Obstacle(100, 400, 50, 10),
    Obstacle(200, 500, 50, 10),
    Obstacle(300, 400, 50, 10),
    Obstacle(400, 500, 50, 10),
]

# Stationary snipers with long range shooting
npcs = [
    NPC(50, 50, 0, 0, is_shooting=True, bullet_cooldown=20, bullet_damage=8, max_health=80),
    NPC(590, 50, 0, 0, is_shooting=True, bullet_cooldown=20, bullet_damage=8, max_health=80),
    NPC(50, 590, 0, 0, is_shooting=True, bullet_cooldown=20, bullet_damage=8, max_health=80),
    NPC(590, 590, 0, 0, is_shooting=True, bullet_cooldown=20, bullet_damage=8, max_health=80),
    NPC(320, 50, 0, 0, is_shooting=True, bullet_cooldown=25, bullet_damage=10, max_health=100),
    NPC(320, 590, 0, 0, is_shooting=True, bullet_cooldown=25, bullet_damage=10, max_health=100),
]

texts = [
    Text("Level 3: Snipers' Den", (10, 40), font_size=20, color="orange"),
    Text("Stationary snipers with high damage!", (10, 70), font_size=16, color="orange"),
    Text("Use small covers to avoid their fire", (10, 100), font_size=16, color="orange"),
    Text("Take them out quickly before they overwhelm you", (10, 130), font_size=16, color="orange"),
]