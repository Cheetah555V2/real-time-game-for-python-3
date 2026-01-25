import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (320, 320)

# Minimal obstacles, focus on movement
obstacles = [
    Obstacle(300, 300, 40, 40),  # Central safe zone
]

# Large swarm of weaker enemies
npcs = []
for i in range(8):  # Create a circle of enemies
    angle = (i / 8) * 2 * math.pi
    x = 320 + math.cos(angle) * 200
    y = 320 + math.sin(angle) * 200
    speed = 1.5
    vx = math.cos(angle + math.pi/2) * speed  # Tangential velocity for circular motion
    vy = math.sin(angle + math.pi/2) * speed
    npcs.append(NPC(x, y, vx, vy, is_shooting=False, max_health=50, radius=8))

# Add some shooting enemies in the mix
npcs.append(NPC(100, 100, 2, 1, is_shooting=True, bullet_cooldown=30, bullet_damage=5, max_health=70))
npcs.append(NPC(540, 100, -2, 1, is_shooting=True, bullet_cooldown=30, bullet_damage=5, max_health=70))
npcs.append(NPC(100, 540, 2, -1, is_shooting=True, bullet_cooldown=30, bullet_damage=5, max_health=70))
npcs.append(NPC(540, 540, -2, -1, is_shooting=True, bullet_cooldown=30, bullet_damage=5, max_health=70))

texts = [
    Text("Level 4: Swarm", (10, 40), font_size=20, color="red"),
    Text("Survive the swarm of enemies!", (10, 70), font_size=16, color="red"),
    Text("Most don't shoot, but there are MANY of them", (10, 100), font_size=16, color="red"),
    Text("Use the central block for temporary safety", (10, 130), font_size=16, color="red"),
]