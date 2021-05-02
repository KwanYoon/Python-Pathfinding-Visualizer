import pygame

# display
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder Visualizer")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 215, 0)
BLUE = (0, 0, 255)

# node class
SQUARE_WIDTH, SQUARE_HEIGHT = 20, 20
class Node:
    def __init__(self, x, y):
        self.x,self.y = x, y
        self.color = GRAY
        self.neighbors = []
        
    def get_pos(self):
        return self.x, self.y
    
    def close(self):
        self.color = RED
        
    def remove(self):
        self.color = GRAY
        
    def make_start(self):
        self.color = ORANGE
        
    def make_end(self):
        self.color = BLUE
        
    def make_wall(self):
        self.color = BLACK
    
    def is_closed(self):
        return self.color == RED
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == BLUE
    
    def is_wall(self):
        return self.color == BLACK
    
    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x * SQUARE_WIDTH, self.y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

# grid
COLS = 30
ROWS = 30
grid = []
for i in range(ROWS):
    grid.append([])
    for j in range(COLS):
        grid[i].append(Node(i, j))


# drawing grid
def draw_grid():
    # drawing boxes
    WIN.fill(WHITE)
    for i in grid:
        for node in i:
            node.draw()
            
    # drawing lines
    for i in range(ROWS):
        pygame.draw.line(WIN, BLACK, (0, i * SQUARE_HEIGHT), (WIDTH, i * SQUARE_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(WIN, BLACK, (i * SQUARE_WIDTH, 0), (i * SQUARE_WIDTH, HEIGHT))


# get grid location based on mouse location
def grid_loc():
    loc = pygame.mouse.get_pos()
    return loc[0] // SQUARE_WIDTH, loc[1] // SQUARE_HEIGHT


# right mouse click handle
def right_mouse(which):
    loc = grid_loc()
    node = grid[loc[0]][loc[1]]
    if which == 'start':
        node.make_start()
        return loc
        
    elif which == 'end' and not node.is_start():
        node.make_end()
        return loc
        
    elif not node.is_start() and not node.is_end():
        node.make_wall()
        
    return None
    
    
# left mouse click handle
def left_mouse(start, end):
    loc = grid_loc()
    node = grid[loc[0]][loc[1]]
    if node.is_start():
        start = None
        
    elif node.is_end():
        end = None
        
    node.remove()
    return start, end
        

# main function
def main():
    run = True
    start, end = None, None
    begin_algo = False
    
    # setting up the grid
    while run:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            # left click
            if pygame.mouse.get_pressed()[0]:
                if not start:
                    start = right_mouse('start')
                
                elif not end:
                    end = right_mouse('end')
                    
                else:
                    right_mouse('wall')
                
            # right click
            if pygame.mouse.get_pressed()[2]:
                remove_return = left_mouse(start, end)
                start = remove_return[0]
                end = remove_return[1]
                
            # key presses
            if event.type == pygame.KEYDOWN:
                # space bar
                if event.key == pygame.K_SPACE:
                    run = False
        
        # drawing the grid
        draw_grid()
        pygame.display.update()
    
    
    # starting visualization
    run = True
    while run:
        break
        
    pygame.quit()

main()
