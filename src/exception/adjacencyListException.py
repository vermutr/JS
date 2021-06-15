from src.exception.exception import GraphException


class AdjacencyListException(GraphException):
    def __str__(self):
        return "Adjacency List Exception:\n" + str(self.my_exception)
