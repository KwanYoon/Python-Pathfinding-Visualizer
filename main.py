import pygame

# display
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder Visualizer")
FPS = 120

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 215, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# node class
SQUARE_WIDTH, SQUARE_HEIGHT = 20, 20
class Node:
    def __init__(self, x, y):
        self.x,self.y = x, y
        self.color = GRAY
        self.neighbors = []
        self.distance = COLS * ROWS
        self.past_nodes = []
    
    def add_neighbors(self):
        if self.x < COLS - 1 and not grid[self.x + 1][self.y].is_wall() and not grid[self.x + 1][self.y].is_closed():
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0 and not grid[self.x - 1][self.y].is_wall() and not grid[self.x - 1][self.y].is_closed():
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < ROWS - 1 and not grid[self.x][self.y + 1].is_wall() and not grid[self.x][self.y + 1].is_closed():
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0 and not grid[self.x][self.y - 1].is_wall() and not grid[self.x][self.y - 1].is_closed():
            self.neighbors.append(grid[self.x][self.y - 1])
    
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


# left mouse click handle
def left_mouse(which):
    loc = grid_loc()
    node = grid[loc[0]][loc[1]]
    if which == 'start':
        node.color = ORANGE
        return loc
        
    elif which == 'end' and not node.is_start():
        node.color = BLUE
        return loc
        
    elif not node.is_start() and not node.is_end():
        node.color = BLACK
        
    return None
    
    
# right mouse click handle
def right_mouse(start, end):
    loc = grid_loc()
    node = grid[loc[0]][loc[1]]
    if node.is_start():
        start = None
        
    elif node.is_end():
        end = None
        
    node.color = GRAY
    return start, end
        

# main function
def main():
    run = True
    start, end = None, None
    begin_algo = False
    clock = pygame.time.Clock()
    grid.clear()
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            grid[i].append(Node(i, j))
    
    # setting up the grid
    while run:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            # left click
            if pygame.mouse.get_pressed()[0]:
                if not start:
                    start = left_mouse('start')
                
                elif not end:
                    end = left_mouse('end')
                    
                else:
                    left_mouse('wall')
                
            # right click
            if pygame.mouse.get_pressed()[2]:
                remove_return = right_mouse(start, end)
                start = remove_return[0]
                end = remove_return[1]
                
            # key presses
            if event.type == pygame.KEYDOWN:
                # space bar to start visualization
                if event.key == pygame.K_SPACE:
                    run = False
        
        # drawing the grid
        draw_grid()
        pygame.display.update()
    
    # checking if there is start and end
    if not start or not end:
        pygame.quit()
    
    # starting visualization
    run = True
    curr = start
    curr_node = grid[curr[0]][curr[1]]
    curr_node.distance = 0
    while run:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # looping through neighbors
        curr_node = grid[curr[0]][curr[1]]
        curr_node.add_neighbors()
        for neighbor in curr_node.neighbors:
            # checking if distance is less going through current node
            if curr_node.distance + 1 < neighbor.distance:
                neighbor.distance = curr_node.distance + 1
                neighbor.past_nodes += curr_node.past_nodes
                neighbor.past_nodes.append(curr_node)
        
        # changing current node to closed
        if not curr_node.is_start():
            curr_node.color = RED
        
        # finding smallest node
        smallest_dist = ROWS * COLS
        smallest_node = None
        for row in grid:
            for node in row:
                if not node.is_closed() and not node.is_start() and node.distance < smallest_dist:
                    smallest_node = node
                    smallest_dist = node.distance
                    
        # if there is no path
        if smallest_dist == ROWS * COLS:
            pygame.time.delay(4000)
            main()
            
        # switching node
        curr_node = smallest_node
        
        # if current node is the end node
        if curr_node.is_end():
            for node in curr_node.past_nodes:
                node.color = GREEN
                draw_grid()
                pygame.display.update()
                clock.tick(FPS)
                    
            pygame.time.delay(4000)
            main()
        
        curr_node.color = GREEN
        curr = (curr_node.x, curr_node.y)
        
        # drawing grid
        draw_grid()
        pygame.display.update()
        clock.tick(FPS)
        
    pygame.quit()

main()
