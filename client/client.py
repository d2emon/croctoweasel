#! /usr/bin/python3
import logging


def main(connect):
    import socket
    import json

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"action": "field", "from": 0, "to": 10}).encode('UTF-8'))
    data = sock.recv(8192)
    print(data)
    sock.close()

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"action": "player", "from": 0, "to": 10}).encode('UTF-8'))
    data = sock.recv(8192)
    print(data)
    sock.close()

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"action": "players", "from": 0, "to": 10}).encode('UTF-8'))
    data = sock.recv(8192)
    print(data)
    sock.close()


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
