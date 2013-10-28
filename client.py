from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS

import config
import json

class HockeyClientProtocol(WebSocketClientProtocol):

    def sendHello(self):
        self.sendMessage(json.dumps({'type': 'hello'}))

    def onOpen(self):
        #self.sendHello()
        self.factory.proto = self
        self.connected = True

    def onMessage(self, msg, binary):
        self.factory.entity_manager.compare_server_state(json.loads(msg))
        # print "Got message: " + msg
        # reactor.callLater(1, self.sendHello)

    def onClose(self, wasClean, code, reason):
        print 'closing connection with reason:' + reason
        self.connected = False

class Client():
    def __init__(self, entity_manager):
        self.factory = WebSocketClientFactory(config.server_url, debug = False)
        self.factory.protocol = HockeyClientProtocol
        self.factory.entity_manager = entity_manager
        connectWS(self.factory)

    def send_msg(self, msg):
        msg_json = json.dumps(msg)
        if not hasattr(self.factory, 'proto'):
            return
        #reactor.callFromThread(self.factory.proto.sendMessage, msg_json)
        self.factory.proto.sendMessage(msg_json)

    def connected(self):
        if hasattr(self.factory, 'proto'):
            return self.factory.proto.connected
        return False