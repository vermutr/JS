class CityNotFoundException(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "No city named " + self.name
