#! /usr/bin/python3
import logging


def main(connect):
    import socket
    import json

    sock = socket.socket()
    sock.connect(connect)
    sent = "actiontestexthello world!"
    print(sent)
    sock.send(sent.encode('UTF-8'))
    data = sock.recv(1024)
    sock.close()
    print(data)

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"text": "hello world!"}).encode('UTF-8'))
    data = sock.recv(1024)
    print(data)
    sock.close()

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"action": "tet", "text": "hello world!"}).encode('UTF-8'))
    data = sock.recv(1024)
    print(data)
    sock.close()

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"action": "test", "text": "hello world!"}).encode('UTF-8'))
    data = sock.recv(1024)
    print(data)
    sock.close()

    sock = socket.socket()
    sock.connect(connect)
    sock.send(json.dumps({"action": "field", "text": "hello world!"}).encode('UTF-8'))
    data = sock.recv(1024)
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
