import heapq


class TargetFound(Exception):
    pass

class NegativeWeightCycle(Exception):
    pass



class Graph:
    vertices = []
    edges = {}
    distance_from_start = {}
    came_from = {}

    def __init__ (self, vertices = [], edges = {}):
        self.vertices = vertices
        self.edges = edges

    def neighbors(self, vertex):
        """
        Returns the neighbors of a given vertex

        :param Any vertex: The vertex to consider
        :return: The neighbor and its weight if any
        """
        if vertex in self.edges:
            return self.edges[vertex]
        else:
            return False

    def is_valid (self, vertex):
        return vertex in self.vertices

    def estimate_to_complete (self, source_vertex, target_vertex):
        return 0

    def reset_search (self):
        self.distance_from_start = {}
        self.came_from = {}

    def grid_to_vertices (self, grid, diagonals_allowed = False, wall = '#'):
        """
        Converts a text to a set of coordinates

        The text is expected to be separated by newline characters
        The vertices will have (x, y) as coordinates
        Edges will be calculated as well

        :param string grid: The grid to convert
        :param Boolean diagonals_allowed: Whether diagonal movement is allowed
        :return: True if the grid was converted
        """
        self.vertices = []
        y = 0

        for line in grid.splitlines():
            for x in range(len(line)):
                if line[x] != wall:
                    self.vertices.append((x, y))
            y += 1

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if diagonals_allowed:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for coords in self.vertices:
            for direction in directions:
                x, y = coords[0] + direction[0], coords[1] + direction[1]
                if (x, y) in self.vertices:
                    if coords in self.edges:
                        self.edges[(coords)].append((x, y))
                    else:
                        self.edges[(coords)] = [(x, y)]

        return True

    def vertices_to_grid (self, mark_coords = [], wall = '#'):
        """
        Converts a set of coordinates to a text

        The text will be separated by newline characters

        :param list mark_coords: List of coordonates to mark
        :param string wall: Which character to use as walls
        :return: True if the grid was converted
        """
        x, y = (0, 0)
        grid = ''

        all_x = [i[0] for i in self.vertices]
        all_y = [i[1] for i in self.vertices]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        if isinstance(next(iter(self.vertices)), dict):
            vertices = self.vertices.keys()
        else:
            vertices = self.vertices

        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if (x, y) in mark_coords:
                    grid += 'X'
                elif (x, y) in vertices:
                    grid += '.'
                else:
                    grid += wall
            grid += '\n'

        return grid

    def depth_first_search (self, start, end = None):
        """
        Performs a depth-first search based on a start node

        The end node can be used for an early exit.
        DFS will explore the graph by going as deep as possible first
        The exploration path is a star, with each branch explored one by one
        It'll not yield exact result for the path-finding

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found or all is explored or False if not
        """
        current_distance = 0
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        try:
            self.depth_first_search_recursion(0, start, end)
        except TargetFound:
            return True
        if end:
            return False
        return False

    def depth_first_search_recursion (self, current_distance, vertex, end = None):
        """
        Recurrence function for depth-first search

        This function will be called each time additional depth is needed
        The recursion stack corresponds to the exploration path

        :param integer current_distance: The distance from start of the current vertex
        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found or all is explored or False if not
        """
        current_distance += 1
        neighbors = self.neighbors(vertex)
        if not neighbors:
            return

        for neighbor in neighbors:
            if neighbor in self.distance_from_start:
                continue

            # Adding for final search
            self.distance_from_start[neighbor] = current_distance
            self.came_from[neighbor] = vertex

            # Examine the neighbor immediatly
            self.depth_first_search_recursion(current_distance, neighbor, end)

            if neighbor == end:
                raise TargetFound

    def breadth_first_search (self, start, end = None):
        """
        Performs a breath-first search based on a start node

        This algorithm is appropriate for "One source, Multiple targets"
        The end node can be used for an early exit.
        BFS will explore the graph in concentric circles
        This is useful when controlling the depth is needed
        It'll yield exact result for the path-finding, but it's quite slow

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found or all is explored or False if not
        """
        current_distance = 0
        frontier = [(start, 0)]
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        while frontier:
            vertex, current_distance = frontier.pop(0)
            current_distance += 1
            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            for neighbor in neighbors:
                if neighbor in self.distance_from_start:
                    continue
                # Adding for future examination
                frontier.append((neighbor, current_distance))

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance
                self.came_from[neighbor] = vertex

                if neighbor == end:
                    return True

        if end:
            return False
        return True

    def greedy_best_first_search (self, start, end):
        """
        Performs a greedy best-first search based on a start node

        This algorithm is appropriate for the search "One source, One target"
        Greedy BFS will explore by always taking the best direction available
        This direction is estimated based on the estimate_to_complete function
        Not everything will be explored
        Does NOT provide the shortest path, but quite quick to run

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found, False otherwise
        """
        current_distance = 0
        frontier = [(self.estimate_to_complete(start, end), start, 0)]
        heapq.heapify(frontier)
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        while frontier:
            _, vertex, current_distance = heapq.heappop(frontier)

            current_distance += 1
            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            for neighbor in neighbors:
                if neighbor in self.distance_from_start:
                    continue

                # Adding for future examination
                heapq.heappush(frontier, (self.estimate_to_complete(neighbor, end), neighbor, current_distance))

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance
                self.came_from[neighbor] = vertex

                if neighbor == end:
                    return True

        return False

    def path (self, target_vertex):
        """
        Reconstructs the path followed to reach a given vertex

        :param Any target_vertex: The vertex to be reached
        :return: A list of vertex from start to target
        """
        path = [target_vertex]
        while self.came_from[target_vertex]:
            target_vertex = self.came_from[target_vertex]
            path.append(target_vertex)

        path.reverse()

        return path


