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