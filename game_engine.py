import time
import pygame
import math
from graphics import GraphicsEngine, PygameGraphicsEngine
from game_object import *
from datatype import Angle

from level import level_6, level_7, level_8, tutorial, level_1, level_2, level_3, level_4, level_5

level_order = [tutorial, level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8]
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
                 fps=10,
                 *args,
                 debug: int = 0,
                 **kwargs,
                 ):
        # Start at tutorial level
        player = Player(level_order[debug].player_start_position[0],
                        level_order[debug].player_start_position[1],
                        3,
                        0,
                        4,
                        10,
                        100)
        super().__init__(player, level_order[debug].npcs, graphics_engine, input_system, width, height, fps)
        self.graphics = graphics_engine
        graphics_engine.setup((self.width, self.height), "white")
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.obstacles = level_order[debug].obstacles
        self.texts = level_order[debug].texts
        self.current_level = debug
        self.is_game_over = False

    def load_level(self, level_index: int):
        level = level_order[level_index]
        self.player.x = level.player_start_position[0]
        self.player.y = level.player_start_position[1]
        self.npcs = level.npcs
        self.obstacles = level.obstacles
        self.texts = level.texts
        self.bullets = []
        self.player.health = self.player.get_max_health()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False    
            
            # Only update game state if game is not over
            if not self.is_game_over:
                self._check_collision()
                self._update_player(pygame.key.get_pressed())
                self._update_npc()
                self._update_bullet()
                self._update_obstacles()
                self.graphics.render(self.player, self.npcs, self.bullets, self.obstacles, self.texts)
                
                # Wait 3 seconds if all npcs are destroyed then go to the next level
                if self.npcs == []:
                    for _ in range(self.fps * 3):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.running = False    
                        self.graphics.render(self.player, self.npcs, self.bullets, self.obstacles, self.texts)
                        self.clock.tick(self.fps)
                    self.current_level += 1
                    if self.current_level >= len(level_order):
                        self.running = False
                    else:
                        self.load_level(self.current_level)
            else:
                # Show game over screen for 3 seconds then exit
                self.graphics.render_over_screen()
                pygame.display.flip()
                
                # Wait for 3 seconds
                start_time = time.time()
                while time.time() - start_time < 3:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            return
                    # Keep updating the display during the wait
                    self.graphics.render_over_screen()
                    pygame.display.flip()
                    self.clock.tick(self.fps)
                
                # After 3 seconds, exit the game
                self.running = False
            
            self.clock.tick(self.fps)
        
        # Clean up pygame after game loop ends
        pygame.quit()
 
            
    def _check_collision(self):
        self._check_collision_npc_player()
        self._check_collision_bullet_player()
        self._check_collision_bullet_npc()
        self._check_collision_npc_npc()
        self._check_collision_bullet_obstacle()
        self._check_collision_npc_obstacle()
        self._check_collision_player_obstacle()

    def _update_player(self, keys: pygame.key.ScancodeWrapper):
        self._handle_input(keys)
        self.player.reduce_cooldown()
        self.player.update_i_frame()

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
            # Store old position
            old_x, old_y = npc.x, npc.y
            
            # Calculate new position
            new_x = npc.x + npc.vx
            new_y = npc.y + npc.vy
            
            # Check collision with obstacles at new position
            can_move_x, can_move_y = True, True
            temp_x, temp_y = npc.x, npc.y
            
            # Test X movement
            npc.x = new_x
            for obstacle in self.obstacles:
                if self._check_collision_circle_rectangle((npc.x, npc.y),
                                                          npc.radius,
                                                          obstacle.get_position(),
                                                          obstacle.get_size()):
                    can_move_x = False
                    npc.vx *= -0.8  # Bounce with energy loss
                    break
            npc.x = old_x
            
            # Test Y movement  
            npc.y = new_y
            for obstacle in self.obstacles:
                if self._check_collision_circle_rectangle((npc.x, npc.y),
                                                          npc.radius,
                                                          obstacle.get_position(),
                                                          obstacle.get_size()):
                    can_move_y = False
                    npc.vy *= -0.8  # Bounce with energy loss
                    break
            npc.y = old_y
            
            # Only move if no collision
            if can_move_x:
                npc.x = new_x
            if can_move_y:
                npc.y = new_y
            
            # Original boundary checks (keep these)
            if npc.x - npc.radius <= 0 or npc.x + npc.radius >= self.width:
                npc.vx *= -1
                if npc.x - npc.radius <= 0:
                    npc.x = npc.radius
                else:
                    npc.x = self.width - npc.radius
            if npc.y - npc.radius <= 0 or npc.y + npc.radius >= self.height:
                npc.vy *= -1
                if npc.y - npc.radius <= 0:
                    npc.y = npc.radius
                else:
                    npc.y = self.height - npc.radius
            
            # Check if npc shoot with patterns
            if npc.is_shooting and npc.current_cooldown == 0:
                if hasattr(npc, 'shoot_pattern'):
                    # Use pattern shooting
                    bullets = npc.shoot_pattern(self.player.x, self.player.y)
                    self.bullets.extend(bullets)
                else:
                    # Fallback to old shooting
                    shooting_angle = Angle(math.degrees(math.atan2(self.player.y - npc.y, self.player.x - npc.x)))
                    self.bullets.append(npc.shoot(shooting_angle, 5, friendly=False))
                
                npc.current_cooldown = npc.bullet_cooldown
                
            if npc.current_cooldown > 0:
                npc.current_cooldown -= 1
        
        # Call boss update if needed
        self._update_boss()
            
    def _update_obstacles(self):
        """Update moving obstacles positions"""
        for obstacle in self.obstacles:
            if isinstance(obstacle, MovingObstacle):
                obstacle.update()
                # Bounce off screen edges
                obstacle.bounce_if_needed(0, self.width, 0, self.height)

    def _update_bullet(self):
        remove = list()
        for i, bullet in enumerate(self.bullets):
            bullet.update()

            # Check if the bullet is out of bound, if it is then remove it
            if bullet.x < 0 or bullet.y < 0 or bullet.x > self.width or bullet.y > self.height:
                remove.append(i)
        
        for i in remove[::-1]:
            self.bullets.pop(i)
    
    def _update_boss(self):
        """Update boss behavior and handle minion spawning"""
        for npc in self.npcs:
            if isinstance(npc, BossNPC):
                # Update boss phase and movement
                npc.update_phase()
                npc.update_movement()
                npc.update_phase_timer()
                
                # Check if boss should spawn minions
                if npc.should_spawn_minions():
                    minion = npc.create_minion()
                    self.npcs.append(minion)

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
    
    def _check_collision_bullet_player(self):
        for bullet in self.bullets:
            if self._check_collision_circle_circle(bullet.get_position(),
                                                   bullet.radius,
                                                   self.player.get_position(),
                                                   self.player.radius) and not bullet.is_friendly():
                if self.player.i_frame == 0:
                    self.player.damage(bullet.damage)
                    self.player.reset_i_frame(15) # 15 frames of invincibility
                self.bullets.remove(bullet)

                if self.player.get_health() <= 0:
                    self.is_game_over = True
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
                    # Get obstacle boundaries
                    obs_pos = obstacle.get_position()
                    obs_size = obstacle.get_size()
                    obs_left = obs_pos[0]
                    obs_right = obs_pos[0] + obs_size[0]
                    obs_top = obs_pos[1]
                    obs_bottom = obs_pos[1] + obs_size[1]
                    
                    # Calculate NPC's position relative to obstacle
                    npc_x, npc_y = npc.get_position()
                    
                    # Find the closest point on the obstacle to the NPC
                    closest_x = max(obs_left, min(npc_x, obs_right))
                    closest_y = max(obs_top, min(npc_y, obs_bottom))
                    
                    # Calculate penetration depth
                    dx = npc_x - closest_x
                    dy = npc_y - closest_y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < npc.radius and distance > 0:
                        # Normalize the direction vector
                        nx = dx / distance
                        ny = dy / distance
                        
                        # Push NPC out of the obstacle
                        overlap = npc.radius - distance
                        npc.x += nx * overlap * 1.1  # Slightly more to prevent sticking
                        npc.y += ny * overlap * 1.1
                        
                        # Reflect velocity (bounce)
                        dot_product = npc.vx * nx + npc.vy * ny
                        npc.vx = npc.vx - 2 * dot_product * nx
                        npc.vy = npc.vy - 2 * dot_product * ny
                        
                        # Reduce speed slightly to prevent clipping
                        speed_reduction = 0.9
                        npc.vx *= speed_reduction
                        npc.vy *= speed_reduction
                    
                    elif distance == 0:
                        # NPC is exactly at the corner, push out diagonally
                        npc.x += npc.radius
                        npc.y += npc.radius
                        npc.vx *= -1
                        npc.vy *= -1

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
        circle_x, circle_y = circle_pos
        rect_x, rect_y = rect_pos
        rect_width, rect_height = rect_size
        
        # Find the closest point on the rectangle to the circle
        closest_x = max(rect_x, min(circle_x, rect_x + rect_width))
        closest_y = max(rect_y, min(circle_y, rect_y + rect_height))
        
        # Calculate distance between circle center and closest point
        distance_x = circle_x - closest_x
        distance_y = circle_y - closest_y
        
        # Check if distance is less than circle radius
        distance_squared = distance_x * distance_x + distance_y * distance_y
        return distance_squared < (circle_radius * circle_radius)