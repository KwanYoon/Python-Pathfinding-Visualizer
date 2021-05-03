import pygame
import math

# display
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder Visualizer")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 215, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)

# node class
SQUARE_WIDTH, SQUARE_HEIGHT = 20, 20
class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color = GRAY
        self.neighbors = []
        self.distance = COLS * ROWS
        self.past_nodes = []
        self.f, self.g, self.h = 99999999999999, 99999999999999, 99999999999999
        self.prev = None
    
    def add_neighbors(self):
        if self.x < COLS - 1 and not grid[self.x + 1][self.y].is_wall() and not grid[self.x + 1][self.y].is_closed():
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0 and not grid[self.x - 1][self.y].is_wall() and not grid[self.x - 1][self.y].is_closed():
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < ROWS - 1 and not grid[self.x][self.y + 1].is_wall() and not grid[self.x][self.y + 1].is_closed():
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0 and not grid[self.x][self.y - 1].is_wall() and not grid[self.x][self.y - 1].is_closed():
            self.neighbors.append(grid[self.x][self.y - 1])
    
    def getFGH(self, g, end):
        self.g = g
        self.h = math.sqrt((end[0] - self.x)**2 + (end[1] - self.y)**2)
        self.f = self.g + self.h
    
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
COLS = 40
ROWS = 40
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
        

# drawing the grid
def grid_draw():
    run = True
    start, end = None, None
    
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
        
    return start, end


# A* function
def a_star(speed):
    # variables
    if speed:
        FPS = speed
    else:
        FPS = 500
    clock = pygame.time.Clock()
    grid.clear()
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            grid[i].append(Node(i, j))
            
    # drawing grid
    start_end = grid_draw()
    start = start_end[0]
    end = start_end[1]

    # checking if there is start and end
    if not start or not end:
        return
    
    # starting visualization
    run = True
    curr = start
    curr_node = grid[curr[0]][curr[1]]
    curr_node.f, curr_node.g, curr_node.h = 0, 0, 0
    open_list = [curr_node]
    closed_list = []
    while run:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # searching for lowest F cost node in open_list
        smallest_node = open_list[0]
        for i in range(len(open_list)):
            if open_list[i].f < smallest_node.f:
                smallest_node = open_list[i]
        
        # change smallest node to closed_list and change current node to smallest node
        closed_list.append(smallest_node)
        open_list.remove(smallest_node)
        curr = (smallest_node.x, smallest_node.y)
        smallest_node.color = RED
        curr_node = smallest_node
        
        # drwaing grid again
        grid[start[0]][start[1]].color = ORANGE
        grid[end[0]][end[1]].color = BLUE
        draw_grid()
        pygame.display.update()
        clock.tick(FPS)
        
        # iterating through neighbors of current node
        curr_node.add_neighbors()
        for neighbor in curr_node.neighbors:
            if not neighbor in closed_list:
                if not neighbor in open_list:
                    open_list.append(neighbor)
                    neighbor.color = YELLOW
                    neighbor.getFGH(curr_node.g + 1, end)
                    neighbor.prev = curr_node
                elif neighbor.g > curr_node.g + 1:
                    neighbor.g = curr_node.g + 1
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.prev = curr_node
                    
        # algorithm finish conditions
        if len(open_list) == 0:
            break
        elif grid[end[0]][end[1]] in closed_list:
            # change all items in open_list to red
            for i in range(len(open_list)):
                open_list[i].color = RED
                
            # color path back green
            start_node = grid[start[0]][start[1]]
            curr_node = grid[end[0]][end[1]]
            while curr_node.prev != start_node:
                curr_node.prev.color = GREEN
                curr_node = curr_node.prev
                draw_grid()
                pygame.display.update()
                clock.tick(FPS)
            break
                    
        
# dijkstra function
def dijkstra(speed):
    # variables
    if speed:
        FPS = speed
    else:
        FPS = 500
    clock = pygame.time.Clock()
    grid.clear()
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            grid[i].append(Node(i, j))
    
    # drawing grid
    start_end = grid_draw()
    start = start_end[0]
    end = start_end[1]
    
    # checking if there is start and end
    if not start or not end:
        return
    
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
            break
            
        # switching node
        curr_node = smallest_node
        
        # if current node is the end node
        if curr_node.is_end():
            for node in curr_node.past_nodes:
                if not node.is_start():
                    node.color = GREEN
                draw_grid()
                pygame.display.update()
                clock.tick(FPS)
            break
        
        curr_node.color = GREEN
        curr = (curr_node.x, curr_node.y)
        
        # drawing grid
        draw_grid()
        pygame.display.update()
        clock.tick(FPS)
