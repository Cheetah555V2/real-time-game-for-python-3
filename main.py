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

class NPC:
    def __init__(self, x_pos, y_pos, x_speed= 1, y_speed= 2):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
    

user_keyboard = KBPoller()

running = True

npc1 = NPC(10, 10)
npc2 = NPC(20, 69, 3, 1)
npc3 = NPC(40, 40, 5, 3)

all_npc = [npc1, npc2, npc3]

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
    print("player is at:", player_x, player_y)
    for i in range(len(all_npc)):
        print(f"npc{i+1} is at: {all_npc[i].x_pos} {all_npc[i].y_pos}")
    print() #for readability


def update_state(inp):
    global player_x, player_y, running, all_npc

    for i in range(len(all_npc)):
        all_npc[i].x_pos += all_npc[i].x_speed
        all_npc[i].y_pos += all_npc[i].y_speed

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

    for i in range(len(all_npc)):
        if all_npc[i].x_pos >= x_max:
            all_npc[i].x_pos = x_max
            all_npc[i].x_speed = -all_npc[i].x_speed
        elif all_npc[i].x_pos <= x_min:
            all_npc[i].x_pos = x_min
            all_npc[i].x_speed = -all_npc[i].x_speed
        if all_npc[i].y_pos >= y_max:
            all_npc[i].y_pos = y_max
            all_npc[i].y_speed = -all_npc[i].y_speed
        elif all_npc[i].y_pos <= y_min:
            all_npc[i].y_pos = y_min
            all_npc[i].y_speed = -all_npc[i].y_speed
        

while running:
    # read/check for user actions (input)
    # update game state (physics, AI, etc)
    # render game state (graphics)

    render_state()
    inp = scan_keys()

    update_state(inp)

    time.sleep(1/4)
