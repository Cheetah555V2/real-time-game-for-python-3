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
        self._draw_text(texts)
        self._draw_obstacles(obsitacles)
        self._draw_npcs(npcs)
        # Render player with i-frame blinking effect
        if player.i_frame % 2 == 0:
            self._draw_player(player, player.raidus)
        self._draw_bullets(bullets)
        
        pygame.display.flip()
    
    def render_over_screen(self, font_size: int = 50, color: str = "red"):
        font = pygame.font.SysFont(None, font_size)
        img = font.render("Game Over", True, color)
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
            pygame.draw.circle(self.screen, "purple", pygame.Vector2(npc_position[0], npc_position[1]), npc.radius)
            self._draw_health_bar(npc, max_health=npc.get_max_health())
        
    def _draw_bullets(self, bullets: list[Bullet],):
        for bullet in bullets:
            bullet_position = bullet.get_position()
            if bullet.is_friendly():
                pygame.draw.circle(self.screen, "yellow", pygame.Vector2(bullet_position[0], bullet_position[1]), bullet.radius)
            else:
                pygame.draw.circle(self.screen, "red", pygame.Vector2(bullet_position[0], bullet_position[1]), bullet.radius)
    
    def _draw_obstacles(self, obstacles: list[Obstacle]):
        for obstacle in obstacles:
            obstacle_position = obstacle.get_position()
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