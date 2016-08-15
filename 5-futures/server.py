#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.gen


def async_file_read():
    return tornado.gen.sleep(3)


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        yield async_file_read()
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
