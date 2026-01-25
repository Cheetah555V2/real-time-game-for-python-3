from pynput import keyboard
import time
import graphics
import game_engine
from game_object import Player, NPC
from kbpoller import KBPoller

if __name__ == "__main__":
    screen_size = (640, 640)

    engine = game_engine.PygameGameEngine(Player(screen_size[0] / 2,# Position X
                                                 screen_size[1] / 2,# Position Y
                                                 2,                 # Velocity X
                                                 2,                 # Velocity Y
                                                 0,                 # Angle
                                                 5,                 # Angular Velocity
                                                 10),               # Radius
                                    [NPC(20, 20, 1, 2), NPC(30, 30, 2, 3)],
                                    graphics.PygameGraphicsEngine(),
                                    "KeyBoard",
                                    screen_size[0],
                                    screen_size[1],
                                    fps= 10)
    engine.run()