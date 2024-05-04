import pygame
from queue import PriorityQueue
from collections import deque

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH + 300, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
    pygame.draw.line(win, GREY, (width, 0), (width, width))

def draw(win, grid, rows, width):
    win.fill(GREY)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    y, x = pos

    y = y if y < width else width - 1 or y if y >= 0 else 0
    x = x if x < width else width - 1 or x if x >= 0 else 0

    gap = width // rows

    row = y // gap
    col = x // gap

    return row, col

def draw_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def A_star(draw, grid, start, end):

    def heuristic_cost_estimate(p1, p2):
        cache = {}
        x1, y1 = p1
        x2, y2 = p2

        if (x1, y1, x2, y2) in cache:
            return cache[(x1, y1, x2, y2)]

        res = abs(x1 - x2) + abs(y1 - y2)
        cache[(x1, y1, x2, y2)] = res    
        return res



    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic_cost_estimate(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 0

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            draw_path(came_from, end, draw)
            return 1

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic_cost_estimate(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return 0

def BFS(draw, start, end):
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 0

        current = queue.popleft()

        if current == end:
            draw_path(came_from, end, draw)
            return 1

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return 0

def DFS(draw, start, end):
    stack = []
    stack.append(start)
    visited = set()
    visited.add(start)
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 0

        current = stack.pop()

        if current == end:
            draw_path(came_from, end, draw)
            return 1

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return 0


def draw_help_text(win):
    # pygame.draw.rect(win, GREY, (WIDTH, 0, 300, WIDTH))
    # pygame.display.update()
    pass


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    finished = False
    run = True
    while run:
        draw(win, grid, ROWS, width)
        draw_help_text(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]: # Quit the game
                run = False

            if finished and (event.type == pygame.KEYDOWN or any(pygame.mouse.get_pressed())):
                start = None
                end = None
                grid = make_grid(ROWS, width)
                finished = False

            if pygame.mouse.get_pressed()[0]: # Left mouse button (start, end, barrier)
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()


            elif pygame.mouse.get_pressed()[2]: # Right mouse button (clear node)
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: # Start the algorithm (A*, BFS, DFS)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    result = A_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    # result = BFS(lambda: draw(win, grid, ROWS, width), start, end)
                    # result = DFS(lambda: draw(win, grid, ROWS, width), start, end)
                    if result == -1:
                        run = False

                    finished = True

                if event.key == pygame.K_c: # Clear the all nodes
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    finished = False
        
    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)