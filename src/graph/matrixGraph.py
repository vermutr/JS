from src.graph.abstractGraph import AbstractGraph


class MatrixGraph(AbstractGraph):
    def __init__(self, adjacency_matrix):
        self._incidence_matrix = self.to_incidence_matrix(adjacency_matrix)

    @staticmethod
    def to_incidence_matrix(adjacency_matrix):
        edges = []
        for node_id in range(len(adjacency_matrix)):
            for pointed_node_id in range(len(adjacency_matrix[node_id])):
                if adjacency_matrix[node_id][pointed_node_id] == 0:
                    continue
                if edges.__contains__((pointed_node_id, node_id)):
                    continue
                edges.append((node_id, pointed_node_id))

        incidence_matrix = []
        for node_id in range(len(adjacency_matrix)):
            ends = []
            for edge in edges:
                ends.append(1 if node_id in edge else 0)
            incidence_matrix.append(ends)

        return incidence_matrix

    def get_node_list(self):
        return [i for i in range(len(self._incidence_matrix))]

    def get_incidental_matrix(self):
        return self._incidence_matrix

    def get_incidental_edges(self, node):
        row = self._incidence_matrix[node]
        return [i for i in range(len(row)) if row[i] == 1]

    def get_nodes_connected_by_edge(self, edge):
        return [i for i in range(len(self._incidence_matrix)) if self._incidence_matrix[i][edge] == 1]