#! /usr/bin/python
import logging
import errorcodes


def getPlayer(game, data):
    code = data.get("code", "")
    return game.getPlayer(code)


def test(game, data):
    if "text" in data.keys():
        return data["text"]
    else:
        return errorcodes.ERROR_UNKNOWN


def field(game, data):
    field_from = data.get("from", 0)
    field_to = data.get("to", 120)
    return [p.serialize() for p in game.field[field_from:field_to]]


def player(game, data):
    return getPlayer(game, data).serialize()


def players(game, data):
    return [p.serialize() for p in game.players]


def add(game, data):
    p = game.createPlayer(
        name = data.get("name", "Player %s" % (len(game.players))),
    )
    print([pl.code for pl in game.players])
    return {"code": p.code}


def gamestat(game, data):
    return game.nextTurn().serialize()


def start(game, data):
    return gamestat(game.start(), data)


def turn(game, data):
    import player

    p = getPlayer(game, data)
    p.state = player.STATE_NEXT
    return gamestat(game, data)


actions = {
    "test": test,
    "field": field,
    "add": add,
    "player": player,
    "players": players,
    "game": gamestat,
    "start": start,
    "turn": turn
}


def doAction(game, action, data):
    if action in actions.keys():
        responce = actions[action](game, data)
    else:
        responce = errorcodes.ERROR_ACTION

    logging.debug(responce)
    return responce


def main(port):
    import socket
    import json
    import game

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
                except Exception as e:
                    logging.error(e)
                    conn.send(json.dumps(errorcodes.ERROR_UNKNOWN).encode("UTF-8"))
                    print(e)
                    break

                try:
                    responce = doAction(g, request.get("action", "error"), request)
                    conn.send(json.dumps(responce).encode("UTF-8"))
                except errorcodes.WrongCodeError as e:
                    logging.error(e)
                    conn.send(json.dumps(errorcodes.ERROR_CODE).encode("UTF-8"))
                    print(data)
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
