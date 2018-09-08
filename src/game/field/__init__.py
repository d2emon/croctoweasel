import logging

from .place import place_from_data, Place
from .data import place_data


class Field:
    def __init__(self, start=0, finish=120):
        self.start = start
        self.finish = finish
        self.field = [place_from_data(place_id, **place_data[place_id]) for place_id in range(start, finish)]

    def __getitem__(self, item):
        if item < len(self.field):
            return self.field[item]

        logging.error("%s vs %s", item, len(self.field))
        return Place(id=item, name='Error')
