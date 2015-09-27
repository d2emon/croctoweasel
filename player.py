import logging


class Player(object):
    """Player class for simple game"""
    __pos = 0
    game = None
    place = None

    def __init__(self, id, game):
        self.id = id
        self.game = game

    def __repr__(self):
        return "%s position at %s. %s." % (self.id, self.pos, self.isFinished())

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        if pos > self.game.finish:
            self.finish()
        else:
            self.__pos = pos
        if self.__pos < len(self.game.places):
            self.place = self.game.places[self.__pos]
        else:
            logging.error("%s vs %s", self.pos, len(self.game.places))
            from place import Place
            self.place = Place(self.__pos)

    def start(self):
        self.pos = 0

    def finish(self):
        self.__pos = self.game.finish

    def isFinished(self):
        return (self.pos >= self.game.finish)

    def roll(self):
        self.pos += self.game.dice()
        self.place.use(self)
