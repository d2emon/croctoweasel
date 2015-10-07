#! /usr/bin/python
import logging
import errorcodes


def test(game, data):
    if "text" in data.keys():
        return data["text"]
    else:
        return errorcodes.errors[2]


def field(game, data):
    field_from = data.get("from", 0)
    field_to = data.get("to", 120)
    return [p.serialize() for p in game.field[field_from:field_to]]


def players(game, data):
    return [p.serialize() for p in game.players]


def player(game, data):
    import player

    p = player.Player("Player%s" % (len(game.players)), game)
    game.players.append(p)
    print("New player:", p.serialize)
    return p.serialize()


def start(game, data):
    # game.start()
    # while not game.isFinished():
    #    show_turn(game)
    #    game.nextTurn()
    #    show_progress(game)
    # show_results(game)
    pass


actions = {
    "test": test,
    "field": field,
    "players": players,
    "player": player,
    "start": start
}


def doAction(game, action, data):
    if action in actions.keys():
        return actions[action](game, data)
    else:
        return errorcodes.errors[1]


def main(port):
    import socket
    import json
    import game

    # from player import Player

    sock = socket.socket()
    logging.info("Binidng socket to port %s", port)
    sock.bind(('', port))

    g = game.Game()
    while True:
        try:
            sock.listen(1)
            conn, addr = sock.accept()
            while True:
                try:
                    data = conn.recv(1024)
                except:
                    data = None

                if not data:
                    break

                try:
                    request = json.loads(data.decode("UTF-8"))
                    logging.debug(request)
                    responce = doAction(g, request.get("action", "error"), request)
                    logging.debug(responce)
                    conn.send(json.dumps(responce).encode("UTF-8"))
                except Exception as e:
                    logging.error(e)
                    conn.send(errorcodes.jsoned(1))
                    print(e)
                    break
            conn.close()
        except (KeyboardInterrupt, SystemExit):
            break
    logging.info("Server is shutting down")
    print("Bye!")


if __name__ == '__main__':
    import sys
    args = sys.argv

    print(args)
    logfile = 'server.log'
    loglevel = logging.DEBUG
    port = 9090

    logging.basicConfig(
        filename=logfile,
        level=loglevel
    )

    main(port)
