#! /usr/bin/python
import logging

from game import Game
from game.player import Player


CONFIG = {
    'logging': {
        # 'filename': 'game.log',
        'level': logging.DEBUG
    }
}


def main():
    game = Game(["Player {}".format(player_id + 1) for player_id in range(2)])
    logging.debug("Players: %s", game.players)

    game.start()
    while not game.finished:
        # Show turn title
        print("Turn #{}".format(game.turn))
        print("=" * 80)
        game.next()

        # Show turn results
        for player in game.players.active:
            print("\t{player}. {place}".format(player=player.name, place=game.field[player.pos]))

    # Show results
    print("Game results:")
    for id, player in enumerate(game.players.leaders):
        place = id + 1
        print("{}. {} ({})\n{}".format(place, player.name, len(player.history), player.history))


if __name__ == '__main__':
    logging.basicConfig(**CONFIG['logging'])
    main()
