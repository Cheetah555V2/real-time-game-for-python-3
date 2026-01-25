import time
import pygame
from graphics import GraphicsEngine, PygameGraphicsEngine
from game_object import Player, NPC, Bullet, Obstacle

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
    def __init__(self, player: Player, npcs: list[NPC], graphics_engine: PygameGraphicsEngine, input_system,
                 width=40, height=20, fps=10):
        super().__init__(player, npcs, graphics_engine, input_system, width, height, fps)
        graphics_engine.setup((self.width, self.height), "white")
        self.clock = pygame.time.Clock()
        self.bullets = []
    
    def run(self):
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self._check_collision_npc()
            self._handle_input()
            self._update_npc()
            self._update_bullet()
            self.graphics.render(self.player, self.npcs, self.bullets) # type: ignore
            self.clock.tick(self.fps)
            
    
    def _handle_input(self):
        # get input from user
        keys = pygame.key.get_pressed()

        # Check if player shoot
        if keys[pygame.K_SPACE] and self.player.bullet_cooldown == 0:
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.angle.cos(), self.player.angle.sin()))


        # walk user
        self.player.update(keys)
        self.player.walk(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d])
        self.player.rotate(keys[pygame.K_q], keys[pygame.K_e])

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
    
    def _check_collision_npc(self):
        for bullet in self.bullets:
            for npc in self.npcs:
                bullet_pos = bullet.get_position()
                npc_pos = npc.get_position()
                distance = ((bullet_pos[0] - npc_pos[0]) ** 2 + (bullet_pos[1] - npc_pos[1]) ** 2) ** 0.5
                if distance <= npc.radius + bullet.radius:
                    self.npcs.remove(npc)
                    self.bullets.remove(bullet)
                    break
        