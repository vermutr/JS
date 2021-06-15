
class GraphException(Exception):
    def __init__(self, my_exception):
        self.my_exception = my_exception

