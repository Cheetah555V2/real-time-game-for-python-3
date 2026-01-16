class NPC:
    def __init__(self, x: int, y: int, vx: int = 1, vy: int = 1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def walk(self):
        self.x += self.vx
        self.y += self.vy

    def bounce_if_needed(self, x_min, x_max, y_min, y_max):
        if self.x <= x_min or self.x >= x_max:
            self.vx *= -1

        if self.y <= y_min or self.y >= y_max:
            self.vy *= -1

    def update(self, x_min, x_max, y_min, y_max):
        self.walk()
        self.bounce_if_needed(x_min, x_max, y_min, y_max)

    def get_position(self):
        return self.x, self.y

class Player(NPC):
    def __init__(self, x, y, vx= 1, vy= 1):
        super().__init__(x, y, vx, vy)
    
    def walk(self, w_pressed: bool, a_pressed: bool, s_pressed: bool, d_pressed: bool):
        if w_pressed:
            self.y -= self.vy
        if a_pressed:
            self.x -= self.vx
        if s_pressed:
            self.y += self.vy
        if d_pressed:
            self.x += self.vx
    
    def update(self, key_pressed: set[str]):
        key_pressed_lower = set()
        for i in key_pressed:
            key_pressed_lower.add(i.lower())
        self.walk('w' in key_pressed_lower,
                  'a' in key_pressed_lower,
                  's' in key_pressed_lower,
                  'd' in key_pressed_lower)
    
    def get_position(self):
        return super().get_position()