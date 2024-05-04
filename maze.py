import random

def generate_maze(grid, grid_width):
	start_bias=random.random()
	end_bias=random.random()
	start_y = int(random.random() < start_bias * grid_width)
	start_x = random.randint(0, grid_width - 1)
	end_y = int(random.random() > 1 - end_bias * grid_width)
	end_x = random.randint(0, grid_width - 1)
	grid[start_y][start_x].make_start()
	grid[end_y][end_x].make_end()

	def build_maze(x1, y1, x2, y2):
		if x2 <= x1 or y2 <= y1:
			return
  
		if random.random() < 0.5:
			if y2 - y1 < 2:
				return
			partition_y = random.randint(y1 + 1, y2 - 1)
			for x in range(x1, x2 + 1):
				grid[partition_y][x].make_barrier()
			build_maze(x1, y1, x2, partition_y - 1)
			build_maze(x1, partition_y + 1, x2, y2)
		else:
			if x2 - x1 < 2:
				return
			partition_x = random.randint(x1 + 1, x2 - 1)
			for y in range(y1, y2 + 1):
				grid[y][partition_x].make_barrier()
			build_maze(x1, y1, partition_x - 1, y2)
			build_maze(partition_x + 1, y1, x2, y2)


	build_maze(0, 0, grid_width - 1, grid_width - 1)
	return grid[start_y][start_x], grid[end_y][end_x]