class WeightedGraph(Graph):
    def grid_to_vertices (self, grid, diagonals_allowed = False, wall = '#', cost_straight = 1, cost_diagonal = 2):
        """
        Converts a text to a set of coordinates

        The text is expected to be separated by newline characters
        The vertices will have (x, y) as coordinates
        Edges will be calculated as well

        :param string grid: The grid to convert
        :param boolean diagonals_allowed: Whether diagonal movement is allowed
        :param float cost_straight: The cost of horizontal and vertical movements
        :param float cost_diagonal: The cost of diagonal movements
        :return: True if the grid was converted
        """
        self.vertices = []
        y = 0

        for line in grid.splitlines():
            for x in range(len(line)):
                if line[x] != wall:
                    self.vertices.append((x, y))
            y += 1

        directions_straight = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        directions_diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        directions = directions_straight[:]
        if diagonals_allowed:
            directions += directions_diagonal

        for coords in self.vertices:
            for direction in directions:
                cost = cost_straight if direction in directions_straight \
                                     else cost_diagonal
                x, y = coords[0] + direction[0], coords[1] + direction[1]
                if (x, y) in self.vertices:
                    if coords in self.edges:
                        self.edges[(coords)][(x, y)] = cost
                    else:
                        self.edges[(coords)] = {(x, y): cost}

        return True

    def dijkstra (self, start, end = None):
        """
        Applies the Dijkstra algorithm to a given search

        This algorithm is appropriate for "One source, multiple targets"
        It takes into account positive weigths / costs of travelling.
        Negative weights will make the algorithm fail.

        The exploration path is based on concentric shapes
        The frontier elements have identical / similar cost from start
        It'll yield exact result for the path-finding, but it's quite slow

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found, False otherwise
        """
        current_distance = 0
        frontier = [(0, start)]
        heapq.heapify(frontier)
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        while frontier:
            current_distance, vertex = heapq.heappop(frontier)

            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            for neighbor, weight in neighbors.items():
                # We've already checked that node, and it's not better now
                if neighbor in self.distance_from_start \
                        and self.distance_from_start[neighbor] <= (current_distance + weight):
                    continue

                # Adding for future examination
                heapq.heappush(frontier, (current_distance + weight, neighbor))

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance + weight
                self.came_from[neighbor] = vertex

        return end is None or end in self.distance_from_start

    def a_star_search (self, start, end = None):
        """
        Performs a A* search

        This algorithm is appropriate for "One source, multiple targets"
        It takes into account positive weigths / costs of travelling.
        Negative weights will make the algorithm fail.

        The exploration path is a mix of Dijkstra and Greedy BFS
        It uses the current cost + estimated cost to determine the next element to consider

        Some cases to consider:
        - If Estimated cost to complete = 0, A* = Dijkstra
        - If Estimated cost to complete <= actual cost to complete, it is exact
        - If Estimated cost to complete > actual cost to complete, it is inexact
        - If Estimated cost to complete = infinity, A* = Greedy BFS
        The higher Estimated cost to complete, the faster it goes

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found, False otherwise
        """
        current_distance = 0
        frontier = [(0, start, 0)]
        heapq.heapify(frontier)
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        while frontier:
            _, vertex, current_distance = heapq.heappop(frontier)

            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            for neighbor, weight in neighbors.items():
                # We've already checked that node, and it's not better now
                if neighbor in self.distance_from_start \
                        and self.distance_from_start[neighbor] <= (current_distance + weight):
                    continue

                # Adding for future examination
                priority = current_distance + self.estimate_to_complete(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor, current_distance + weight))

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance + weight
                self.came_from[neighbor] = vertex

                if neighbor == end:
                    return True

        return end in self.distance_from_start

    def bellman_ford (self, start, end = None):
        """
        Applies the Bellman–Ford algorithm to a given search

        This algorithm is appropriate for "One source, multiple targets"
        It takes into account positive or negative weigths / costs of travelling.

        The algorithm is basically Dijkstra, but it runs V-1 times (V = number of vertices)
        Unless there is a neigative-weight cycle (meaning there is no possible minimum), it'll yield a result
        It'll yield exact result for the path-finding

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found, False otherwise
        """
        current_distance = 0
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        for i in range (len(self.vertices)-1):
            for vertex in self.vertices:
                current_distance = self.distance_from_start[vertex]
                for neighbor, weight in self.neighbors(vertex).items():
                    # We've already checked that node, and it's not better now
                    if neighbor in self.distance_from_start \
                            and self.distance_from_start[neighbor] <= (current_distance + weight):
                        continue

                    # Adding for final search
                    self.distance_from_start[neighbor] = current_distance + weight
                    self.came_from[neighbor] = vertex

        # Check for cycles
        for vertex in self.vertices:
            for neighbor, weight in self.neighbors(vertex).items():
                if neighbor in self.distance_from_start \
                        and self.distance_from_start[neighbor] <= (current_distance + weight):
                    raise NegativeWeightCycle

        return end is None or end in self.distance_from_start

