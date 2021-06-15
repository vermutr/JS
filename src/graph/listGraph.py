from src.graph.abstractGraph import AbstractGraph


class ListGraph(AbstractGraph):
    def __init__(self, list_of_adjacency_lists):
        self._incidental_edges = self.to_incidental_edge_list(list_of_adjacency_lists)

    @staticmethod
    def to_incidental_edge_list(list_of_adjacency_lists):
        edges = []
        for index, adjacency_list in enumerate(list_of_adjacency_lists):
            for node in adjacency_list:
                if edges.__contains__((node, index)):
                    continue
                edges.append((index, node))

        return edges

    def get_node_list(self):
        nodes = []
        for top_element in self._incidental_edges:
            for lower_element in top_element:
                nodes.append(lower_element)
        max_val = 0 if nodes == [] else max(nodes) + 1
        return [i for i in range(max_val)]

    def get_incidental_edges(self, node):
        incidental_edges_to_node = []
        for index, edge in enumerate(self._incidental_edges):
            if node in edge:
                incidental_edges_to_node.append(index)

        return incidental_edges_to_node

    def get_nodes_connected_by_edge(self, edge):
        return self._incidental_edges[edge]
