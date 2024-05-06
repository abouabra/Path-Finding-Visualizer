from queue import PriorityQueue
from collections import deque
import pygame

ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)

def draw_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current.color != ORANGE and current.color != TURQUOISE:
            current.make_path()
        draw()

def A_star(draw, grid, start, end):

    def heuristic_cost_estimate(p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        return abs(x1 - x2) + abs(y1 - y2)

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
                    if neighbor.color != ORANGE and neighbor.color != TURQUOISE:
                        neighbor.make_open()
                    neighbor.updated = True

        draw()

        if current != start:
            if current.color != ORANGE and current.color != TURQUOISE:
                current.make_closed()
            current.updated = True

    return 0

def BFS(draw, grid, start, end):
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
                if neighbor.color != ORANGE and neighbor.color != TURQUOISE:
                    neighbor.make_open()

        draw()

        if current != start:
            if current.color != ORANGE and current.color != TURQUOISE:
                current.make_closed()
    return 0

def DFS(draw, grid, start, end):
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
                if neighbor.color != ORANGE and neighbor.color != TURQUOISE:
                    neighbor.make_open()

        draw()
        if current != start:
            if current.color != ORANGE and current.color != TURQUOISE:
                current.make_closed()
    return 0

def GBFS(draw, grid, start, end):
    def heuristic_cost_estimate(p1, p2):
        cache = {}
        x1, y1 = p1
        x2, y2 = p2

        if (x1, y1, x2, y2) in cache:
            return cache[(x1, y1, x2, y2)]

        res = abs(x1 - x2) + abs(y1 - y2)
        cache[(x1, y1, x2, y2)] = res    
        return res

    queue = PriorityQueue()
    queue.put((0, start))
    visited = set()
    visited.add(start)
    came_from = {}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 0

        current = queue.get()[1]

        if current == end:
            draw_path(came_from, end, draw)
            return 1

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put((heuristic_cost_estimate(neighbor.get_pos(), end.get_pos()), neighbor))
                if neighbor.color != ORANGE and neighbor.color != TURQUOISE:
                    neighbor.make_open()

        draw()

        if current != start:
            if current.color != ORANGE and current.color != TURQUOISE:
                current.make_closed()
    return 0

def Dijkstra(draw, grid, start, end):
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set()
    visited.add(start)
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 0

        current = queue.get()[1]

        if current == end:
            draw_path(came_from, end, draw)
            return 1

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                queue.put((g_score[neighbor], neighbor))
                if neighbor.color != ORANGE and neighbor.color != TURQUOISE:
                    neighbor.make_open()

        draw()

        if current != start:
            if current.color != ORANGE and current.color != TURQUOISE:
                current.make_closed()
    return 0