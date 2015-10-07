import logging

STATE_START = 0
STATE_PLAY = 1
STATE_NEXT = 2
STATE_FINISH = 3


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
        self.state = STATE_START

    def serialize(self):
        return {"turn": self.turn, "players": [p.serialize() for p in self.players], "state": self.state}

    def getPlayer(self, code):
        import errorcodes

        players = [p for p in self.players if p.code == code]
        if len(players) <= 0:
            raise errorcodes.WrongCodeError(errorcodes.ERROR_CODE["error"])
        return players[0]

    def createPlayer(self, **player_data):
        import player

        return self.addPlayer(player.Player(self, **player_data))

    def addPlayer(self, player):
        self.players.append(player)
        if self.state > STATE_START:
            player.start(self.turn)
        return player

    def start(self):
        if self.state > STATE_START:
            return self

        logging.info("Starting game")
        self.__init__()
        self.state = STATE_PLAY
        for player in self.players:
            print("Started %s" % (player))
            player.start()

        return self

    def nextTurn(self):
        import player

        if self.state not in ((STATE_PLAY, STATE_NEXT)):
            return self

        turners = [p for p in self.players if p.state == player.STATE_NEXT]
        if len(turners) > 0:
            self.state = STATE_NEXT
        else:
            return self

        self.turn += 1
        logging.info("Starting turn #%s", self.turn)
        logging.debug("Players are %s.", turners)

        for p in turners:
            p.turn()

        if len(self.leaders) >= len(self.players):
            self.state = STATE_FINISH

        return self

    def dice(self):
        import random
        roll = random.randint(1, 6)
        logging.debug("1d6=%s", roll)
        return roll
