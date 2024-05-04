import pygame
from algorithms import A_star, BFS, DFS, GBFS, Dijkstra
from maze import generate_maze
from node import Node

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH + 400, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")
pygame.font.init()
# IMG = pygame.image.load("assets/rules.jpg")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
algo_index = 0
start = None
end = None

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

def draw(win, grid, rows, width):
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

def draw_panel(win):
    win.fill(WHITE)
    header_font = pygame.font.Font("assets/Akshar-Regular.ttf", 70)
    rules_font = pygame.font.Font("assets/Akshar-Regular.ttf", 30)
    
    click_and_play = header_font.render("Click & Play!", True, (0, 0, 0))
    win.blit(click_and_play, (WIDTH + 40, 20))
   
    have_fun = header_font.render("Have Fun!", True, (0, 0, 0))
    win.blit(have_fun, (WIDTH + 77, 680))

    # Draw the rules
    rules_lines = [
        "Left-click:",
        "    Set Start (Orange) &",
        "    End (Turquoise)",
        "Drag:",
        "    Draw Obstacles (Black)",
        "A:",
        "    Switch Algorithm",
        "     ",
        "M:",
        "    Generate Random Map",
    ]

    text_surfaces = []
    text_positions = []

    for i, line in enumerate(rules_lines):
        font_color = (0, 0, 0)  # Default color

        if "Start" in line:
            font_color = (255, 165, 0)  # Orange
        elif "End" in line:
            font_color = (64, 224, 208)  # Turquoise

        text_surface = rules_font.render(line, True, font_color)
        text_positions.append((WIDTH + 30, 150 + i * 40))
        text_surfaces.append(text_surface)

    for surface, position in zip(text_surfaces, text_positions):
        win.blit(surface, position)

    # Draw the algorithm line
    algo_text_surfaces = []
    algo_text_positions = []
    algorithms = ["A*", "BFS", "DFS", "GBFS", "Dijkstra"]
    total_algo = ""

    for i, algo in enumerate(algorithms):
        font_color = (0, 0, 0)  # Default color
        if i == algo_index:
            font_color = (255, 0, 0)  # Red for selected
        algo = f"{algo}/" if i < len(algorithms) - 1 else algo
        text_surface = rules_font.render(algo, True, font_color)
        algo_text_surfaces.append(text_surface)
        text_position = (WIDTH + 53 + len(total_algo) * 13 , 430)
        total_algo += algo
        algo_text_positions.append(text_position)

    for surface, position in zip(algo_text_surfaces, algo_text_positions):
        win.blit(surface, position)

def make_maze(grid):
    global start, end
    start, end = generate_maze(grid, len(grid))

def game(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    global algo_index
    algorithms = [A_star, BFS, DFS, GBFS, Dijkstra]
    global start, end



    finished = False
    run = True
    while run:
        draw(win, grid, ROWS, width)
        draw_panel(win)

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
                    
                    result = algorithms[algo_index](lambda: draw(win, grid, ROWS, width), grid, start, end)
                    if result == -1:
                        run = False

                    finished = True

                if event.key == pygame.K_c: # Clear the all nodes
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    finished = False
                
                if event.key == pygame.K_a:
                    algo_index = (algo_index + 1) % len(algorithms)  # Wrap around the list

                if event.key == pygame.K_m:
                    grid = make_grid(ROWS, width)
                    make_maze(grid)
                    finished = False

    pygame.quit()

if __name__ == "__main__":
    game(WIN, WIDTH)