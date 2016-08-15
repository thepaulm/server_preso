#!/usr/bin/env python

import tornado.ioloop
import tornado.web


def async_file_read(f):
    tornado.ioloop.IOLoop.current().call_later(3, f)


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        async_file_read(self.readdone)

    def readdone(self):
        self.write("<head><title>Web Page</title></head><h1>Hello!</h1>")
        self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
