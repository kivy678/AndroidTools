# -*- coding:utf-8 -*-

##################################################################################################

import env

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
    # Flask running
    app.run(host="0.0.0.0", port=7777, debug=True)

    # tornadorunning
    #server = getServer(7777)
    #server.start()

    print("Web done...")
