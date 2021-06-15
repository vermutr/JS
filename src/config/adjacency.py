from src import data
from src.exception import cityNotFoundException

from src.exception.adjacencyListException import AdjacencyListException
from src.exception.adjacencyMatrixException import AdjacencyMatrixException


class Adjacency(object):
    @staticmethod
    def adjacency_list(node_pairs):
        adjacency_lists = [[] for _ in data.cities]

        for pair in node_pairs:
            try:
                a, b = pair.graph_node_ids()
            except cityNotFoundException.CityNotFoundException as exp:
                raise AdjacencyListException(exp)

            adjacency_lists[a].append(b)

        return adjacency_lists

    @staticmethod
    def adjacency_matrix(node_pairs):
        matrix = [[0 for _ in data.cities] for _ in data.cities]

        for pair in node_pairs:
            try:
                a, b = pair.graph_node_ids()
            except cityNotFoundException.CityNotFoundException as err:
                raise AdjacencyMatrixException(err)

            matrix[a][b] = 1

        return matrix
