import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cocos2d-0.5.5'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pyglet-1.1.4'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Twisted-13.1.0'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'autobahn-0.6.4'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'zope-3.8.0'))

from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

import json

from entity import EntityManager, StateItem
from physics import PhysicsManager
import config

class HockeyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, req):
        print 'onConnect from ' + req.peerstr
        self.entity_manager = EntityManager(1)
        self.physics_manager = PhysicsManager(self.entity_manager.entities)
        item = StateItem(self.entity_manager.entities, {'seq': 0}).state()
        item_json = json.dumps(item)
        print 'sending ', item_json
        self.sendMessage(item_json)

    def onMessage(self, msg, binary):
        print 'onMessage: ' + msg
        msg = json.loads(msg)
        if msg.get('type', '') != 'input':
            return
        self.physics_manager.update(config.tick, msg)
        item = StateItem(self.entity_manager.entities, {'seq': msg.get('seq', 0)}).state()
        item_json = json.dumps(item)
        #print 'sending ', item_json
        self.sendMessage(item_json)

if __name__ == '__main__':
 
    factory = WebSocketServerFactory("ws://localhost:54321", debug = True, debugCodePaths = True)
    factory.protocol = HockeyServerProtocol
    listenWS(factory)
    reactor.run()