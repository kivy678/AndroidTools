# -*- coding:utf-8 -*-

##################################################################################################

import env

import argparse

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.web import Application, FallbackHandler

from tornado.ioloop import IOLoop

from web.runner import app

##################################################################################################


def getServer(port):
    server = HTTPServer(WSGIContainer(app))
    server.listen(port)
    return IOLoop.instance()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Android Analysis', description='Android Analysis System')

    parser.add_argument('-p', '--port', help='Input Server Port', dest='i', type=int)

    args = parser.parse_args()

    if args.i is None:
        parser.print_help()
        exit()

    # Flask running
    app.run(host="0.0.0.0", port=args.i, debug=True)

    # tornadorunning
    #server = getServer(args.i)
    #server.start()

    print("Web done...")
