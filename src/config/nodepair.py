from src.data import cities
from src.exception import cityNotFoundException


def check_city_id(city):
    for index, name in enumerate(cities):
        if name == city:
            return index
    raise cityNotFoundException.CityNotFoundException(city)


class NodePair(object):
    def __init__(self, first, second):
        self.a = first
        self.b = second

    def graph_node_ids(self):
        a_id = check_city_id(self.a)
        b_id = check_city_id(self.b)
        return a_id, b_id

    def __str__(self):
        return "{0} - {1}".format(self.a, self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
