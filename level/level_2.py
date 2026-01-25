import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (50, 320)

# Create maze-like obstacles
obstacles = [
    # Outer walls
    Obstacle(0, 0, 640, 20),
    Obstacle(0, 0, 20, 640),
    Obstacle(620, 0, 20, 640),
    Obstacle(0, 620, 640, 20),
    
    # Inner maze walls
    Obstacle(100, 100, 20, 200),
    Obstacle(100, 100, 200, 20),
    Obstacle(280, 100, 20, 200),
    Obstacle(100, 280, 200, 20),
    
    Obstacle(400, 100, 20, 200),
    Obstacle(400, 100, 200, 20),
    Obstacle(580, 100, 20, 200),
    Obstacle(400, 280, 200, 20),
    
    Obstacle(100, 400, 20, 200),
    Obstacle(100, 400, 200, 20),
    Obstacle(280, 400, 20, 200),
    Obstacle(100, 580, 200, 20),
    
    Obstacle(400, 400, 20, 200),
    Obstacle(400, 400, 200, 20),
    Obstacle(580, 400, 20, 200),
    Obstacle(400, 580, 200, 20),
]

npcs = [
    NPC(200, 200, 2, 1, is_shooting=True, bullet_cooldown=40, bullet_damage=5),
    NPC(500, 200, -1, 2, is_shooting=True, bullet_cooldown=35, bullet_damage=5),
    NPC(200, 500, 1, -2, is_shooting=True, bullet_cooldown=45, bullet_damage=5),
    NPC(500, 500, -2, -1, is_shooting=True, bullet_cooldown=50, bullet_damage=5),
]

texts = [
    Text("Level 2: The Maze", (10, 40), font_size=20, color="green"),
    Text("Navigate through the maze while dodging enemies!", (10, 70), font_size=16, color="green"),
    Text("Use the walls as cover from enemy fire", (10, 100), font_size=16, color="green"),
]