#! /usr/bin/python
import logging


def test(data):
    return data


def field(data):
    return "FIELD"


def error(errcode, data):
    errors = (
        {"errcode": 0, "error": "No error"},
        {"errcode": 1, "error": "Wrong action"},
        {"errcode": 2, "error": "Unknown error"},
    )
    return errors[errcode]


actions = {
    "test": lambda data: data,
    "field": field,
}


def doAction(action, data):
    print("A:", action)

    if action in actions.keys():
        return actions[action](data)
    else:
        return error(1, data)


def main(port):
    import socket
    import json

    sock = socket.socket()
    logging.info("Binidng socket to port %s", port)
    sock.bind(('', port))
    while True:
        try:
            sock.listen(1)
            conn, addr = sock.accept()
            while True:
                data = conn.recv(1024)
                logging.info("Get data: %s", data)
                print(data)
                if not data:
                    break

                try:
                    request = json.loads(data.decode("UTF-8"))
                except(ValueError):
                    conn.send(json.dumps(error(1, data)).encode("UTF-8"))
                    break

                if not isinstance(request, dict):
                    conn.send(json.dumps(error(1, request)).encode("UTF-8"))
                    break

                if "action" in request.keys():
                    responce = doAction(request["action"], request)
                else:
                    responce = error(1, request)

                print(request)
                print(responce)
                conn.send(json.dumps(responce).encode("UTF-8"))
            conn.close()
        except (KeyboardInterrupt, SystemExit):
            break
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
