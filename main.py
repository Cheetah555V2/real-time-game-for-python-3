from pynput import keyboard
import time
import graphics
import game_engine
# pip install pynput


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

class NPC:
    def __init__(self, x, y, vx= 1, vy= 2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

class Player(NPC):
    def __init__(self, x, y, vx= 1, vy= 2):
        super().__init__(x, y, vx, vy)    

user_keyboard = KBPoller()

player1 = Player(20, 20)

all_npc = [NPC(10, 10), NPC(20, 69, 3, 1), NPC(40, 40, 5, 3)]



if __name__ == "__main__":
    engine = game_engine.GameEngine(player1,
                                    all_npc,
                                    graphics.GraphicsEngine(),
                                    user_keyboard,
                                    100,
                                    100,
                                    5)
    engine.run()