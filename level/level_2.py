import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (50, 320)

# Create a solvable maze with clear paths
obstacles = [
    # Outer boundary (with entry/exit gaps)
    Obstacle(0, 0, 640, 20),           # Top wall
    Obstacle(0, 0, 20, 280),           # Left wall - top section
    Obstacle(0, 360, 20, 280),         # Left wall - bottom section
    Obstacle(620, 0, 20, 280),         # Right wall - top section  
    Obstacle(620, 360, 20, 280),       # Right wall - bottom section
    Obstacle(0, 620, 640, 20),         # Bottom wall
    
    # Inner maze structure - creates winding path
    # Horizontal corridors
    Obstacle(100, 100, 440, 20),       # Top corridor wall
    Obstacle(100, 300, 440, 20),       # Middle corridor wall
    Obstacle(100, 500, 440, 20),       # Bottom corridor wall
    
    # Vertical corridors - with gaps for passages
    # Left column
    Obstacle(100, 120, 20, 80),        # Left top vertical
    Obstacle(100, 320, 20, 80),        # Left middle vertical
    Obstacle(100, 520, 20, 80),        # Left bottom vertical
    
    # Middle columns (create gaps by splitting into segments)
    Obstacle(250, 120, 20, 80),        # Middle-left vertical top
    Obstacle(250, 320, 20, 80),        # Middle-left vertical middle
    Obstacle(250, 520, 20, 80),        # Middle-left vertical bottom
    
    Obstacle(400, 120, 20, 80),        # Middle-right vertical top
    Obstacle(400, 120, 20, 80),        # Duplicate to fix gap?
    Obstacle(400, 320, 20, 80),        # Middle-right vertical middle
    Obstacle(400, 520, 20, 80),        # Middle-right vertical bottom
    
    # Right column
    Obstacle(550, 120, 20, 80),        # Right vertical top
    Obstacle(550, 320, 20, 80),        # Right vertical middle
    Obstacle(550, 520, 20, 80),        # Right vertical bottom
    
    # Additional obstacles to make navigation interesting
    # These create zig-zag paths
    Obstacle(175, 200, 20, 100),       # Left zig
    Obstacle(325, 200, 20, 100),       # Middle-left zig
    Obstacle(475, 200, 20, 100),       # Middle-right zig
    
    Obstacle(175, 400, 20, 100),       # Left zig bottom
    Obstacle(325, 400, 20, 100),       # Middle-left zig bottom
    Obstacle(475, 400, 20, 100),       # Middle-right zig bottom
]

# Enemies placed in open areas (not inside walls)
npcs = [
    # Top area enemies
    NPC(320, 50, 1, 0, is_shooting=True, bullet_cooldown=45, bullet_damage=5, max_health=80),
    
    # Middle area enemies - placed in corridors
    NPC(180, 200, 0, 1.5, is_shooting=True, bullet_cooldown=40, bullet_damage=5, max_health=80),
    NPC(460, 200, 0, -1.5, is_shooting=True, bullet_cooldown=40, bullet_damage=5, max_health=80),
    
    # Bottom area enemies
    NPC(320, 570, -1, 0, is_shooting=True, bullet_cooldown=50, bullet_damage=5, max_health=80),
    
    # Center guardian (higher health)
    NPC(320, 320, 0, 0, is_shooting=True, bullet_cooldown=30, bullet_damage=6, max_health=120, radius=12),
]

texts = [
    Text("Level 2: The Maze", (10, 40), font_size=20, color="green"),
    Text("Navigate through the winding corridors", (10, 70), font_size=16, color="green"),
    Text("Follow the gaps between vertical walls", (10, 100), font_size=16, color="green"),
    Text("Use corners for cover against enemy fire", (10, 130), font_size=16, color="green"),
]