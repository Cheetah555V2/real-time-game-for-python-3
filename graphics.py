import pygame
from game_object import Player, NPC

class GraphicsEngine:
    def __init__(self) -> None:
        return None

    def render(self, player: Player, npcs: list[NPC]) -> None:
        player_position = player.get_position()
        print(f"Player is at: {player.x} {player.y}")
        for i in range(len(npcs)):
            npc_position = npcs[i].get_position()
            print(f"NPC {i+1} is at: {npc_position[0]} {npc_position[1]}")
        print()

class PygameGraphicsEngine(GraphicsEngine):
    def __init__(self):
        super().__init__()
    
    def rander(self):
        pass
    
if __name__ == "__main__":
    player1 = Player(10, 10, 1, 1)
    npcs = [NPC(20, 20), NPC(30, 30)]
    gp_engine = GraphicsEngine()

    gp_engine.render(player1, npcs)