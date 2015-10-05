#! /usr/bin/python
import logging


def show_turn(game):
    print("Turn #%s" % (game.turn))


def show_progress(game):
    for player in (player for player in game.players if not player.isFinished()):
        print("%s. %s" % (player.id, player.place))


def show_results(game):
    print("Game results:")
    for id, player in enumerate(game.leaders):
        place = id + 1
        print("%s. %s.\n%s" % (place, player.id, player.log))


def main():
    from game import Game
    from player import Player

    logging.info("------------------------------------------------------------------------")
    game = Game()
    game.players = [Player("Player%s" % (id), game) for id in range(6)]
    logging.debug("Players: %s" % (game.players))

    game.start()
    while not game.isFinished():
        show_turn(game)
        game.nextTurn()
        show_progress(game)
    show_results(game)

if __name__ == '__main__':
    import sys
    args = sys.argv
    logfile = 'game.log'
    loglevel = logging.DEBUG
    logging.basicConfig(
        filename=logfile,
        level=loglevel
    )
    main()
