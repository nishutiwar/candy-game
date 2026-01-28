import pygame
import random

# Settings
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 8
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 30

# Colors
COLORS = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128)
}
COLOR_LIST = list(COLORS.values())

class CandyCrush:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Real Candy Crush Clone")
        self.clock = pygame.time.Clock()
        self.grid = [[random.choice(COLOR_LIST) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected = None

    def draw_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                # Draw Candy
                pygame.draw.rect(self.screen, self.grid[r][c], (c*TILE_SIZE+5, r*TILE_SIZE+5, TILE_SIZE-10, TILE_SIZE-10), border_radius=10)
                # Highlight Selection
                if self.selected == (r, c):
                    pygame.draw.rect(self.screen, (255, 255, 255), (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

    def swap(self, p1, p2):
        r1, c1 = p1
        r2, c2 = p2
        # Check if adjacent (baaju mein hai ya nahi)
        if abs(r1-r2) + abs(c1-c2) == 1:
            self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
            if not self.check_matches():
                # Swap back if no match
                self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]

    def check_matches(self):
        to_crush = set()
        # Horizontal check
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 2):
                if self.grid[r][c] == self.grid[r][c+1] == self.grid[r][c+2]:
                    to_crush.update([(r, c), (r, c+1), (r, c+2)])
        
        # Vertical check
        for r in range(GRID_SIZE - 2):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == self.grid[r+1][c] == self.grid[r+2][c]:
                    to_crush.update([(r, c), (r+1, c), (r+2, c)])

        if to_crush:
            for (r, c) in to_crush:
                self.grid[r][c] = random.choice(COLOR_LIST) # Replace with new
            return True
        return False

    def run(self):
        while True:
            self.screen.fill((30, 30, 30))
            self.draw_grid()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    c, r = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
                    if self.selected:
                        self.swap(self.selected, (r, c))
                        self.selected = None
                    else:
                        self.selected = (r, c)

            self.check_matches()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = CandyCrush()
    game.run()