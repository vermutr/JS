from abc import ABCMeta, abstractmethod


class AbstractGraph(metaclass=ABCMeta):
    @abstractmethod
    def get_node_list(self):
        pass

    def get_amount_of_nodes(self):
        return len(self.get_node_list())

    @abstractmethod
    def get_incidental_edges(self, node):
        pass

    @abstractmethod
    def get_nodes_connected_by_edge(self, edge):
        pass

    def get_neighbour_nodes(self, node):
        edges = self.get_incidental_edges(node)
        nodes = [self.get_nodes_connected_by_edge(edge) for edge in edges]
        ret_val = []
        for top_element in nodes:
            for lower_element in top_element:
                ret_val.append(lower_element)

        nodes = ret_val
        return list(filter(node.__ne__, nodes))
