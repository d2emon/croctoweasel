import logging


class Player(object):
    """Player class for simple game"""
    __pos = 0
    game = None

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
        if pos < self.game.start_pos:
            self.start()
        elif pos > self.game.finish_pos:
            self.finish()
        else:
            self.__pos = pos

    @property
    def place(self):
        if self.pos < len(self.game.places):
            return self.game.places[self.pos]
        else:
            logging.error("%s vs %s", self.pos, len(self.game.places))
            from place import Place
            return Place(self.__pos)

    def start(self):
        self.pos = self.game.start_pos

    def finish(self):
        self.__pos = self.game.finish_pos

    def isFinished(self):
        return (self.pos >= self.game.finish_pos)

    def turn(self):
        self.pos += self.game.dice()
        self.place.use(self)
