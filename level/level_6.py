import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (320, 500)

# Arena with cover spots
obstacles = [
    # Arena boundary
    Obstacle(0, 0, 640, 20),
    Obstacle(0, 0, 20, 640),
    Obstacle(620, 0, 20, 640),
    Obstacle(0, 620, 640, 20),
    
    # Cover spots
    Obstacle(100, 100, 60, 20),
    Obstacle(480, 100, 60, 20),
    Obstacle(100, 500, 60, 20),
    Obstacle(480, 500, 60, 20),
    Obstacle(280, 300, 80, 20),
]

# Boss enemy with high health and fast shooting
npcs = [
    NPC(320, 150, 0, 0, radius=25, is_shooting=True, bullet_cooldown=10, bullet_damage=8, max_health=300),
]

# Mini-boss helpers
npcs.append(NPC(150, 150, 1, 1, is_shooting=True, bullet_cooldown=50, bullet_damage=5, max_health=100))
npcs.append(NPC(490, 150, -1, 1, is_shooting=True, bullet_cooldown=50, bullet_damage=5, max_health=100))

texts = [
    Text("FINAL LEVEL: THE BOSS", (10, 40), font_size=20, color="darkred"),
    Text("Destroy the boss with 300 health!", (10, 70), font_size=16, color="darkred"),
    Text("He shoots rapidly - use cover strategically", (10, 100), font_size=16, color="darkred"),
    Text("Take out his helpers first if needed", (10, 130), font_size=16, color="darkred"),
    Text("Good luck, you'll need it!", (10, 160), font_size=16, color="darkred"),
]