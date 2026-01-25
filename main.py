from pynput import keyboard
import time
import graphics
import game_engine
from game_object import Player, NPC
from kbpoller import KBPoller

if __name__ == "__main__":
    screen_size = (640, 640)

    engine = game_engine.PygameGameEngine(graphics.PygameGraphicsEngine(),
                                            "KeyBoard",
                                            screen_size[0],
                                            screen_size[1],
                                            fps= 30,
                                            debug= 1)                       # debug level
    engine.run()