#! /usr/bin/python
import logging


def print_progress(game):
    logging.debug("Turn #%s", game.turn)
    for player in [player for player in game.players if not player.isFinished()]:
        logging.debug((player.id, player.pos))
        print("%s. %s" % (player.id, player.pos))


def print_results(game):
    logging.info("Finished game")
    print("Game results:")
    for id, player in enumerate(game.leaders):
        place = id + 1
        print("%s. %s" % (place, player.id))


def main():
    from game import Game
    from player import Player

    logging.basicConfig(filename='game.log', level=logging.DEBUG)
    logging.info("------------------------------------------------------------------------")

    game = Game()
    game.players = [Player("Player%s" % (id), game) for id in range(1, 7)]

    logging.debug("Game: %s" % (game))
    logging.debug("Players: %s" % (game.players))

    game.start()
    while True:
        logging.info("Starting new turn")
        game.nextTurn()
        print_progress(game)
        if game.isFinished():
            break
    print_results(game)

if __name__ == '__main__':
    main()
