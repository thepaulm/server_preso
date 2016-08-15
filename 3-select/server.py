#!/usr/bin/env python

import socket
import subprocess
import select
import functools


class Client(object):
    def __init__(self, con):
        self.con = con

    def send(self, page):
        self.con.send("HTTP/1.0 200 OK\n\n")
        print "sending page ..."
        self.con.send(page)
        print "done sending."
        self.con.close()

    def sock(self):
        return self.con


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

    def sock(self):
        return self.s


class SelectContext(object):
    def __init__(self):
        self.ios = dict()

    def add(self, io, f):
        self.ios[io] = f

    def remove(self, io):
        del self.ios[io]

    def set(self):
        return self.ios.keys()

    def fire(self, io):
        self.ios[io]()


def async_file_read():
    proc = subprocess.Popen('sleep 3 && echo done', stdout=subprocess.PIPE, shell=True)
    return proc.stdout


def sender(ctx, f, client):
    ctx.remove(f)
    client.send("<head><title>Web Page</title></head><h1>Hello!</h1>")
    ctx.remove(client.sock())


def reader(ctx, client):
    request = client.con.recv(4096)
    print "req: ", request

    f = async_file_read()
    ctx.add(f, functools.partial(sender, ctx, f, client))


def acceptor(ctx, l):
    client = l.accept()
    ctx.add(client.sock(), functools.partial(reader, ctx, client))


def main():
    ctx = SelectContext()
    l = Listener(8080)
    ctx.add(l.sock(), functools.partial(acceptor, ctx, l))

    while True:
        (read, write, ex) = select.select(ctx.set(), [], [])
        for r in read:
            ctx.fire(r)


if __name__ == '__main__':
    main()
