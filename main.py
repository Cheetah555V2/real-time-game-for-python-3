from pynput import keyboard
import time
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


user_keyboard = KBPoller()

running = True

npc_x = 10
npc_y = 10
npc_x_speed = 1
npc_y_speed = 2


player_x = 10
player_y = 10

x_min = 0
x_max = 100
y_min = 0
y_max = 100


def scan_keys():
    global user_keyboard
    return user_keyboard.pressed


def render_state():
    #print("player is at:", player_x, player_y)
    print("npc is at:", npc_x, npc_y)


def update_state(inp):
    global player_x, player_y, running, npc_x, npc_y, npc_x_speed, npc_y_speed

    npc_x += npc_x_speed
    npc_y += npc_y_speed

    if "a" in inp:
        player_x -= 1
    if "d" in inp:
        player_x += 1
    if "w" in inp:
        player_y -= 1
    if "s" in inp:
        player_y += 1
    if "q" in inp:
        running = False

    if player_x < x_min:
        player_x = x_min
    if player_x > x_max:
        player_x = x_max
    if player_y < y_min:
        player_y = y_min
    if player_y > y_max:
        player_y = y_max

    if npc_x >= x_max:
        npc_x = x_max
        npc_x_speed = -1
    elif npc_x <= x_min:
        npc_x = x_min
        npc_x_speed = 1
    if npc_y >= y_max:
        npc_y = y_max
        npc_y_speed = -2
    elif npc_y <= y_min:
        npc_y = y_min
        npc_y_speed = 2
    

while running:
    # read/check for user actions (input)
    # update game state (physics, AI, etc)
    # render game state (graphics)

    render_state()
    inp = scan_keys()

    update_state(inp)

    time.sleep(1/4)
