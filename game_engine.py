import time
import pygame
import math
from level import tutorial
from graphics import GraphicsEngine, PygameGraphicsEngine
from game_object import Player, NPC, Bullet, Obstacle
from datatype import Angle


class GameEngine:
    """
    GameEngine is responsible for:
    - main game loop
    - updating game state
    - calling input and graphics subsystems
    """

    def __init__(self, player: Player, npcs: list[NPC], graphics_engine: GraphicsEngine, input_system,
                 width=40, height=20, fps=10):
        self.player = player
        self.npcs = npcs
        self.graphics = graphics_engine
        self.input = input_system

        self.width = width
        self.height = height
        self.fps = fps
        self.running = True

    def run(self):
        """Main game loop"""
        delay = 1.0 / self.fps

        while self.running:
            keys = self.input.scan_keys()
            self.update(keys)
            self.graphics.render(self.player, self.npcs)
            time.sleep(delay)

    def update(self, keys):
        """Update game state"""
        self._handle_input(keys)
        self._update_npcs()

    def _handle_input(self, keys):
        """Move player based on pressed keys"""
        if "q" in keys:
            self.running = False
            return

        if "w" in keys:
            self.player.y -= 1
        if "s" in keys:
            self.player.y += 1
        if "a" in keys:
            self.player.x -= 1
        if "d" in keys:
            self.player.x += 1

        # Keep player inside bounds
        self.player.x = max(0, min(self.width - 1, self.player.x))
        self.player.y = max(0, min(self.height - 1, self.player.y))

    def _update_npcs(self):
        """Move NPCs and make them bounce"""
        for npc in self.npcs:
            npc.x += npc.vx
            npc.y += npc.vy

            if npc.x <= 0 or npc.x >= self.width - 1:
                npc.vx *= -1
                if npc.x <= 0:
                    npc.x = 0
                else:
                    npc.x = self.width - 1
            if npc.y <= 0 or npc.y >= self.height - 1:
                npc.vy *= -1
                if npc.y <= 0:
                    npc.y = 0
                else:
                    npc.y = self.width - 1

