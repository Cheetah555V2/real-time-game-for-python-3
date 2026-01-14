import time


class GameEngine:
    """
    GameEngine is responsible for:
    - main game loop
    - updating game state
    - calling input and graphics subsystems
    """

    def __init__(self, player, npcs, graphics_engine, input_system,
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
            if npc.y <= 0 or npc.y >= self.height - 1:
                npc.vy *= -1
