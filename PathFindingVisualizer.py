import pygame
from algorithms import A_star, BFS, DFS, GBFS, Dijkstra
from maze import generate_maze
from node import Node
import time
import random

ROWS = 51
DEFAULT_WIDTH = 1000
assert ROWS % 2 != 0, "Rows must be odd!"
WIDTH = DEFAULT_WIDTH if DEFAULT_WIDTH % ROWS == 0 else DEFAULT_WIDTH - DEFAULT_WIDTH % ROWS
WIN = pygame.display.set_mode((WIDTH + 400, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")
pygame.font.init()
header_font = pygame.font.Font("assets/Akshar-Regular.ttf", 70)
rules_font = pygame.font.Font("assets/Akshar-Regular.ttf", 30)
time_taken = 0

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

def draw(win, grid):
	for row in grid:
		for node in row:
			node.draw(win)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	y, x = pos

	y = y if y < width else width - 1 or y if y >= 0 else 0
	x = x if x < width else width - 1 or x if x >= 0 else 0

	gap = width // rows

	row = y // gap
	col = x // gap

	return row, col


def convert_time(time_taken):
	if time_taken < 1000:
		return f"{round(time_taken, 2)}ns"
	elif time_taken < 1000000:
		return f"{round(time_taken / 1000, 2)}μs"
	elif time_taken < 1000000000:
		return f"{round(time_taken / 1000000, 2)}ms"
	else:
		return f"{round(time_taken / 1000000000, 2)}s"

def draw_panel_2(win, nodes_explored, path_length, time_taken):
	pygame.draw.rect(win, WHITE, (WIDTH + 1, 0, 399, WIDTH))
	click_and_play = header_font.render("Click & Play!", True, (0, 0, 0))
	win.blit(click_and_play, (WIDTH + 40, 20))
   
	have_fun = header_font.render("Have Fun!", True, (0, 0, 0))
	win.blit(have_fun, (WIDTH + 77, 850))

	time_taken = convert_time(time_taken)
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
		"C:",
		"    Clear Board",
		"Space:",
		"    Start / Stop Algorithm",
		"     ",
		f"Nodes Explored: {nodes_explored}",
		f"Path Length: {path_length}",
		f"Time Taken: {time_taken}"
	]

	text_surfaces = []
	text_positions = []

	for i, line in enumerate(rules_lines):
		font_color = (0, 0, 0)  # Default color

		if i == 1:
			font_color = (255, 165, 0)  # Orange
		elif i == 2:
			font_color = (64, 224, 208)  # Turquoise

		text_surface = rules_font.render(line, True, font_color)
		text_positions.append((WIDTH + 30, 120 + i * 40))
		text_surfaces.append(text_surface)

	for surface, position in zip(text_surfaces, text_positions):
		win.blit(surface, position)

	update_algo(win, algo_index, rules_font)


def draw_panel(win, nodes_explored, path_length):
	pygame.draw.rect(win, WHITE, (WIDTH, 0, 400, WIDTH))
	click_and_play = header_font.render("Click & Play!", True, (0, 0, 0))
	win.blit(click_and_play, (WIDTH + 40, 20))
   
	have_fun = header_font.render("Have Fun!", True, (0, 0, 0))
	win.blit(have_fun, (WIDTH + 77, 680))

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
		"C:",
		"    Clear Board",
		"Space:",
		"    Start / Stop Algorithm",
		"     ",
		f"Nodes Explored: {nodes_explored}",
		f"Path Length: {path_length}"
	]

	text_surfaces = []
	text_positions = []

	for i, line in enumerate(rules_lines):
		font_color = (0, 0, 0)  # Default color

		if i == 1:
			font_color = (255, 165, 0)  # Orange
		elif i == 2:
			font_color = (64, 224, 208)  # Turquoise

		text_surface = rules_font.render(line, True, font_color)
		text_positions.append((WIDTH + 30, 150 + i * 40))
		text_surfaces.append(text_surface)

	for surface, position in zip(text_surfaces, text_positions):
		win.blit(surface, position)

	update_algo(win, algo_index, rules_font)

def update_algo(win, algo_index, rules_font):
	pygame.draw.rect(win, WHITE, (WIDTH + 50, 390, 300, 50))
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
		text_position = (WIDTH + 53 + len(total_algo) * 13 , 395)
		total_algo += algo
		algo_text_positions.append(text_position)

	for surface, position in zip(algo_text_surfaces, algo_text_positions):
		win.blit(surface, position)

def make_maze(grid, rows, width):
	global start, end

	gap = width // rows

	start_pos = (random.randint(1, rows - 2), random.randint(1, rows - 2))
	
	generate_maze(grid, start_pos[0], start_pos[1], rows)
	
	start = Node(start_pos[1], start_pos[0], gap, rows)
	start.make_start()
	grid[start_pos[1]][start_pos[0]] = start

	
	end_pos = (random.randint(1, rows - 2), random.randint(1, rows - 2))
	while end_pos == start_pos:
		end_pos = (random.randint(1, rows - 2), random.randint(1, rows - 2))
	end = Node(end_pos[1], end_pos[0], gap, rows)
	end.make_end()
	grid[end_pos[1]][end_pos[0]] = end

def game(win, width):
	grid = make_grid(ROWS, width)

	global algo_index, start, end, time_taken

	explored_nodes = 0
	path_length = 0
	algorithms = [A_star, BFS, DFS, GBFS, Dijkstra]

	finished = False
	run = True
	win.fill(GREY)
	pygame.draw.rect(win, WHITE, (WIDTH, 0, 400, WIDTH))
	draw_panel_2(win, explored_nodes, path_length, time_taken)


	while run:
		draw(win, grid)

		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]: # Quit the game
				run = False

			if finished and (event.type == pygame.KEYDOWN or any(pygame.mouse.get_pressed())):
				for row in grid:
					for node in row:
						if node.color == GREEN or node.color == RED or node.color == PURPLE:
							node.reset()
						node.neighbors = []
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
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					star_time = time.time_ns()
					explored_nodes, path_length = algorithms[algo_index](lambda: draw(win, grid), grid, start, end)
					end_time = time.time_ns()
					if explored_nodes == -1:
						run = False
					time_taken = end_time - star_time
					draw_panel_2(win, explored_nodes, path_length, time_taken)
					finished = True

				if event.key == pygame.K_c: # Clear the all nodes
					start = None
					end = None
					for row in grid:
						for node in row:
							node.reset()


				
				if event.key == pygame.K_a:
					algo_index = (algo_index + 1) % len(algorithms)
					update_algo(win, algo_index, rules_font)

				if event.key == pygame.K_m:
					for row in grid:
						for node in row:
							node.make_barrier()
					make_maze(grid, ROWS, width)

		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	game(WIN, WIDTH)