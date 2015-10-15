import logging

STATE_START = 0
STATE_PLAY = 1
STATE_NEXT = 2
STATE_FINISH = 3


class Player(object):
    """Player class for simple game"""
    __pos = 0
    game = None
    log = []

    def __init__(self, game, **data):
        import random
        import string

        self.code = ''.join(random.choice(string.digits+'abcdef') for _ in range(32))
        self.game = game
        self.name = data.get("name", self.code)
        self.state = STATE_START

    def __repr__(self):
        if self.state == STATE_FINISH:
            return "%s" % self.name
        else:
            return "%s is at %s." % (self.name, self.place)

    def serialize(self):
        return {"name": self.name, "state": self.state, "loc":  self.place.serialize()}
        # "log": [l.serialize() for l in self.log]}

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
        if self.pos < len(self.game.field):
            return self.game.field[self.pos]
        else:
            logging.error("%s vs %s", self.pos, len(self.game.field))
            from place import Place
            return Place(id=self.__pos, name='Error')

    def start(self, turn=0):
        logging.info("Setting up player %s", self.name)
        self.pos = self.game.start_pos
        self.log = [self.place]
        self.state = STATE_PLAY
        for i in range(0, turn):
            self.state = STATE_NEXT
            self.turn()

    def finish(self):
        self.__pos = self.game.finish_pos
        if not(self in self.game.leaders):
            self.game.leaders.append(self)
        self.state = STATE_FINISH

    def turn(self):
        logging.info("Doing %s's turn:" % (self.name))
        self.pos += self.game.dice()
        self.log.append(self.place)
        self.place.use(self)
        self.state = STATE_PLAY
        if (self.pos >= self.game.finish_pos):
            self.state = STATE_FINISH
