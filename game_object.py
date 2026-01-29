from datatype import Angle
import pygame
import math
import random

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
                 bullet_damage: float = 10,
                 bullet_pattern: str = "single",  # "single", "spread", "circle", "spiral"
                 pattern_params: dict = None,  # type: ignore
                 bullet_color: str = None): # type: ignore
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
        self.bullet_pattern = bullet_pattern
        self.pattern_params = pattern_params if pattern_params else {}
        self.bullet_color = bullet_color if bullet_color else random.choice(["red", "orange"])
        
        # For spiral pattern
        self.spiral_offset = 0

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
    
    def shoot_pattern(self, target_x: float = None, target_y: float = None) -> list['Bullet']: # type: ignore
        """Shoot bullets based on pattern"""
        if self.bullet_pattern == "single":
            angle = self._get_aim_angle(target_x, target_y)
            return BulletPattern.single(self.x, self.y, angle, 5, 
                                       friendly=False, damage=self.bullet_damage,
                                       color=self.bullet_color)
        
        elif self.bullet_pattern == "spread":
            angle = self._get_aim_angle(target_x, target_y)
            num_bullets = self.pattern_params.get("num_bullets", 5)
            spread = self.pattern_params.get("spread_angle", 45)
            speed = self.pattern_params.get("speed", 4)
            return BulletPattern.spread(self.x, self.y, angle, num_bullets, spread,
                                       speed, False, self.bullet_damage, self.bullet_color)
        
        elif self.bullet_pattern == "circle":
            num_bullets = self.pattern_params.get("num_bullets", 8)
            speed = self.pattern_params.get("speed", 3)
            random_offset = self.pattern_params.get("random_offset", True)
            return BulletPattern.circle(self.x, self.y, num_bullets, speed,
                                       False, self.bullet_damage, self.bullet_color,
                                       random_offset)
        
        elif self.bullet_pattern == "spiral":
            num_arms = self.pattern_params.get("num_arms", 3)
            bullets_per_arm = self.pattern_params.get("bullets_per_arm", 3)
            speed = self.pattern_params.get("speed", 4)
            
            bullets = BulletPattern.spiral(self.x, self.y, self.spiral_offset,
                                          num_arms, bullets_per_arm, speed,
                                          False, self.bullet_damage, self.bullet_color)
            # Update spiral offset for next shot
            self.spiral_offset += 15
            if self.spiral_offset >= 360:
                self.spiral_offset = 0
            
            return bullets
        
        elif self.bullet_pattern == "aimed_spread":
            num_bullets = self.pattern_params.get("num_bullets", 7)
            spread = self.pattern_params.get("spread_angle", 30)
            speed = self.pattern_params.get("speed", 5)
            return BulletPattern.aimed_spread(self.x, self.y, target_x, target_y,
                                             num_bullets, spread, speed,
                                             False, self.bullet_damage, self.bullet_color)
        
        # Default to single shot
        angle = self._get_aim_angle(target_x, target_y)
        return BulletPattern.single(self.x, self.y, angle, 5, 
                                   friendly=False, damage=self.bullet_damage,
                                   color=self.bullet_color)
    
    def _get_aim_angle(self, target_x: float = None, target_y: float = None) -> Angle: # type: ignore
        """Get angle to aim at target or random direction"""
        if target_x is not None and target_y is not None:
            dx = target_x - self.x
            dy = target_y - self.y
            return Angle(math.degrees(math.atan2(dy, dx)))
        else:
            # Random direction for non-aimed patterns
            return Angle(random.randint(0, 360))

