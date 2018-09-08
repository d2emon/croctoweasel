import logging

from .dice import dice
from .player import Players, Player
from .field import Field


STATE_START = 0
STATE_PLAY = 1
STATE_NEXT = 2
STATE_FINISH = 3


class Game(object):
    """Basic game object"""
    def __init__(self, players=None):
        self.state = STATE_START
        self.field = Field()
        self.players = Players(players)

        self.turn = 0

    def serialize(self):
        return {
            "turn": self.turn,
            "players": [p.serialize() for p in self.players],
            "state": self.state
        }

    def new_player(self, **player_data):
        return self.players.append(Player(**player_data))

    def start(self):
        if self.state > STATE_START:
            return self

        logging.info("Starting game")

        # self.players.clear()
        self.players.leaders = []
        self.turn = 0
        self.state = STATE_PLAY

        for p in self.players:
            print("Started {}".format(p))
            p.start()

    def next(self):
        if self.state not in (STATE_PLAY, STATE_NEXT):
            return

        players = self.players.playing
        # if len(players) < len(self.players):
        #     return

        self.state = STATE_NEXT

        self.turn += 1

        logging.info("Starting turn #%s", self.turn)
        logging.debug("Players are %s.", players)

        for p in players:
            self.move_player_by(p)

            place = self.field[p.pos]
            place.action(self, p)
            p.history.append(place)

        if len(self.players.leaders) >= len(self.players):
            self.state = STATE_FINISH
        else:
            self.state = STATE_PLAY

        return self

    @property
    def finished(self):
        return self.state == STATE_FINISH

    def start_player(self, player, turn=0):
        logging.info("Setting up player %s", player.name)
        self.move_player_to(player, self.field.start)
        player.start(turn)

        for _ in range(0, turn):
            player.state = STATE_NEXT
            self.move_player_by(player)
        # player.state = STATE_NEXT

    def finish_player(self, player):
        # self.move_player_to(player, self.field.finish)
        player.pos = self.field.finish
        if not(player in self.players.leaders):
            self.players.leaders.append(player)
        player.finish()

    def move_player_to(self, player, pos):
        if pos < self.field.start:
            self.start_player(player)
        elif pos >= self.field.finish:
            self.finish_player(player)
        else:
            player.pos = pos
        # player.history.append(self.field[player.pos])

    def move_player_by(self, player, moves=None):
        self.move_player_to(player, player.roll(moves))
