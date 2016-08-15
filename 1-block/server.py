#!/usr/bin/env python

import socket
import time


class Client(object):
    def __init__(self, con):
        self.con = con

    def handle(self, call):
        request = self.con.recv(4096)
        print "req: ", request
        self.con.send("HTTP/1.0 200 OK\n\n")
        page = call()
        print "sending page ..."
        self.con.send(page)
        print "done sending."
        self.con.close()


class Listener(object):
    def __init__(self, port):
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('localhost', self.port))
        self.s.listen(socket.SOMAXCONN)

    def accept(self):
        (con, addr) = self.s.accept()
        return Client(con)


def blocking_read_file():
    time.sleep(3)


def get_web_page():
    blocking_read_file()
    return "<head><title>Web Page</title></head><h1>Hello!</h1>"


def main():
    l = Listener(8080)
    while True:
        c = l.accept()
        print "I've got a connection!"
        c.handle(get_web_page)

if __name__ == '__main__':
    main()