class BossNPC(NPC):
    def __init__(self,
                 x: float,
                 y: float,
                 vx: float = 0,
                 vy: float = 0,
                 radius: float = 25,
                 max_health: float = 300,
                 is_shooting: bool = True,
                 bullet_cooldown: int = 10,
                 bullet_damage: float = 8):
        super().__init__(x, y, vx, vy, radius, max_health, is_shooting, bullet_cooldown, bullet_damage)
        
        # Phase management
        self.phase = 1
        self.phase_health_thresholds = [300, 150]  # Health values to trigger phase changes
        self.phase_change_timer = 0
        self.phase_change_duration = 30  # Frames to transition between phases
        
        # Spawning management
        self.spawn_timer = 0
        self.spawn_interval = 120  # Spawn minions every 120 frames (2 seconds at 60 FPS)
        self.minions_spawned = 0
        self.max_minions_per_phase = 4
        
        # Phase-specific attributes
        self.phase_attributes = {
            1: {"bullet_cooldown": 15, "bullet_damage": 8, "color": "red"},
            2: {"bullet_cooldown": 10, "bullet_damage": 10, "color": "orange"},
            3: {"bullet_cooldown": 5, "bullet_damage": 12, "color": "yellow", "is_moving": True}
        }
        
        # Movement for phase 3
        self.move_timer = 0
        self.move_direction = 1
        self.move_range = 100
        
        # Current phase attributes
        self.current_color = "red"
        self.is_moving = False
        
    def update_phase(self):
        """Check if health has dropped below phase thresholds and update phase"""
        # Check phase transitions
        if self.phase == 1 and self.health <= self.phase_health_thresholds[0]:
            self.phase = 2
            self.phase_change_timer = self.phase_change_duration
            self.minions_spawned = 0
            
        elif self.phase == 2 and self.health <= self.phase_health_thresholds[1]:
            self.phase = 3
            self.phase_change_timer = self.phase_change_duration
            self.minions_spawned = 0
            
        # Update attributes based on current phase
        if self.phase in self.phase_attributes:
            attrs = self.phase_attributes[self.phase]
            self.bullet_cooldown = attrs["bullet_cooldown"]
            self.bullet_damage = attrs["bullet_damage"]
            self.current_color = attrs["color"]
            self.is_moving = attrs.get("is_moving", False)
    
    def update_movement(self):
        """Handle movement for phase 3"""
        if self.is_moving and self.phase == 3:
            self.move_timer += 1
            
            # Move in a sine wave pattern
            progress = (self.move_timer % 180) / 180.0
            
            # Update position (temporarily, actual movement handled in game engine)
            self.vx = math.sin(progress * 2 * math.pi) * 2
            self.vy = math.cos(progress * 2 * math.pi) * 1
    
    def should_spawn_minions(self) -> bool:
        """Check if boss should spawn minions"""
        self.spawn_timer += 1
        
        # During phase change, don't spawn
        if self.phase_change_timer > 0:
            return False
            
        # Check spawn interval
        if (self.spawn_timer >= self.spawn_interval and 
            self.minions_spawned < self.max_minions_per_phase):
            self.spawn_timer = 0
            self.minions_spawned += 1
            return True
            
        return False
    
    def create_minion(self) -> 'NPC':
        """Create a minion NPC based on current phase"""
        # Different minion types per phase
        if self.phase == 1:
            # Basic minions
            angle = random.random() * 2 * math.pi
            distance = 50
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            return NPC(x, y, 
                      vx=math.cos(angle) * 1.5,
                      vy=math.sin(angle) * 1.5,
                      radius=8,
                      max_health=50,
                      is_shooting=True,
                      bullet_cooldown=60,
                      bullet_damage=3)
                      
        elif self.phase == 2:
            # Faster minions
            angle = random.random() * 2 * math.pi
            distance = 40
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            return NPC(x, y,
                      vx=math.cos(angle) * 2,
                      vy=math.sin(angle) * 2,
                      radius=10,
                      max_health=75,
                      is_shooting=True,
                      bullet_cooldown=45,
                      bullet_damage=4)
                      
        else:  # Phase 3
            # Aggressive minions
            angle = random.random() * 2 * math.pi
            distance = 60
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            return NPC(x, y,
                      vx=math.cos(angle) * 2.5,
                      vy=math.sin(angle) * 2.5,
                      radius=12,
                      max_health=100,
                      is_shooting=True,
                      bullet_cooldown=30,
                      bullet_damage=5)
    
    def get_color(self) -> str:
        return self.current_color
    
    def is_changing_phase(self) -> bool:
        return self.phase_change_timer > 0
    
    def update_phase_timer(self):
        if self.phase_change_timer > 0:
            self.phase_change_timer -= 1
    
    def shoot_pattern(self, target_x: float = None, target_y: float = None) -> list['Bullet']: # type: ignore
        """Override to use phase-specific patterns"""
        if self.phase in self.phase_attributes:
            attrs = self.phase_attributes[self.phase]
            pattern = attrs.get("pattern", "single")
            params = attrs.get("pattern_params", {})
            
            if pattern == "single":
                angle = self._get_aim_angle(target_x, target_y)
                return BulletPattern.single(self.x, self.y, angle, 5, 
                                           friendly=False, damage=self.bullet_damage,
                                           color=self.current_color)
            elif pattern == "circle":
                return BulletPattern.circle(self.x, self.y, 
                                           params.get("num_bullets", 8),
                                           params.get("speed", 3),
                                           False, self.bullet_damage,
                                           self.current_color, True)
            elif pattern == "spread":
                angle = self._get_aim_angle(target_x, target_y)
                return BulletPattern.spread(self.x, self.y, angle,
                                           params.get("num_bullets", 5),
                                           params.get("spread_angle", 45),
                                           params.get("speed", 4),
                                           False, self.bullet_damage,
                                           self.current_color)
            elif pattern == "spiral":
                return BulletPattern.spiral(self.x, self.y, self.spiral_offset,
                                           params.get("num_arms", 3),
                                           params.get("bullets_per_arm", 3),
                                           params.get("speed", 4),
                                           False, self.bullet_damage,
                                           self.current_color)
            elif pattern == "aimed_spread":
                return BulletPattern.aimed_spread(self.x, self.y, target_x, target_y,
                                                 params.get("num_bullets", 7),
                                                 params.get("spread_angle", 30),
                                                 params.get("speed", 5),
                                                 False, self.bullet_damage,
                                                 self.current_color)
        
        # Default fallback
        return super().shoot_pattern(target_x, target_y)
