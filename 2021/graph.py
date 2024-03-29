import heapq


class TargetFound(Exception):
    pass


class NegativeWeightCycle(Exception):
    pass


class Graph:
    def __init__(self, vertices=[], edges={}):
        self.vertices = vertices.copy()
        self.edges = edges.copy()

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

    def estimate_to_complete(self, source_vertex, target_vertex):
        return 0

    def reset_search(self):
        self.distance_from_start = {}
        self.came_from = {}

    def dfs_groups(self):
        """
        Groups vertices based on depth-first search

        :return: A list of groups
        """
        groups = []
        unvisited = set(self.vertices)

        while unvisited:
            start = unvisited.pop()
            self.depth_first_search(start)

            newly_visited = list(self.distance_from_start.keys())
            unvisited -= set(newly_visited)
            groups.append(newly_visited)

        return groups

    def depth_first_search(self, start, end=None):
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
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}

        try:
            self.depth_first_search_recursion(0, start, end)
        except TargetFound:
            return True
        if end:
            return False
        return False

    def depth_first_search_recursion(self, current_distance, vertex, end=None):
        """
        Recurrence function for depth-first search

        This function will be called each time additional depth is needed
        The recursion stack corresponds to the exploration path

        :param integer current_distance: The distance from start of the current vertex
        :param Any vertex: The vertex being explored
        :param Any end: The target/end vertex to consider
        :return: nothing
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

    def find_all_paths(self, start, end=None):
        """
        Searches for all possible paths

        To avoid loops, function is_vertex_valid_for_path must be set

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: A list of paths
        """
        self.paths = []

        return self.dfs_all_paths([start], start, end)

    def is_vertex_valid_for_path(self, path, vertex):
        """
        Determines whether a vertex can be added to a path

        The goal is to avoid loops

        :param Any path: The current path
        :param Any vertex: The vertex to be added to the path
        :return: True if the vertex can be added
        """
        return False

    def dfs_all_paths(self, path, vertex, end=None):
        """
        Recurrence function for depth-first search

        This function will be called each time additional depth is needed
        The recursion stack corresponds to the exploration path

        :param integer current_distance: The distance from start of the current vertex
        :param Any vertex: The vertex being explored
        :param Any end: The target/end vertex to consider
        :return: nothing
        """

        neighbors = self.neighbors(vertex)
        if not neighbors:
            return

        for neighbor in neighbors:
            if not self.is_vertex_valid_for_path(path, neighbor):
                continue

            new_path = path.copy()

            # Adding to path
            new_path.append(neighbor)

            # Examine the neighbor immediatly
            self.dfs_all_paths(new_path, neighbor, end)

            if neighbor == end:
                self.paths.append(new_path)

    def topological_sort(self):
        """
        Performs a topological sort

        Topological sort is based on dependencies
        All nodes are traversed, based on their dependencies
        The "distance from start" is the order to use

        :return: True when all is explored
        """
        self.distance_from_start = {}

        not_visited = set(self.vertices)
        edges = self.edges.copy()

        next_nodes = sorted(x for x in not_visited if x not in sum(edges.values(), []))
        current_distance = 0

        while not_visited:
            for next_node in next_nodes:
                self.distance_from_start[next_node] = current_distance

            not_visited -= set(next_nodes)
            current_distance += 1
            edges = {x: edges[x] for x in edges if x in not_visited}
            next_nodes = sorted(
                x for x in not_visited if not x in sum(edges.values(), [])
            )

        return True

    def topological_sort_alphabetical(self):
        """
        Performs a topological sort with alphabetical sort

        Topological sort is based on dependencies
        All nodes are traversed, based on their dependencies
        When multiple choices are available, the first one will be taken (no parallel work)
        The "distance from start" is the order to use

        :return: True when all is explored
        """
        self.distance_from_start = {}

        not_visited = set(self.vertices)
        edges = self.edges.copy()

        next_node = sorted(x for x in not_visited if x not in sum(edges.values(), []))[
            0
        ]
        current_distance = 0

        while not_visited:
            self.distance_from_start[next_node] = current_distance

            not_visited.remove(next_node)
            current_distance += 1
            edges = {x: edges[x] for x in edges if x in not_visited}
            next_node = sorted(
                x for x in not_visited if not x in sum(edges.values(), [])
            )
            if len(next_node):
                next_node = next_node[0]

        return True

    def breadth_first_search(self, start, end=None):
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
            # This allows to cover WeightedGraphs
            if isinstance(neighbors, dict):
                neighbors = list(neighbors.keys())
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

        return False

    def greedy_best_first_search(self, start, end):
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
                heapq.heappush(
                    frontier,
                    (
                        self.estimate_to_complete(neighbor, end),
                        neighbor,
                        current_distance,
                    ),
                )

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance
                self.came_from[neighbor] = vertex

                if neighbor == end:
                    return True

        return False

    def path(self, target_vertex):
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
    def dijkstra(self, start, end=None):
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
        min_distance = float("inf")

        while frontier:
            current_distance, vertex = heapq.heappop(frontier)

            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            # No need to explore neighbors if we already found a shorter path to the end
            if current_distance > min_distance:
                continue

            for neighbor, weight in neighbors.items():
                # We've already checked that node, and it's not better now
                if neighbor in self.distance_from_start and self.distance_from_start[
                    neighbor
                ] <= (current_distance + weight):
                    continue

                # Adding for future examination
                heapq.heappush(frontier, (current_distance + weight, neighbor))

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance + weight
                self.came_from[neighbor] = vertex

                if neighbor == end:
                    min_distance = min(min_distance, current_distance + weight)

        return end is None or end in self.distance_from_start

    def a_star_search(self, start, end=None):
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
                if neighbor in self.distance_from_start and self.distance_from_start[
                    neighbor
                ] <= (current_distance + weight):
                    continue

                # Adding for future examination
                priority = current_distance + self.estimate_to_complete(neighbor, end)
                heapq.heappush(
                    frontier, (priority, neighbor, current_distance + weight)
                )

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance + weight
                self.came_from[neighbor] = vertex

                if neighbor == end:
                    return True

        return end in self.distance_from_start

    def bellman_ford(self, start, end=None):
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

        for i in range(len(self.vertices) - 1):
            for vertex in self.vertices:
                current_distance = self.distance_from_start[vertex]
                for neighbor, weight in self.neighbors(vertex).items():
                    # We've already checked that node, and it's not better now
                    if (
                        neighbor in self.distance_from_start
                        and self.distance_from_start[neighbor]
                        <= (current_distance + weight)
                    ):
                        continue

                    # Adding for final search
                    self.distance_from_start[neighbor] = current_distance + weight
                    self.came_from[neighbor] = vertex

        # Check for cycles
        for vertex in self.vertices:
            for neighbor, weight in self.neighbors(vertex).items():
                if neighbor in self.distance_from_start and self.distance_from_start[
                    neighbor
                ] <= (current_distance + weight):
                    raise NegativeWeightCycle

        return end is None or end in self.distance_from_start

    def ford_fulkerson(self, start, end):
        """
        Searches for the maximum flow using the Ford-Fulkerson algorithm

        The weights of the graph are used as flow limitations
        Note: there may be multiple options, this generates only one

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: The maximum flow
        """

        if start not in self.vertices:
            raise ValueError("Source not in graph")
        if end not in self.vertices:
            raise ValueError("End not in graph")

        if end not in self.edges:
            self.edges[end] = {}

        initial_edges = {a: self.edges[a].copy() for a in self.edges}
        self.flow_graph = {a: self.edges[a].copy() for a in self.edges}

        max_flow = 0
        frontier = [start]
        heapq.heapify(frontier)

        while self.breadth_first_search(start, end):
            path_flow = float("Inf")
            cursor = end
            while cursor != start:
                path_flow = min(path_flow, self.edges[self.came_from[cursor]][cursor])
                cursor = self.came_from[cursor]

            max_flow += path_flow

            # Update the graph to change the flows
            cursor = end
            while cursor != start:
                self.edges[self.came_from[cursor]][cursor] -= path_flow
                if self.edges[self.came_from[cursor]][cursor] == 0:
                    del self.edges[self.came_from[cursor]][cursor]
                self.edges[cursor][self.came_from[cursor]] = (
                    self.edges[cursor].get(self.came_from[cursor], 0) + path_flow
                )

                cursor = self.came_from[cursor]

        cursor = end
        for vertex in self.vertices:
            for neighbor, items in self.neighbors(vertex).items():
                if neighbor in self.flow_graph[vertex]:
                    self.flow_graph[vertex][neighbor] -= self.edges[vertex][neighbor]
                    if self.flow_graph[vertex][neighbor] == 0:
                        del self.flow_graph[vertex][neighbor]

        self.edges = initial_edges

        return max_flow

    def bipartite_matching(self, starts, ends):
        """
        Performs a bipartite matching using Fold-Fulkerson's algorithm

        :param iterable starts: A list of source vertices
        :param iterable ends: A list of target vertices
        :return: The maximum matches found
        """

        start_point = "A"
        while start_point in self.vertices:
            start_point += "A"
        self.edges[start_point] = {}
        self.vertices += start_point
        for start in starts:
            if start not in self.vertices:
                return ValueError("Source not in graph")
            self.edges[start_point].update({start: 1})

        end_point = "Z"
        while end_point in self.vertices:
            end_point += "Z"
        self.vertices.append(end_point)
        for end in ends:
            if end not in self.vertices:
                return ValueError("End not in graph")
            if end not in self.edges:
                self.edges[end] = {}
            self.edges[end].update({end_point: 1})

        value = self.ford_fulkerson(start_point, end_point)
        self.vertices.remove(end_point)
        self.vertices.remove(start_point)
        return value
