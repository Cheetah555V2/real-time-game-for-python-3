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
