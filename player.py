import logging


class Player(object):
    """Player class for simple game"""
    __pos = 0
    game = None
    log = []

    def __init__(self, id, game):
        self.id = id
        self.game = game

    def __repr__(self):
        if self.isFinished():
            return "%s" % self.id
        else:
            return "%s is at %s." % (self.id, self.place)

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        if pos < self.game.start_pos:
            self.start()
        elif pos >= self.game.finish_pos:
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
            return Place(id=self.__pos, name='Error')

    def start(self):
        logging.info("Setting up player %s", self.id)
        self.pos = self.game.start_pos
        self.log = ["Start", self.place]

    def finish(self):
        self.__pos = self.game.finish_pos
        if not(self in self.game.leaders):
                self.game.leaders.append(self)

    def isFinished(self):
        return (self.pos >= self.game.finish_pos)

    def turn(self):
        logging.info("Doing %s's turn:" % (self.id))
        self.pos += self.game.dice()
        self.log.append(self.place)
        self.place.use(self)
