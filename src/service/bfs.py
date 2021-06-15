from collections import deque

from src.config.nodepair import check_city_id
from src.graph.abstractGraph import AbstractGraph


class Bfs(object):

    def __init__(self, graph):
        if not isinstance(graph, AbstractGraph):
            raise TypeError("Value of a \"graph\" parameter has to be AbstractGraph")
        self._graph = graph

    def find_path(self, starting_node, last_node):
        solution = self._solve(starting_node, last_node)

        if not solution:
            return []

        return self._reconstruct_path(starting_node, last_node, solution)

    def find_path_cities(self, starting_city, destination_city):
        c_from = check_city_id(starting_city)
        c_to = check_city_id(destination_city)
        return self.find_path(c_from, c_to)

    def _solve(self, starting_node, last_node):
        node_queue = deque()
        node_queue.append(starting_node)

        visited = [False if i != starting_node else True for i in self._graph.get_node_list()]
        soution = [None for _ in self._graph.get_node_list()]

        while len(node_queue):
            current_node = node_queue.popleft()
            neighbours = self._graph.get_neighbour_nodes(current_node)

            for next_node in neighbours:
                if not visited[next_node]:
                    node_queue.append(next_node)
                    visited[next_node] = True
                    soution[next_node] = current_node

        if len(visited) <= last_node or not visited[last_node]:
            return []

        return soution

    @staticmethod
    def _reconstruct_path(starting_node, last_node, solution):
        path = []
        actual = last_node

        while actual is not None:
            path.append(actual)
            actual = solution[actual]

        path.reverse()

        if path[0] == starting_node:
            return path
        return []
