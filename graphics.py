import pygame
from game_object import *

class GraphicsEngine:
    def __init__(self) -> None:
        return None

    def render(self, player: Player, npcs: list[NPC]) -> None:
        player_position = player.get_position()
        print(f"Player is at: {player_position[0]} {player_position[1]}")
        for i in range(len(npcs)):
            npc_position = npcs[i].get_position()
            print(f"NPC {i+1} is at: {npc_position[0]} {npc_position[1]}")
        print()

class PygameGraphicsEngine(GraphicsEngine):
    def __init__(self):
        super().__init__()
        pygame.init()
    
    def setup(self, screen_size: tuple[int, int] = (640, 640), background_color: str = "white"):
        self.screen = pygame.display.set_mode((screen_size))
        self.background_color = background_color
    
    def render(self,
               player: Player,
               npcs: list[NPC],
               bullets: list[Bullet],
               obsitacles: list[Obstacle],
               texts: list[Text],
               npc_radius: float = 10,
               bullet_radius: float = 2) -> None:
        
        
        self.screen.fill(self.background_color)
        self._draw_obstacles(obsitacles)
        self._draw_text(texts)
        self._draw_npcs(npcs)
        # Render player with i-frame blinking effect
        if player.i_frame % 2 == 0:
            self._draw_player(player, player.raidus)
        self._draw_bullets(bullets)
        
        pygame.display.flip()
    
    def render_over_screen(self, font_size: int = 40, color: str = "green"):
        font = pygame.font.SysFont(None, font_size)
        img = font.render("Thank you for playing our game", True, color)
        screen_rect = self.screen.get_rect()
        text_rect = img.get_rect(center=screen_rect.center)
        self.screen.blit(img, text_rect)
        pygame.display.flip()

    def _draw_player(self, player: Player, player_radius: float = 10):
        player_position = player.get_position()
        pygame.draw.circle(self.screen,
                           "green",
                           pygame.Vector2(player_position[0], player_position[1]),
                           player_radius)
        pygame.draw.line(self.screen,
                         "black",
                         pygame.Vector2(player_position[0],
                                        player_position[1]),
                         pygame.Vector2(player_position[0] + player_radius * player.angle.cos(),
                                        player_position[1] + player_radius * player.angle.sin())
                        )
        self._draw_health_bar(player, max_health=100)
    
    def _draw_npcs(self, npcs: list[NPC]):
        for npc in npcs:
            npc_position = npc.get_position()
            
            # Draw boss with different colors based on phase
            if isinstance(npc, BossNPC):
                boss_color = npc.get_color()
                if npc.is_changing_phase():
                    pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.2 + 0.8
                    radius = int(npc.radius * pulse)
                else:
                    radius = npc.radius
                
                pygame.draw.circle(self.screen, boss_color, 
                                 pygame.Vector2(npc_position[0], npc_position[1]), radius)
                
                font = pygame.font.SysFont(None, 24)
                phase_text = f"PHASE {npc.phase}"
                img = font.render(phase_text, True, boss_color)
                self.screen.blit(img, (npc_position[0] - 40, npc_position[1] - npc.radius - 30))
                
            else:
                pygame.draw.circle(self.screen, "purple", 
                                 pygame.Vector2(npc_position[0], npc_position[1]), npc.radius)
            
            self._draw_health_bar(npc, max_health=npc.get_max_health())
        
    def _draw_bullets(self, bullets: list[Bullet]):
        for bullet in bullets:
            bullet_position = bullet.get_position()
            
            # Get bullet color (default to old colors if not specified)
            if hasattr(bullet, 'color'):
                color = bullet.color
            else:
                color = "yellow" if bullet.is_friendly() else "red"
            
            # Draw bullet with colored circle and glow effect
            pygame.draw.circle(self.screen, color, 
                             pygame.Vector2(bullet_position[0], bullet_position[1]), 
                             bullet.radius)
            
            # Add glow effect for enemy bullets
            if not bullet.is_friendly():
                glow_color = (min(255, int(pygame.Color(color).r * 1.5)),
                            min(255, int(pygame.Color(color).g * 1.5)),
                            min(255, int(pygame.Color(color).b * 1.5)))
                pygame.draw.circle(self.screen, glow_color,
                                 pygame.Vector2(bullet_position[0], bullet_position[1]),
                                 bullet.radius * 1.5, 1)  # Outline
    
    def _draw_obstacles(self, obstacles: list):
        for obstacle in obstacles:
            obstacle_position = obstacle.get_position()
            if isinstance(obstacle, MovingObstacle):
                # Draw moving obstacles in blue
                pygame.draw.rect(self.screen,
                                 "blue",
                                 pygame.Rect(obstacle_position[0],
                                             obstacle_position[1],
                                             obstacle.width,
                                             obstacle.height)
                                )
            else:
                # Draw static obstacles in black
                pygame.draw.rect(self.screen,
                                 "black",
                                 pygame.Rect(obstacle_position[0],
                                             obstacle_position[1],
                                             obstacle.width,
                                             obstacle.height)
                                )

    def _draw_text(self, texts: list[Text]):
        for text in texts:
            font = pygame.font.SysFont(None, text.font_size)
            img = font.render(text.content, True, text.color)
            self.screen.blit(img, (text.x, text.y))

    def _draw_health_bar(self, entity, max_health: float, bar_length: float = 40, bar_height: float = 5):
        entity_position = entity.get_position()
        health_ratio = entity.get_health() / max_health
        pygame.draw.rect(self.screen,
                         "red",
                         pygame.Rect(entity_position[0] - bar_length / 2,
                                     entity_position[1] - entity.radius - 10,
                                     bar_length,
                                     bar_height)
                        )
        pygame.draw.rect(self.screen,
                         "green",
                         pygame.Rect(entity_position[0] - bar_length / 2,
                                     entity_position[1] - entity.radius - 10,
                                     bar_length * health_ratio,
                                     bar_height)
                        )

if __name__ == "__main__":
    player1 = Player(10, 10, 1, 1)
    npcs = [NPC(20, 20), NPC(30, 30)]
    gp_engine = GraphicsEngine()

    gp_engine.render(player1, npcs)