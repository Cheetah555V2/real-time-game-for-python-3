class GraphicsEngine:

    def __init__(self, player: object, npcs: list[object]) -> None:
        self.player = player
        self.npcs = npcs
    
    def render_player_position(self) -> None:
        print(f"Player is at: {self.player.x_pos} {self.player.y_pos}")
    
    def render_npcs_position(self) -> None:
        for i in range(len(self.npcs)):
            print(f"NPC {i+1} is at: {self.npcs[i].x_pos} {self.npcs[i].y_pos}")
    
    def render_all_object_position(self) -> None:
        self.render_player_position()
        self.render_npcs_position()

if __name__ == "__main__":
    class Player:
        def __init__(self, x, y):
            self.x_pos = x
            self.y_pos = y
    
    class NPC(Player):
        def __init__(self, x, y):
            super().__init__(x, y)

    player1 = Player(10, 10)
    npcs = [NPC(20, 20), NPC(30, 30)]
    gp_engine = GraphicsEngine(player1, npcs)

    gp_engine.render_all_object_position()
    print()
    gp_engine.render_npcs_position()
    print()
    gp_engine.render_player_position()