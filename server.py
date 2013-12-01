import sys
import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cocos2d-0.5.5'))
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pyglet-1.1.4'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Twisted-13.1.0'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'autobahn-0.6.4'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'zope.interface-3.8.0', 'src'))

from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

import json
import traceback

import config
config.server = True

from state import EntityManager, StateItem, History
from physics import PhysicsManager

class SessionManager:
    def __init__(self):
        self.assoc = {}
        self.pending = []
    def add(self, client):
        self.pending.append(client)
        if len(self.pending) == 2:
            session = Session(self.pending)
            for i in self.pending:
                self.assoc[i.req.peerstr] = session
            self.pending = []
            session.start()
        else:
            client.send_msg({'type': 'waiting'})

    def get(self, client):
        return self.assoc.get(client.req.peerstr)
    def delete(self, client):
        if client in self.pending:
            self.pending.remove(client)
            for c in self.pending:
                c.send_msg({'type': 'leave'})
        session = self.assoc.get(client.req.peerstr)
        if session:
            session.broadcast_msg({'type': 'leave'})
            del self.assoc[client.req.peerstr]

class Session:
    def __init__(self, clients=None):
        if clients:
            self.clients = clients
            self.in_pause = 0
            for c in clients:
                c.score = 0
        self.entity_manager = EntityManager(1)
        self.physics_manager = PhysicsManager(self.entity_manager.entities)
        self.seq = 0
        for i, c in enumerate(self.clients):
            c.num = i + 1
            c.input_history = History()
            c.last_seq = 0

    def start(self):
        #send the clients pre-init info and wait for "get ready" before actually starting
        print 'sending pre_init'
        for c in self.clients:
            c.send_msg({'type': 'pre_init', 'num': str(c.num)})
        reactor.callLater(config.get_ready_time, self.unpause)

    def unpause(self):
        self.in_pause = 0

    def reset(self):
        self.__init__()

    def msg(self, client, msg):
        if self.in_pause:
            return
        msg_type = msg.get('type', '')
        if msg_type == 'input':
            self.input(client, msg)
        elif msg_type == 'leaving':
            self.broadcast_msg({'type': 'leave'})
            for c in self.clients:
                c.sendClose()

    def input(self, client, msg):
        self.check_input(client, msg)
        client.input_history.add(msg)
        inputs = [msg]
        seq = msg['seq']
        # print 'input msg from client %d, seq %d, server seq %d, client lag %d states' % \
        #     (client.num, seq, self.seq, self.seq - seq)
        # find if there are corresponding inputs for the same state, identified by seq
        for c in self.clients:
            if c == client: continue
            inp = c.input_history.get(seq)
            if inp:
                inputs.append(inp)
        if len(inputs) == len(self.clients):
            for c in self.clients:
                c.input_history.delete(seq)
            self.update(inputs)

    def check_input(self, client, inp):
        client.last_seq += 1
        assert inp['seq'] == client.last_seq, 'Seq in msg: %d last seq %d, client %s' % (inp['seq'], client.last_seq, client.req.peerstr)
        num = str(client.num)
        allowed = ('seq', 'letters' + num, 'arrows' + num)
        for item, data in inp.items():
            if item not in allowed:
                del inp[item]

    def update(self, inputs):
        common_inp = {}
        for inp in inputs:
            common_inp.update(inp)

        self.entity_manager.update(config.tick)
        self.physics_manager.update(config.tick, common_inp)
        item = StateItem(self.entity_manager.entities, common_inp).full_state()
        self.seq = common_inp['seq']
        goal = self.entity_manager.is_goal()
        if goal:
            c = self.clients
            c[goal - 1].score += 1
            score = {'type': 'score', 'score': {'1': c[0].score, '2': c[1].score}}
            print 'Goal! Score:', score
            self.broadcast_msg(score)
            self.in_pause = 1
            self.reset()
            self.start()
            return
        #self.broadcast_msg(item)
        for c in self.clients:
            item['last_seq'] = c.last_seq
            c.send_msg(item)

    def broadcast_msg(self, msg):
        for c in self.clients:
            c.send_msg(msg)


class HockeyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, req):
        self.req = req
        print 'onConnect from ' + req.peerstr

    def onMessage(self, msg, binary):
        #print 'onMessage: ' + msg + ' client ' + self.req.peerstr
        try:
            msg = json.loads(msg)
            msg_type = msg.get('type', '')
            if msg_type == 'hello':
                self.factory.sm.add(self)
            else:
                self.factory.sm.get(self).msg(self, msg)

        except:
            traceback.print_exc()
            reactor.stop()

    def onClose(self, wasClean, code, reason):
        print 'closing connection with reason:', reason
        self.factory.sm.delete(self)

    def send_msg(self, msg):
        try:
            msg_json = json.dumps(msg)
            #print 'Sending to', self.req.peerstr, 'message:', msg_json
            return self.sendMessage(msg_json)
        except:
            traceback.print_exc()

if __name__ == '__main__':
 
    factory = WebSocketServerFactory("ws://localhost:54321", debug = False)
    factory.protocol = HockeyServerProtocol
    factory.sm = SessionManager()
    listenWS(factory)
    reactor.run()