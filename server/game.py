import logging


class Game(object):
    """Basic game object"""
    start_pos = 0
    finish_pos = 120

    field = []
    players = []
    leaders = []
    turn = 0

    def __init__(self):
        import field

        self.turn = 0
        self.leaders = []
        self.field = field.getField(self.start_pos, self.finish_pos+1)

    def start(self):
        logging.info("Starting game")
        self.__init__()
        for player in self.players:
            print("Started %s" % (player))
            player.start()

    def nextTurn(self):
        self.turn += 1
        logging.info("Starting turn #%s", self.turn)

        turners = [player for player in self.players if not player.isFinished()]
        logging.debug("Players are %s.", turners)
        for player in turners:
            player.turn()

    def isFinished(self):
        return len(self.leaders) >= len(self.players)

    def dice(self):
        import random
        roll = random.randint(1, 6)
        logging.debug("1d6=%s", roll)
        return roll
