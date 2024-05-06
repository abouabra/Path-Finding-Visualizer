import random

NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

def generate_maze(maze, x, y, WIDTH):
	hasVisited = [(x, y)]
	def visit(x, y):
		maze[y][x].reset()
		while True:
			unvisitedNeighbors = []
			if y > 1 and (x, y - 2) not in hasVisited:
				unvisitedNeighbors.append(NORTH)

			if y < WIDTH - 2 and (x, y + 2) not in hasVisited:
				unvisitedNeighbors.append(SOUTH)

			if x > 1 and (x - 2, y) not in hasVisited:
				unvisitedNeighbors.append(WEST)

			if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
				unvisitedNeighbors.append(EAST)

			if len(unvisitedNeighbors) == 0:
				return
			else:
				nextIntersection = random.choice(unvisitedNeighbors)
				if nextIntersection == NORTH:
					nextX = x
					nextY = y - 2
					maze[y - 1][x].reset()
				elif nextIntersection == SOUTH:
					nextX = x
					nextY = y + 2
					maze[y + 1][x].reset()
				elif nextIntersection == WEST:
					nextX = x - 2
					nextY = y
					maze[y][x - 1].reset()
				elif nextIntersection == EAST:
					nextX = x + 2
					nextY = y
					maze[y][x + 1].reset()

				hasVisited.append((nextX, nextY)) 
				visit(nextX, nextY)
	visit(x, y)