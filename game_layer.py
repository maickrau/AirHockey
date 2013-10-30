import cocos
import physics
import input
import config
import client
from state import EntityManager, StateItem, History

from twisted.internet import reactor
from threading import Timer, Thread

from copy import deepcopy
import json
import random

class GameLayer(cocos.layer.Layer):

    #Lets the layer receive events from director.window
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()

        self.entity_manager = EntityManager(0)
        self.skip = 0
        self.seq = self.server_seq = 0
        self.soft_skip_count = self.hard_skip_count = 0

        if not config.single_player:
            self.net = client.Client(self)
        else:
            self.pre_init({'num': '1'})

        #Schedule the render method
        self.schedule(self.entity_manager.render)
        # start Twisted's reactor in another thread
        Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()

    def pre_init(self, msg):
        self.input_manager = input.InputManager(msg['num'])
        self.physics_manager = physics.PhysicsManager(self.entity_manager.entities)
        
        #Add entities to layer
        for e in self.entity_manager.entities:
            self.add(e)

        # Set a timer-based updater for internal state
        self.updater(self.update_state, config.tick)

    def updater(self, func, interval):
        """Thread-based timer 
        """
        def iteration(first_run=0):
            #if not noexit and not obj.closing:
            # if not noexit:
            #     print 'exiting'
            #     return
            #self._timer = Timer(interval, iteration).start()
            reactor.callLater(interval, iteration)
            if not first_run:
                func(interval)

        iteration(1)

    def update_state(self, dt):
        """Sends input over network and calls physics_manager's update
        Called within reactor's thread
        """
        #print json.dumps(StateItem(self.entity_manager.entities, {'seq': 0}).state())
        start = reactor.seconds()
        if not config.single_player:
            if not self.net.connected():
                print 'Exiting due to disconnect from server'
                self.shutdown()

            
            seq_diff = self.seq - self.server_seq
            if seq_diff >= config.hard_skip_thres:
                self.hard_skip_count += 1
                print 'hard skip, seq', self.seq, 'server', self.server_seq, 'count', self.hard_skip_count
                if self.hard_skip_count > config.state_history_size:
                    print 'No updates from server, shutting down'
                    self.shutdown()
                # self.skip = 0
                return
            elif seq_diff >= config.soft_skip_thres:
                if not self.soft_skip_count % config.soft_skip_period:
                    self.soft_skip_count += 1
                    print 'soft skip, seq', self.seq, 'server', self.server_seq, 'diff', seq_diff, 'count', self.soft_skip_count
                    return
            else:
                self.soft_skip_count = self.hard_skip_count = 0

        self.input_manager.serial['seq'] += 1
        self.seq += 1
        # the copy of the input state is used to ensure it's constant during 
        # sending to server and physics computation
        input_state = deepcopy(self.input_manager.serial)
        if not config.single_player:
            self.net.send_msg(input_state)
        self.physics_manager.update(dt, input_state)
        self.entity_manager.add_to_history(input_state)
        #print 'seq:', self.input_manager.serial['seq'], 'spent time:', reactor.seconds() - start

    def update_from_server(self, state):
        start_time = reactor.seconds()

        self.server_seq = state['seq']
        local_state = self.entity_manager.state_history.get(state['seq'])
        compare = StateItem.compare(local_state, state)
        if not compare:
            to_recompute = self.entity_manager.state_history.get_after(state['seq'])
            StateItem.restore_entities(self.entity_manager.entities, state['entities'])
            for st in to_recompute:
                self.physics_manager.update(config.tick, st['input'])
                new_hist_item = StateItem(self.entity_manager.entities, st['input']).full_state()
                self.entity_manager.state_history.replace(st['seq'], new_hist_item)
            print 'update_from_server took', reactor.seconds() - start_time
            print 'recomputed', len(to_recompute), 'states'


    def on_key_press(self, key, modifiers):
        if hasattr(self, 'input_manager'):
            self.input_manager.update_key(key, 1)

    def on_key_release(self, key, modifiers):
        if hasattr(self, 'input_manager'):
            self.input_manager.update_key(key, 0)

    def on_close(self):
        print 'Close button pressed, shutting down'
        self.shutdown()

    def shutdown(self):
        reactor.stop()
        cocos.director.director.pop()