class GraphicsEngine:
    def __init__(self) -> None:
        return None

    def render(self, player: object, npcs: list[object]) -> None:
        print(f"Player is at: {player.x} {player.y}")
        for i in range(len(npcs)):
            print(f"NPC {i+1} is at: {npcs[i].x} {npcs[i].y}")
        print()

if __name__ == "__main__":
    class Player:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    class NPC(Player):
        def __init__(self, x, y):
            super().__init__(x, y)

    player1 = Player(10, 10)
    npcs = [NPC(20, 20), NPC(30, 30)]
    gp_engine = GraphicsEngine()

    gp_engine.render(player1, npcs)