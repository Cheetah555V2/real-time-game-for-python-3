import math
from game_object import Player, NPC, Bullet, Obstacle, Text

player_start_position = (320, 320)
obstacles = []
npcs = [NPC(320, 100, 0, 0, is_shooting=True, bullet_cooldown=30, bullet_damage=5)]

texts = [Text("Dodge the enemy's bullets!", (10, 40), font_size=20, color="blue"),]