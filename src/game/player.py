import random
import string
import logging

from .errors import WrongCodeError, ERROR_CODE
from .dice import dice


STATE_START = 0
STATE_PLAY = 1
STATE_NEXT = 2
STATE_FINISH = 3


class Players:
    def __init__(self, players):
        self._players = [Player(name=name) for name in players]
        self.player_id = -1
        self.leaders = []

    def clear(self):
        self._players = []
        self.leaders = []

    def __len__(self):
        return len(self._players)

    def players(self):
        for player in self._players:
            yield player

    def __getitem__(self, item):
        if len(self._players) <= 0:
            raise WrongCodeError(ERROR_CODE["error"])

        return self._players[item]

    def append(self, player):
        self._players.append(player)
        # if self.state > STATE_START:
        #     player.start(self.turn)
        return player

    @property
    def active(self):
        return filter(lambda player: not player.finished, self._players)

    @property
    def playing(self):
        return filter(lambda player: player.state not in (STATE_NEXT, STATE_FINISH), self._players)


class Player(object):
    """Player class for simple game"""
    def __init__(self, name=None):
        self.pos = 0
        self.name = name or self.code()
        self.state = STATE_START
        self.history = []

    @classmethod
    def code(cls):
        return ''.join(random.choice(string.digits+'abcdef') for _ in range(32))

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def serialize(self):
        return {
            "name": str(self),
            "state": self.state,
            "loc": self.pos,
        }

    @property
    def finished(self):
        return self.state == STATE_FINISH

    def start(self, turn=0):
        self.state = STATE_PLAY

    def finish(self):
        self.state = STATE_FINISH

    def roll(self, moves):
        self.state = STATE_PLAY
        logging.info("Doing %s's turn:", self.name)
        if moves is None:
            moves = dice()
        return self.pos + moves
