
handler = None

from ws4py.websocket import WebSocket
class HandlerWebSocket(WebSocket):
    def opened(self):
        global handler
        handler.addConnection(self) 

from wsgiref.simple_server import make_server
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import threading

class WsThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self, daemon=True)

    def run(self):
        print('making server')
        server = make_server('', 9000, server_class=WSGIServer,
                             handler_class=WebSocketWSGIRequestHandler,
                             app=WebSocketWSGIApplication(handler_cls=HandlerWebSocket))
        print('initializing')
        server.initialize_websockets_manager()
        print('starting')
        server.serve_forever()

thread = WsThread()
thread.start()
