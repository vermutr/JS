from src.exception.exception import GraphException


class AdjacencyMatrixException(GraphException):
    def __str__(self):
        return "Adjacency Matrix Exception:\n" + str(self.my_exception)
