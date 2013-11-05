import cocos
import physics
import input
import config
import client
from state import EntityManager, StateItem, History
from util import mstime
import AI
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
        self.entity_manager2 = EntityManager(0)
        self.skip = 0
        self.seq = self.server_seq = 0
        self.soft_skip_count = self.hard_skip_count = 0
        self.total_soft_skip_count = self.total_hard_skip_count = 0
        self.send_times = []

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
        self.physics_manager2 = physics.PhysicsManager(self.entity_manager2.entities)

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
            self.updater_delayed = reactor.callLater(interval, iteration)
            if not first_run:
                func(interval)

        iteration(1)

    def should_skip(self):
        seq_diff = self.seq - self.server_seq
        if seq_diff >= config.hard_skip_thres:
            self.hard_skip_count += 1
            self.total_hard_skip_count += 1
            print 'hard skip, seq', self.seq, 'server', self.server_seq, 'count', self.hard_skip_count
            if self.hard_skip_count > config.state_history_size:
                print 'No updates from server, shutting down'
                self.shutdown()
            # self.skip = 0
            return 1
        elif seq_diff >= config.soft_skip_thres:
            self.hard_skip_count = 0
            self.soft_skip_count += 1

            if not (self.soft_skip_count - 1) % config.soft_skip_period:
                self.total_soft_skip_count += 1
                print 'soft skip, seq', self.seq, 'server', self.server_seq, 'diff', seq_diff, 'count', self.soft_skip_count
                return 1
        else:
            self.soft_skip_count = self.hard_skip_count = 0
        return 0

    def update_state(self, dt):
        """Sends input over network and calls physics_manager's update
        Called within reactor's thread
        """
        #print json.dumps(StateItem(self.entity_manager.entities, {'seq': 0}).state())
        start = mstime()
        if not config.single_player:
            if not self.net.connected():
                print 'Exiting due to disconnect from server'
                self.shutdown()

            if self.should_skip():
                return

        self.input_manager.serial['seq'] += 1
        self.seq += 1
        # the copy of the input state is used to ensure it's constant during
        # sending to server and physics computation
        local_input = deepcopy(self.input_manager.serial)
        if config.single_player:

            ai_input = AI.AI_commands(self.entity_manager.entities)
            local_input.update(ai_input)
        last_hist_item = self.entity_manager.state_history.get_last()
        if last_hist_item is not None:
            input_state = self.input_manager.combine(last_hist_item['input'], local_input)
        else:
            input_state = local_input
        if not config.single_player:
            self.send_times.append(mstime())
            self.net.send_msg(local_input)
        self.entity_manager.update(dt)
        self.physics_manager.update(dt, input_state)
        self.entity_manager.add_to_history(input_state)
        #print 'seq:', self.input_manager.serial['seq'], 'spent time:', mstime(start)

    def update_from_server(self, state):
        start_time = mstime()

        self.server_seq = state['seq']
        if state['seq'] != state['last_seq']:
            last_seq_diff = state['last_seq'] - state['seq']
            print 'Seq %d, server seq %d, server last seq %d, diff %d' % (self.seq, state['seq'], state['last_seq'], last_seq_diff)
        else:
            time_diff = mstime() - self.send_times[state['seq'] - 1]
            #print 'Seq %d, server seq %d, time diff %.0f ms' % (self.seq, self.server_seq, time_diff)
        local_state = self.entity_manager.state_history.get(state['seq'])
        compare = StateItem.compare(local_state, state)
        if not compare:
            StateItem.restore_entities(self.entity_manager2.entities, state['entities'])
            combined_input = self.input_manager.combine(state['input'], local_state['input'])
            new_hist_item = StateItem(self.entity_manager2.entities, combined_input).full_state()
            # update the history item with new entities and input
            self.entity_manager.state_history.replace(state['seq'], new_hist_item)

            # recompute all subsequent states in history
            to_recompute = self.entity_manager.state_history.get_after(state['seq'])
            for st in to_recompute:
                combined_input = self.input_manager.combine(state['input'], st['input'])
                self.entity_manager2.update(config.tick)
                self.physics_manager2.update(config.tick, combined_input)
                new_hist_item = StateItem(self.entity_manager2.entities, combined_input).full_state()
                self.entity_manager.state_history.replace(st['seq'], new_hist_item)
            StateItem.copy_entity_data(self.entity_manager2.entities, self.entity_manager.entities)
            print 'update_from_server took %.1f ms' % (mstime(start_time))
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
        if hasattr(self, 'updater_delayed') and self.updater_delayed.active():
            self.updater_delayed.cancel()
        if not config.single_player:
			self.net.send_msg({'type': 'leaving'})
        if not config.single_player and self.seq:
            total_states = self.seq + self.total_soft_skip_count + self.total_hard_skip_count
            print 'Last seq %d, last server seq %d' % (self.seq, self.server_seq)
            soft_percent = self.total_soft_skip_count * 100.0 / total_states
            print 'Total soft skips: %d - %.1f%%' % (self.total_soft_skip_count, soft_percent)
            hard_percent = self.total_hard_skip_count * 100.0 / total_states
            print 'Total hard skips: %d - %.1f%%' % (self.total_hard_skip_count, hard_percent)
        reactor.stop()
        cocos.director.director.pop()