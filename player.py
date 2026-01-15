from pynput import keyboard
import time

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
            self.pressed.discard(ch)
        except AttributeError:
            pass

    def __init__(self):
        self.pressed = set()
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
            suppress=False  # <= เปลี่ยนจาก True เป็น False
        )
        self.listener.start()


running = True

player_x = 10
player_y = 10

x_min = 0
x_max = 100
y_min = 0
y_max = 100

kb = KBPoller()

def scan_keys():
    if "q" in kb.pressed:
        return "q"
    if "a" in kb.pressed:
        return "a"
    if "d" in kb.pressed:
        return "d"
    if "w" in kb.pressed:
        return "w"
    if "s" in kb.pressed:
        return "s"
    return None

def render_state():
    print("player is at:", player_x, player_y)

def update_state(inp):
    global player_x, player_y, running
    if inp == "a":
        player_x -= 1
    elif inp == "d":
        player_x += 1
    elif inp == "w":
        player_y -= 1
    elif inp == "s":
        player_y += 1
    elif inp == "q":
        running = False

    if player_x < x_min:
        player_x = x_min
    if player_x > x_max:
        player_x = x_max
    if player_y < y_min:
        player_y = y_min
    if player_y > y_max:
        player_y = y_max

while running:
    render_state()
    inp = scan_keys()
    update_state(inp)
    time.sleep(0.05)