class PygameGameEngine(GameEngine):
    def __init__(self,
                 graphics_engine: PygameGraphicsEngine,
                 input_system,
                 width=40,
                 height=20,
                 fps=10):
        # Start at tutorial level
        player = Player(tutorial.player_start_position[0],
                        tutorial.player_start_position[1],
                        3,
                        3, 
                        0,
                        4,
                        10,
                        100)
        super().__init__(player, tutorial.npcs, graphics_engine, input_system, width, height, fps)
        self.graphics = graphics_engine
        graphics_engine.setup((self.width, self.height), "white")
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.obstacles = tutorial.obstacles
        self.texts = tutorial.texts
    
    def run(self):
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False    
        
            self._check_collision()
            self._update_player(pygame.key.get_pressed())
            self._update_npc()
            self._update_bullet()
            self.graphics.render(self.player, self.npcs, self.bullets, self.obstacles, self.texts)
            self.clock.tick(self.fps)
            
    def _check_collision(self):
        self._check_collision_npc_player()
        self._check_collision_bullet_npc()
        self._check_collision_npc_npc()
        self._check_collision_bullet_obstacle()
        self._check_collision_npc_obstacle()
        self._check_collision_player_obstacle()

    def _update_player(self, keys: pygame.key.ScancodeWrapper):
        self._handle_input(keys)
        self.player.reduce_cooldown()

    def _handle_input(self, keys: pygame.key.ScancodeWrapper):
        # Check if player shoot
        if keys[pygame.K_SPACE] and self.player.bullet_cooldown == 0:
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.angle, 5))


        # walk user
        self.player.update(keys)

        # Check bound
        self.player.x = max(0, min(self.width - 1, self.player.x))
        self.player.y = max(0, min(self.height - 1, self.player.y))



    def _update_npc(self):
        for npc in self.npcs:
            npc.x += npc.vx
            npc.y += npc.vy

            if npc.x <= 0 or npc.x >= self.width - 1:
                npc.vx *= -1
                if npc.x <= 0:
                    npc.x = 0
                else:
                    npc.x = self.width - 1
            if npc.y <= 0 or npc.y >= self.height - 1:
                npc.vy *= -1
                if npc.y <= 0:
                    npc.y = 0
                else:
                    npc.y = self.width - 1
    
    def _update_bullet(self):
        remove = list()
        for i, bullet in enumerate(self.bullets):
            bullet.update()

            # Check if the bullet is out of bound, if it is then remove it
            if bullet.x < 0 or bullet.y < 0 or bullet.x > self.width or bullet.y > self.height:
                remove.append(i)
        
        for i in remove[::-1]:
            self.bullets.pop(i)
    
    def _check_collision_bullet_npc(self):
        for bullet in self.bullets:
            for npc in self.npcs:
                if self._check_collision_circle_circle(bullet.get_position(),
                                                       bullet.radius,
                                                       npc.get_position(),
                                                       npc.radius) and bullet.is_friendly():
                    npc.damage(bullet.damage)
                    if npc.get_health() <= 0:
                        self.npcs.remove(npc)
                    self.bullets.remove(bullet)
                    break
    
    def _check_collision_npc_player(self):
        for npc in self.npcs:
            if self._check_collision_circle_circle(npc.get_position(),
                                                   npc.radius,
                                                   self.player.get_position(),
                                                   self.player.radius):
                speed = npc.get_speed()
                npc_pos = npc.get_position()
                player_pos = self.player.get_position()

                speed = math.sqrt(speed[0] ** 2 + speed[1] ** 2)
                
                dx = npc_pos[0] - player_pos[0]
                dy = npc_pos[1] - player_pos[1]
                angle = Angle(math.degrees(math.atan2(dy, dx)))

                npc.set_speed(angle.cos() * speed, angle.sin() * speed)
    
    def _check_collision_npc_npc(self):
        for i in range(len(self.npcs)):
            for j in range(i + 1, len(self.npcs)):
                npc1 = self.npcs[i]
                npc2 = self.npcs[j]
                if self._check_collision_circle_circle(npc1.get_position(),
                                                        npc1.radius,
                                                        npc2.get_position(),
                                                        npc2.radius):
                    speed1 = npc1.get_speed()
                    speed2 = npc2.get_speed()

                    speed1_magnitude = math.sqrt(speed1[0] ** 2 + speed1[1] ** 2)
                    speed2_magnitude = math.sqrt(speed2[0] ** 2 + speed2[1] ** 2)

                    pos1 = npc1.get_position()
                    pos2 = npc2.get_position()

                    dx = pos1[0] - pos2[0]
                    dy = pos1[1] - pos2[1]
                    angle = Angle(math.degrees(math.atan2(dy, dx)))

                    npc1.set_speed(angle.cos() * speed2_magnitude, angle.sin() * speed2_magnitude)
                    npc2.set_speed(-angle.cos() * speed1_magnitude, -angle.sin() * speed1_magnitude)

    def _check_collision_bullet_obstacle(self):
        for bullet in self.bullets:
            for obstacle in self.obstacles:
                if self._check_collision_circle_rectangle(bullet.get_position(),
                                                          bullet.radius,
                                                          obstacle.get_position(),
                                                          obstacle.get_size()):
                    self.bullets.remove(bullet)
                    break
    
    def _check_collision_npc_obstacle(self):
        for npc in self.npcs:
            for obstacle in self.obstacles:
                if self._check_collision_circle_rectangle(npc.get_position(),
                                                          npc.radius,
                                                          obstacle.get_position(),
                                                          obstacle.get_size()):
                    speed = npc.get_speed()
                    speed_magnitude = math.sqrt(speed[0] ** 2 + speed[1] ** 2)

                    npc_pos = npc.get_position()
                    obs_pos = obstacle.get_position()
                    obs_size = obstacle.get_size()

                    # Determine the closest point on the rectangle to the circle center
                    closest_x = max(obs_pos[0], min(npc_pos[0], obs_pos[0] + obs_size[0]))
                    closest_y = max(obs_pos[1], min(npc_pos[1], obs_pos[1] + obs_size[1]))

                    dx = npc_pos[0] - closest_x
                    dy = npc_pos[1] - closest_y
                    angle = Angle(math.degrees(math.atan2(dy, dx)))

                    npc.set_speed(angle.cos() * speed_magnitude, angle.sin() * speed_magnitude)

    def _check_collision_player_obstacle(self):
        for obstacle in self.obstacles:
            if self._check_collision_circle_rectangle(self.player.get_position(),
                                                      self.player.radius,
                                                      obstacle.get_position(),
                                                      obstacle.get_size()):
                player_pos = self.player.get_position()
                obs_pos = obstacle.get_position()
                obs_size = obstacle.get_size()

                # Determine the closest point on the rectangle to the circle center
                closest_x = max(obs_pos[0], min(player_pos[0], obs_pos[0] + obs_size[0]))
                closest_y = max(obs_pos[1], min(player_pos[1], obs_pos[1] + obs_size[1]))

                dx = player_pos[0] - closest_x
                dy = player_pos[1] - closest_y
                angle = Angle(math.degrees(math.atan2(dy, dx)))

                self.player.set_position(closest_x + angle.cos() * (self.player.radius + 1),
                                         closest_y + angle.sin() * (self.player.radius + 1))

    def _check_collision_circle_circle(self,
                                     obj1_pos: tuple[float, float],
                                     obj1_radius: float,
                                     obj2_pos: tuple[float, float],
                                     obj2_radius: float) -> bool:
        distance = ((obj1_pos[0] - obj2_pos[0]) ** 2 + (obj1_pos[1] - obj2_pos[1]) ** 2) ** 0.5
        if distance <= obj1_radius + obj2_radius:
            return True
        return False

    def _check_collision_circle_rectangle(self,
                                        circle_pos: tuple[float, float],
                                        circle_radius: float,
                                        rect_pos: tuple[float, float],
                                        rect_size: tuple[float, float]) -> bool:
        circle_distance_x = abs(circle_pos[0] - (rect_pos[0] + rect_size[0] / 2))
        circle_distance_y = abs(circle_pos[1] - (rect_pos[1] + rect_size[1] / 2))

        if circle_distance_x > (rect_size[0] / 2 + circle_radius):
            return False
        if circle_distance_y > (rect_size[1] / 2 + circle_radius):
            return False

        if circle_distance_x <= (rect_size[0] / 2):
            return True
        if circle_distance_y <= (rect_size[1] / 2):
            return True

        corner_distance_sq = (circle_distance_x - rect_size[0] / 2) ** 2 + (circle_distance_y - rect_size[1] / 2) ** 2

        return corner_distance_sq <= (circle_radius ** 2)