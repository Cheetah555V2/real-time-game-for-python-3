import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (320, 50)  # Start at top

# Custom Obstacle class that moves (we'll need to modify game_object.py or handle in engine)
# For now, we'll create static obstacles but position them to create moving wall effect when paired with NPCs
obstacles = [
    # Horizontal moving walls (top and bottom)
    Obstacle(0, 100, 640, 20),
    Obstacle(0, 520, 640, 20),
    
    # Vertical moving walls
    Obstacle(100, 0, 20, 640),
    Obstacle(520, 0, 20, 640),
    
    # Central static obstacles
    Obstacle(250, 250, 140, 140),
]

# Enemies that patrol between obstacles
npcs = [
    NPC(320, 150, 3, 0, is_shooting=True, bullet_cooldown=40, bullet_damage=6, max_health=90),
    NPC(320, 490, -3, 0, is_shooting=True, bullet_cooldown=40, bullet_damage=6, max_health=90),
    NPC(150, 320, 0, 3, is_shooting=True, bullet_cooldown=40, bullet_damage=6, max_health=90),
    NPC(490, 320, 0, -3, is_shooting=True, bullet_cooldown=40, bullet_damage=6, max_health=90),
]

texts = [
    Text("Level 5: Moving Walls", (10, 40), font_size=20, color="purple"),
    Text("Patrolling enemies and tight corridors", (10, 70), font_size=16, color="purple"),
    Text("Time your movements between enemy patrols", (10, 100), font_size=16, color="purple"),
    Text("Use the central block as a temporary safe zone", (10, 130), font_size=16, color="purple"),
]