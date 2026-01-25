import math
from game_object import *

player_start_position = (320, 50)  # Start at top

# Smaller, slower moving obstacles for better performance
obstacles = [
    # Central static safe zone
    Obstacle(280, 280, 80, 80),
    
    # Small horizontal moving blocks (slow speed, small size)
    MovingObstacle(100, 150, 30, 30, vx=1.0, vy=0, move_range_x=0, move_range_y=0),
    MovingObstacle(510, 150, 30, 30, vx=-1.0, vy=0, move_range_x=0, move_range_y=0),
    
    # Small vertical moving blocks
    MovingObstacle(150, 100, 30, 30, vx=0, vy=1.0, move_range_x=0, move_range_y=0),
    MovingObstacle(490, 100, 30, 30, vx=0, vy=1.0, move_range_x=0, move_range_y=0),
    
    # Stationary obstacles for cover
    Obstacle(50, 250, 40, 40),
    Obstacle(550, 250, 40, 40),
    Obstacle(50, 400, 40, 40),
    Obstacle(550, 400, 40, 40),
    
    # Border obstacles with gaps
    Obstacle(0, 0, 640, 20),    # Top
    Obstacle(0, 620, 640, 20),  # Bottom
    Obstacle(0, 0, 20, 620),    # Left
    Obstacle(620, 0, 20, 620),  # Right
]

# Fewer, slower enemies that are easier to deal with
npcs = [
    # Patrolling enemies with slower speed
    NPC(200, 200, 1.5, 0, is_shooting=True, bullet_cooldown=50, bullet_damage=5, max_health=80),
    NPC(440, 200, -1.5, 0, is_shooting=True, bullet_cooldown=50, bullet_damage=5, max_health=80),
    
    # Stationary snipers
    NPC(100, 500, 0, 0, is_shooting=True, bullet_cooldown=40, bullet_damage=6, max_health=70),
    NPC(540, 500, 0, 0, is_shooting=True, bullet_cooldown=40, bullet_damage=6, max_health=70),
    
    # One moving enemy with vertical patrol
    NPC(320, 100, 0, 1.0, is_shooting=True, bullet_cooldown=60, bullet_damage=4, max_health=60),
]

texts = [
    Text("Level 5: Moving Obstacles", (10, 40), font_size=20, color="purple")
]