class Player(NPC):
    def __init__(self, x, y, vx=1, vy=1, angle: float = 0, v_angle: float = 2,
                 radius: float = 10, max_health: float = 100):
        super().__init__(x, y, vx, vy)
        self.angle = Angle(angle)
        self.v_angle = v_angle

        # IMPORTANT: your code uses player.raidus in graphics; keep that name to avoid breaking.
        self.raidus = radius

        self.health = max_health
        self.max_health = max_health
        self.i_frame = 0

        # === Power-up friendly stats ===
        self.bullet_damage = 10.0
        self.base_shot_cooldown = 6  # frames (your old _reset_cooldown set 6)
        self.bullet_cooldown = 0

        # Multishot
        self.multishot_enabled = False
        self.multishot_count = 1
        self.multishot_spread_deg = 0

        # Movement (use float so small upgrades matter)
        self.vx = float(vx)
        self.vy = float(vy)

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

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

        self.update_i_frame()

    # === NEW: Engine will call this to generate bullets ===
    def shoot_bullets(self) -> list['Bullet']:
        if self.bullet_cooldown != 0:
            return []

        bullets: list[Bullet] = []

        if self.multishot_enabled and self.multishot_count >= 2:
            # spread around current aim angle
            total = self.multishot_count
            spread = float(self.multishot_spread_deg)
            if total == 2:
                offsets = [-spread/2, spread/2]
            else:
                step = spread / (total - 1)
                start = -spread / 2
                offsets = [start + i * step for i in range(total)]

            for off in offsets:
                bullets.append(Bullet(self.x, self.y, self.angle + Angle(off), 5,
                                      friendly=True, damage=self.bullet_damage, color="yellow"))
        else:
            bullets.append(Bullet(self.x, self.y, self.angle, 5,
                                  friendly=True, damage=self.bullet_damage, color="yellow"))

        self.bullet_cooldown = self.base_shot_cooldown
        return bullets

    # === PowerUp helper methods ===
    def heal(self, amount: float) -> None:
        self.health = min(self.max_health, self.health + amount)

    def increase_max_health(self, amount: float) -> None:
        self.max_health += amount
        self.health = min(self.health, self.max_health)

    def increase_move_speed(self, amount: float) -> None:
        self.vx += amount
        self.vy += amount

    def enable_multishot(self, count: int = 3, spread_deg: float = 18) -> None:
        self.multishot_enabled = True
        self.multishot_count = max(2, int(count))
        self.multishot_spread_deg = float(spread_deg)

    # unchanged methods
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

    def get_position(self):
        return super().get_position()
    
    def _reset_cooldown(self):
        self.bullet_cooldown = 6
    
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
    def __init__(self, x: float, y: float, angle: Angle, speed: float, 
                 radius: float = 3, friendly: bool = True, damage: float = 10,
                 color: str = None): # type: ignore
        self.x = x
        self.y = y
        self.x_speed = angle.cos() * speed
        self.y_speed = angle.sin() * speed
        self.radius = radius
        self.friendly = friendly
        self.damage = damage
        self.color = color if color else ("yellow" if friendly else "red")
    
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
    
    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
    def shape(self) -> str:
        return "circle"
    
    def is_friendly(self) -> bool:
        return self.friendly
    
    def get_color(self) -> str:
        return self.color

