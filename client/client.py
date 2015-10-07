#! /usr/bin/python3
import logging


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

        print("Sending")
        print(data)
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


def stats(sock, code):
    print('----')
    print(sock.sendrecv({"action": "game"}, 8192))
    print(sock.sendrecv({"action": "player", "code": code}, 8192))


def main(connect):
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
    for l in locations:
        print("%d.\t%s\n\t%s" % (l["id"], l["name"], l["description"]))
    stats(sock, 0)

    userName = raw_input("Enter your name:")
    code = sock.sendrecv({"action": "add", "name": userName}, 8192)["code"]
    print(code)

    data = sock.sendrecv({"action": "start"}, 8192)
    print(data)
    stats(sock, code)

    turn = "y"
    while turn == "y":
        data = sock.sendrecv({"action": "turn", "code": code}, 8192)
        print(data)
        stats(sock, code)
        turn = raw_input("Next turn?")


if __name__ == '__main__':
    import sys
    args = sys.argv
    print(args)
    logfile = 'server.log'
    loglevel = logging.DEBUG
    server = 'localhost'
    port = 9090

    logging.basicConfig(
        filename=logfile,
        level=loglevel
    )
    connect = (server, port)

    main(connect)
