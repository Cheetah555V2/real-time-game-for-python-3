from pynput import keyboard
import time
import graphics
import game_engine
from game_object import Player, NPC
from kbpoller import KBPoller

if __name__ == "__main__":
    engine = game_engine.PygameGameEngine(Player(10, 10, 10, 10),
                                    [NPC(20, 20, 1, 2), NPC(30, 30, 2, 3)],
                                    graphics.PygameGraphicsEngine(),
                                    "KeyBoard",
                                    640,
                                    640,
                                    fps= 5)
    engine.run()