class BulletPattern:
    @staticmethod
    def single(origin_x: float, origin_y: float, angle: Angle, speed: float = 5, 
               friendly: bool = False, damage: float = 5, color: str = None): # type: ignore
        """Single bullet"""
        return [Bullet(origin_x, origin_y, angle, speed, friendly=friendly, 
                      damage=damage, color=color)]
    
    @staticmethod
    def spread(origin_x: float, origin_y: float, center_angle: Angle, 
               num_bullets: int = 5, spread_angle: float = 45, 
               speed: float = 4, friendly: bool = False, damage: float = 4,
               color: str = None): # type: ignore
        """Spread shot pattern"""
        bullets = []
        start_angle = center_angle - Angle(spread_angle / 2)
        angle_step = spread_angle / (num_bullets - 1) if num_bullets > 1 else 0
        
        for i in range(num_bullets):
            bullet_angle = start_angle + Angle(angle_step * i)
            bullets.append(Bullet(origin_x, origin_y, bullet_angle, speed, 
                                 friendly=friendly, damage=damage, color=color))
        return bullets
    
    @staticmethod
    def circle(origin_x: float, origin_y: float, num_bullets: int = 8, 
               speed: float = 3, friendly: bool = False, damage: float = 3,
               color: str = None, random_offset: bool = False): # type: ignore
        """Circle pattern"""
        bullets = []
        angle_step = 360 / num_bullets
        offset = Angle(random.randint(0, 360)) if random_offset else Angle(0)
        
        for i in range(num_bullets):
            angle = Angle(i * angle_step) + offset
            bullets.append(Bullet(origin_x, origin_y, angle, speed, 
                                 friendly=friendly, damage=damage, color=color))
        return bullets
    
    @staticmethod
    def spiral(origin_x: float, origin_y: float, angle_offset: float, 
               num_arms: int = 3, bullets_per_arm: int = 4, 
               speed: float = 4, friendly: bool = False, damage: float = 4,
               color: str = None): # type: ignore
        """Spiral pattern"""
        bullets = []
        angle_step = 360 / num_arms
        
        for arm in range(num_arms):
            base_angle = Angle(arm * angle_step + angle_offset)
            for i in range(bullets_per_arm):
                # Each bullet in the arm has a slight offset
                spread = 10  # degrees
                bullet_angle = base_angle + Angle(i * spread)
                bullets.append(Bullet(origin_x, origin_y, bullet_angle, speed * (0.8 + i * 0.1),
                                     friendly=friendly, damage=damage, color=color))
        return bullets
    
    @staticmethod
    def aimed_spread(origin_x: float, origin_y: float, target_x: float, target_y: float,
                    num_bullets: int = 7, spread_angle: float = 30,
                    speed: float = 5, friendly: bool = False, damage: float = 5,
                    color: str = None): # type: ignore
        """Aimed spread pattern towards target"""
        # Calculate angle to target
        dx = target_x - origin_x
        dy = target_y - origin_y
        center_angle = Angle(math.degrees(math.atan2(dy, dx)))
        
        return BulletPattern.spread(origin_x, origin_y, center_angle, num_bullets, 
                                   spread_angle, speed, friendly, damage, color)
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

# Add this class after the Obstacle class
class MovingObstacle:
    def __init__(self, x: float, y: float, width: float, height: float, 
                 vx: float = 0, vy: float = 0, 
                 move_range_x: float = 0, move_range_y: float = 0,
                 move_speed: float = 1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.original_x = x
        self.original_y = y
        self.move_range_x = move_range_x
        self.move_range_y = move_range_y
        self.move_speed = move_speed
        self.move_direction = 1  # 1 for forward, -1 for backward
        self.move_progress = 0  # Progress along movement path
    
    def update(self):
        # Update movement based on type
        if self.vx != 0 or self.vy != 0:
            # Simple velocity-based movement
            self.x += self.vx
            self.y += self.vy
        elif self.move_range_x > 0 or self.move_range_y > 0:
            # Sine wave movement along a range
            self.move_progress += self.move_direction * self.move_speed * 0.05
            if abs(self.move_progress) >= 1:
                self.move_direction *= -1
                self.move_progress = max(-1, min(1, self.move_progress))
            
            # Calculate position using sine wave for smooth movement
            progress_ratio = math.sin(self.move_progress * math.pi / 2)
            self.x = self.original_x + progress_ratio * self.move_range_x
            self.y = self.original_y + progress_ratio * self.move_range_y
    
    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
    def get_size(self) -> tuple[float, float]:
        return self.width, self.height
    
    def shape(self) -> str:
        return "rectangle"
    
    def bounce_if_needed(self, x_min, x_max, y_min, y_max):
        # Bounce off screen edges
        if self.x <= x_min:
            self.x = x_min
            self.vx = abs(self.vx)  # Bounce right
        elif self.x + self.width >= x_max:
            self.x = x_max - self.width
            self.vx = -abs(self.vx)  # Bounce left
        
        if self.y <= y_min:
            self.y = y_min
            self.vy = abs(self.vy)  # Bounce down
        elif self.y + self.height >= y_max:
            self.y = y_max - self.height
            self.vy = -abs(self.vy)  # Bounce up
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