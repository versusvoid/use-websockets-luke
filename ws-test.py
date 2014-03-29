#!/usr/bin/env python


import threading
import json

class TestThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self, target=self)
        self.socket = socket

    def run(self):
        print('running thread')
        import time
        import random
        while True:
            time.sleep(3)
            if self.socket.terminated: return
            self.socket.send(json.dumps(
            { "type": "score"
            , "data": {
                "id": int(random.uniform(0,3.99)), 
                "score": round(random.random(), 3)
              }
            }, indent=4), False)


from ws4py.websocket import WebSocket
class TestWebSocket(WebSocket):
    def opened(self):
        print('yai!')
        self.send(json.dumps(
        { "type": "table"
        , "data": [
            {"id": 0, "name": "a", "score": 1},
            {"id": 1, "name": "b", "score": 4},
            {"id": 2, "name": "c", "score": 0},
            {"id": 3, "name": "d", "score": 9}
          ]
        }, indent=4), False);
        TestThread(self).start()

from wsgiref.simple_server import make_server
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

print('making server')
server = make_server('', 9000, server_class=WSGIServer,
                     handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls=TestWebSocket))
print('initializing')
server.initialize_websockets_manager()
print('starting')
server.serve_forever()
