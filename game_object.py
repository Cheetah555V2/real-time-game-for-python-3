from datatype import Angle
import pygame
import math

class NPC:
    def __init__(self,
                 x: float,
                 y: float,
                 vx: float = 1,
                 vy: float = 1,
                 radius: float = 10,
                 max_health: float = 100,
                 is_shooting: bool = False,
                 bullet_cooldown: int = 30,
                 bullet_damage: float = 10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.health = max_health
        self.max_heahth = max_health
        self.is_shooting = is_shooting
        self.bullet_cooldown = bullet_cooldown
        self.current_cooldown = 0
        self.bullet_damage = bullet_damage

    def walk(self):
        self.x += self.vx
        self.y += self.vy

    def bounce_if_needed(self, x_min, x_max, y_min, y_max):
        if self.x - self.radius <= x_min or self.x + self.radius >= x_max:
            self.vx *= -1

        if self.y - self.radius <= y_min or self.y + self.radius >= y_max:
            self.vy *= -1

    def update(self, x_min, x_max, y_min, y_max):
        self.walk()
        self.bounce_if_needed(x_min, x_max, y_min, y_max)

    def get_position(self):
        return self.x, self.y

    def shape(self) -> str:
        return "circle"
    
    def get_speed(self) -> tuple[float, float]:
        return self.vx, self.vy

    def set_speed(self, vx: float, vy: float) -> None:
        self.vx = vx
        self.vy = vy
    
    def damage(self, amount: float) -> None:
        self.health -= amount
    
    def get_health(self) -> float:
        return self.health
    
    def get_max_health(self) -> float:
        return self.max_heahth

    def get_angle(self) -> Angle:
        return Angle(math.degrees(math.atan2(self.vy, self.vx)))

    def shoot(self, angle: Angle, speed: float, friendly: bool = False) -> 'Bullet':
        bullet = Bullet(self.x, self.y, angle, speed, friendly=friendly, damage=self.bullet_damage)
        return bullet

class Player(NPC):
    def __init__(self, x, y, vx= 1, vy= 1, angle: float = 0, v_angle: float = 2, radius: float = 10, max_health: float = 100):
        super().__init__(x, y, vx, vy)
        self.angle = Angle(angle)
        self.v_angle = v_angle
        self.bullet_cooldown = 0
        self.raidus = radius
        self.health = max_health
        self.max_health = max_health
        self.i_frame = 0
    
    def walk(self, w_pressed: bool, a_pressed: bool, s_pressed: bool, d_pressed: bool):
        if w_pressed:
            self.y -= self.vy
        if a_pressed:
            self.x -= self.vx
        if s_pressed:
            self.y += self.vy
        if d_pressed:
            self.x += self.vx

    def rotate(self, q_pressed: bool, e_pressed: bool) -> None:
        if q_pressed:
            self.angle.rotate(-self.v_angle)
        if e_pressed:
            self.angle.rotate(self.v_angle)

    def update(self, key_pressed: pygame.key.ScancodeWrapper):
            
        self.walk(key_pressed[pygame.K_w],
                  key_pressed[pygame.K_a],
                  key_pressed[pygame.K_s],
                  key_pressed[pygame.K_d])
        
        self.rotate(key_pressed[pygame.K_q] or key_pressed[pygame.K_LEFT],
                    key_pressed[pygame.K_e] or key_pressed[pygame.K_RIGHT])

        if self.bullet_cooldown != 0:
            self.bullet_cooldown -= 1
        elif key_pressed[pygame.K_SPACE]:
            self._reset_cooldown()

        self.update_i_frame()   

    def get_position(self):
        return super().get_position()
    
    def _reset_cooldown(self):
        self.bullet_cooldown = 3
    
    def reduce_cooldown(self):
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
    
    def shape(self) -> str:
        return "circle"

    def damage(self, amount: float) -> None:
        self.health -= amount
    
    def get_health(self) -> float:
        return self.health
    
    def get_max_health(self) -> float:
        return self.max_health

    def set_position(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def reset_i_frame(self, duration: int) -> None:
        self.i_frame = duration
    
    def update_i_frame(self) -> None:
        if self.i_frame > 0:
            self.i_frame -= 1

class Bullet():
    def __init__(self, x: float, y: float, angle: Angle, speed: float, radius: float = 2, friendly: bool = True, damage: float = 10):
        self.x = x
        self.y = y
        self.x_speed = angle.cos() * speed
        self.y_speed = angle.sin() * speed
        self.radius = radius
        self.friendly = friendly
        self.damage = damage
    
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
    
    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
    def shape(self) -> str:
        return "circle"
    
    def is_friendly(self) -> bool:
        return self.friendly

class Obstacle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
    def get_size(self) -> tuple[float, float]:
        return self.width, self.height
    
    def shape(self) -> str:
        return "rectangle"


class Text:
    def __init__(self, content: str, position: tuple[float, float], font_size: int = 20, color: str = "black"):
        self.content = content
        self.x = position[0]
        self.y = position[1]
        self.font_size = font_size
        self.color = color
    
    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
    def get_content(self) -> str:
        return self.content
    
    def get_font_size(self) -> int:
        return self.font_size
    
    def get_color(self) -> str:
        return self.color