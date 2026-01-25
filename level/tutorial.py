import math
from game_object import Player, NPC, Bullet, Obstacle, Text


player_start_position = (320, 320)
obstacles = [Obstacle(0, 300, 640, 10)]
npcs = [NPC(20, 360, 3, 3), NPC(300, 360, -2, -2)]

texts = [Text("Welcome to the Tutorial Level!", (10, 40), font_size=20, color="blue"),
         Text("Use W/A/S/D to move the player", (10, 70), font_size=20, color="blue"),
         Text("Use LEFT/RIGHT arrow keys to rotate the player", (10, 100), font_size=20, color="blue"),
         Text("Press SPACE to shoot bullets", (10, 130), font_size=20, color="blue"),
         Text("Shoot all the NPCs until their health are depleated to progress", (10, 160), font_size=20, color="blue"),
         Text("Good luck!", (10, 190), font_size=20, color="blue")]