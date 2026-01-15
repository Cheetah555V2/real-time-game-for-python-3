from pynput import keyboard
import time
import graphics
import game_engine
from game_object import Player, NPC
class KBPoller:
    def on_press(self, key):
        try:
            ch = key.char.lower()
            self.pressed.add(ch)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            ch = key.char.lower()
            self.pressed.remove(ch)
        except AttributeError:
            pass

    def __init__(self):
        self.pressed = set()

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=True)
        listener.start()
    
    def scan_keys(self):
        return self.pressed

user_keyboard = KBPoller()

if __name__ == "__main__":
    engine = game_engine.GameEngine(Player(10, 10),
                                    [NPC(20, 20, 1, 2), NPC(30, 30, 2, 3)],
                                    graphics.GraphicsEngine(),
                                    user_keyboard,
                                    100,
                                    100,
                                    5)
    engine.run()