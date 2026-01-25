import pygame
from game_object import Player, NPC, Bullet

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
               player_radius: float = 10,
               npc_radius: float = 10,
               bullet_radius: float = 2) -> None:
        
        self.screen.fill(self.background_color)
        self._draw_npcs(npcs, npc_radius)
        self._draw_player(player, player_radius)
        self._draw_bullets(bullets, bullet_radius)
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
    
    def _draw_npcs(self, npcs: list[NPC], npc_radius: float = 10):
        for npc in npcs:
            npc_position = npc.get_position()
            pygame.draw.circle(self.screen, "purple", pygame.Vector2(npc_position[0], npc_position[1]), npc_radius)
        
    def _draw_bullets(self, bullets: list[Bullet], bullet_radius: float = 2):
        for bullet in bullets:
            bullet_position = bullet.get_position()
            pygame.draw.circle(self.screen, "red", pygame.Vector2(bullet_position[0], bullet_position[1]), bullet_radius)


if __name__ == "__main__":
    player1 = Player(10, 10, 1, 1)
    npcs = [NPC(20, 20), NPC(30, 30)]
    gp_engine = GraphicsEngine()

    gp_engine.render(player1, npcs)