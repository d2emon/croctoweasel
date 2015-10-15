#! /usr/bin/python3
import logging


sock = None
code = 0


class SocketSender:
    sock = None

    def __init__(self, **connect_data):
        self.conn = (
            connect_data.get("host", "localhost"),
            connect_data.get("port", 9090)
        )

    def connect(self):
        import socket

        self.sock = socket.socket()
        self.sock.connect(self.conn)

    def send(self, data):
        import json

        logging.info(data)
        self.sock.send(json.dumps(data).encode('UTF-8'))

    def recv(self, size):
        import json

        return json.loads(self.sock.recv(size))

    def close(self):
        self.sock.close()

    def sendrecv(self, data, size):
        self.connect()
        self.send(data)
        responce = self.recv(size)
        self.close()
        return responce


def showField(field):
    for l in field:
        showLoc(l)


def showLoc(loc):
    print("%d.\t%s\n\t%s" % (loc["id"], loc["name"], loc["description"]))


def showGame(game):
    if game.get("errcode", 0) > 0:
        print(game)
        return True

    states = (
        "Ready to start",
        "Waiting for players",
        "Doing next turn",
        "Finished"
    )
    print("Turn #%d.\t%s" % (game["turn"], states[game["state"]]))
    for p in game["players"]:
        showPlayer(p)


def showPlayer(player):
    if player.get("errcode", 0) > 0:
        print(player)
        return True

    states = (
        "Ready to start",
        "Doing next turn",
        "Waiting for other players",
        "Finished"
    )
    print("%s.\t%s" % (player["name"], states[player["state"]]))
    showLoc(player["loc"])


def stats():
    global sock, code

    print('----')
    showGame(sock.sendrecv({"action": "game"}, 8192))
    print('----')
    showPlayer(sock.sendrecv({"action": "player", "code": code}, 8192))


def next():
    global sock, code

    sock.sendrecv({"action": "turn", "code": code}, 8192)
    stats()


def main(connect):
    import msvcrt

    global sock, code

    sock = SocketSender(
        host = connect[0],
        port = connect[1]
    )

    try:
        first_field = int(raw_input("Enter first field:"))
        last_field = int(raw_input("Enter last field:"))
    except ValueError as e:
        print(e)
        first_field = 0
        last_field = 120

    locations = sock.sendrecv({"action": "field", "from": first_field, "to": last_field}, 8192)
    showField(locations)
    stats()

    userName = raw_input("Enter your name:")
    code = sock.sendrecv({"action": "add", "name": userName}, 8192)["code"]
    print(code)

    data = sock.sendrecv({"action": "start"}, 8192)
    print(data)
    stats()

    while True:
        msvcrt.getch()
        next()


if __name__ == '__main__':
    import sys
    args = sys.argv
    print(args)
    logfile = 'client.log'
    loglevel = logging.DEBUG
    server = 'localhost'
    port = 9090

    logging.basicConfig(
        filename=logfile,
        level=loglevel
    )
    connect = (server, port)

    main(connect)
