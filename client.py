from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS

import config
import json
import traceback

class HockeyClientProtocol(WebSocketClientProtocol):

    def sendHello(self):
        self.sendMessage(json.dumps({'type': 'hello'}))

    def onConnect(self, resp):
        self.sendHello()
        self.factory.proto = self
        self.connected = True
        print 'onConnect to', resp.peerstr

    def onMessage(self, msg, binary):
        #print "Got message: " + msg
        msg = json.loads(msg)
        msg_type = msg.get('type', '')
        if msg_type == 'waiting':
            print 'Waiting for party...'
        elif msg_type == 'pre_init':
            self.factory.game_layer.pre_init(msg)
        elif msg_type == 'score':
            self.factory.game_layer.score(msg)
        elif msg_type == 'leave':
            print 'Another player left the game, we are leaving too'
            self.factory.game_layer.shutdown()
        else: # state update
            self.factory.game_layer.update_from_server(msg)
        # reactor.callLater(1, self.sendHello)

    def onClose(self, wasClean, code, reason):
        print 'closing connection with reason:' + reason
        self.connected = False

class Client():
    def __init__(self, game_layer):
        self.factory = WebSocketClientFactory(config.server_url, debug = False)
        self.factory.protocol = HockeyClientProtocol
        self.factory.game_layer = game_layer
        connectWS(self.factory)

    def send_msg(self, msg):
        msg_json = json.dumps(msg)
        #print 'Sending message:', msg_json
        if not hasattr(self.factory, 'proto'):
            return
        #reactor.callFromThread(self.factory.proto.sendMessage, msg_json)
        self.factory.proto.sendMessage(msg_json)

    def connected(self):
        if hasattr(self.factory, 'proto'):
            return self.factory.proto.connected
        return False