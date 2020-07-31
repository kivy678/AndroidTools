# -*- coding:utf-8 -*-

##################################################################################################

from tornado.websocket import WebSocketHandler

import time

##################################################################################################

class MYWebSocket(WebSocketHandler):
    def open(self):
        print("Socket opened.")

        for i in range(100):
            self.write_message("Received: " + str(i))
            time.sleep(0.1)

    def on_message(self, message):
        self.write_message("Received: " + message)
        print("Received message: " + message)

    def on_close(self):
        print("Socket closed.")
