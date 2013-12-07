import cocos
import physics
import input
import config
import client
from state import EntityManager, StateItem, History
import util
from util import mstime
import AI
from twisted.internet import reactor
from threading import Timer, Thread
import pyglet

from copy import deepcopy
import json
import random

import sounds

class GameLayer(cocos.layer.Layer):

    #Lets the layer receive events from director.window
    is_event_handler = True

    def __init__(self, start_game_callback, is_restart=0, max_goals=3):
        super(GameLayer, self).__init__()
        self.start_game = start_game_callback
        self.entity_manager = EntityManager(0)
        self.entity_manager2 = EntityManager(0)
        self.shutting_down = 0
        self.seq = self.server_seq = 0
        self.soft_skip_count = self.hard_skip_count = 0
        self.total_soft_skip_count = self.total_hard_skip_count = 0
        self.max_goals = max_goals
        self.game_over = False
        self.goals1 = 0
        self.goals2 = 0
        self.goalsign = cocos.text.Label("0123456789-", font_size=32, anchor_x='center',anchor_y='top', color=(0, 0, 0, 255))
        self.goalsign.position = config.field_width/2, config.field_height
        self.ready_message = cocos.text.Label("Get ready", font_size=64, anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        self.go_message = cocos.text.Label("GO!", font_size=96, anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        self.ready_message.position = config.field_width/2, config.field_height/2
        self.go_message.position = self.ready_message.position
        self._update_score_signs()
        self.add(self.goalsign)
        self.send_times = []
        self.paused = False
        
        self.playing_sounds = []
        self.background_player = pyglet.media.Player()
        self.background_player.eos_action = 'loop'
#        self.background_player.queue(sounds.background)
#        self.background_player.play()

        if not config.single_player:
            if not is_restart:
                self.net = client.Client(self)
        else:
            self.pre_init({'num': '1'})

        #Schedule the render method
        self.schedule(self.entity_manager.render)
#        if not is_restart:
            # start Twisted's reactor in another thread

    def score(self, msg):
        scores = msg['score']
        self.goals1 = scores['1']
        self.goals2 = scores['2']
        self.stop_updater()
        self.seq = self.input_manager.serial['seq'] = 0
        self.entity_manager.reset()
        self._update_score_signs()
        self._get_ready()
        self.playing_sounds.append(sounds.goal.play())

    def _get_ready(self):
        #pause the game and show "get ready"
        if self._check_quit_condition():
            return
        self.paused = True
        self.add(self.ready_message)
        reactor.callLater(config.get_ready_time, self._remove_get_ready)

    def _remove_get_ready(self):
        #unpause, replace "get ready" with "go"
        self.paused = False
        self.remove(self.ready_message)
        self.add(self.go_message)
        reactor.callLater(config.go_time, self._remove_go)
#        self.playing_sounds.append(sounds.go.play())

    def _remove_go(self):
        self.remove(self.go_message)

    def _did_i_win(self):
        num = int(self.input_manager.num)
        if self.exch_goals:
            num ^= 3
        if num == 1:
            if self.goals1 >= self.max_goals:
                return True
        else:
            if self.goals2 >= self.max_goals:
                return True
        return False

    def _check_goals(self):
        goal = self.entity_manager.is_goal()
        if goal == 0:
            return
        if goal == 1:
            self.goals1 += 1
        elif goal == 2:
            self.goals2 += 1
        self.entity_manager.reset()
        self._update_score_signs()
        self._get_ready()
        self.playing_sounds.append(sounds.goal.play())

    def _update_score_signs(self):
        self.goalsign.element.text = str(self.goals1) + '-' + str(self.goals2)

    def _check_quit_condition(self):
        if self.goals1 >= self.max_goals:
            return True
        if self.goals2 >= self.max_goals:
            return True
        return False

    def pre_init(self, msg):
        if config.local_multiplayer:
            self.input_manager = input.InputManager('1', 1)
            self.input_manager2 = input.InputManager('2', 2)
        else:
            self.input_manager = input.InputManager(msg['num'])
            self.exch_goals = msg['exch_goals']
        self.physics_manager = physics.PhysicsManager(self.entity_manager.entities)
        self.physics_manager2 = physics.PhysicsManager(self.entity_manager2.entities)

        #Add entities to layer
        for e in self.entity_manager.entities:
            self.add(e)
            colors = {
                'arrows1': (255, 0, 0),
                'arrows2': (0, 0, 255),
                'letters1': (255, 128, 0),
                'letters2': (0, 128, 255),
            }
            ident = e.ident
            if self.exch_goals: # if we have exchanged goals, color balls accordingly
                ident = ident.replace('1', '9')
                ident = ident.replace('2', '1')
                ident = ident.replace('9', '2')
            color = colors.get(ident)
            if color:
                e.color = color
                e.default_color = color
			

        # Set a timer-based updater for internal state
        self.updater(self.update_state, config.tick)

        self._get_ready()

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
        if self.paused:
            return
        if self.game_over:
            return
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
            if config.local_multiplayer:
                ai_input = self.input_manager2.serial
            else:
                ai_input = AI.AI_commands(self.entity_manager)
            ai_input['seq'] = self.seq
            local_input.update(ai_input)
        last_hist_item = self.entity_manager.state_history.get_last()
#        if last_hist_item is not None:
        if not config.single_player and last_hist_item is not None:
            input_state = self.input_manager.combine(last_hist_item['input'], local_input)
        else:
            input_state = local_input
        if not config.single_player:
            self.send_times.append(mstime())
            self.net.send_msg(local_input)
        self.entity_manager.update(dt)
        self.physics_manager.update(dt, input_state)
        self.entity_manager.recolor_balls(input_state)
        self.entity_manager.add_to_history(input_state)
        if config.single_player or config.server:
            self._check_goals()
        if self._check_quit_condition():
            # We have to use pyglet's scheduler because show_end_text creates a text label
            # Creating/modifying a label at the 'wrong' time will cause an error in pyglet
            pyglet.clock.schedule_once(self._show_end_text, 0)
            self.game_over = True
        #print 'seq:', self.input_manager.serial['seq'], 'spent time:', mstime(start)

    def _show_end_text(self, dt):
        end_label = cocos.text.Label("", font_size=64, anchor_x='center', anchor_y='bottom', color=(0, 0, 0, 255))
        end_label.position = config.field_width/2, config.field_height/2
        if not config.local_multiplayer:
            if self._did_i_win():
                end_label.element.text = "You won!"
                self.playing_sounds.append(sounds.win.play())
            else:
                end_label.element.text = "You lost!"
                self.playing_sounds.append(sounds.lose.play())
        else:
            if self._did_i_win():
                end_label.element.text = "Player 1 won!"
            else:
                end_label.element.text = "Player 2 won!"
            # everyone is a winner
            self.playing_sounds.append(sounds.win.play())
        self.add(end_label)
        continue_label = cocos.text.Label("Press Enter to continue", font_size=16, anchor_x='center', anchor_y='top', color=(0, 0, 0, 255))
        continue_label.position = config.field_width/2, config.field_height/2-16
        self.add(continue_label)

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
        if key == 65293 and self.game_over: #65293 is enter
            self.shutdown()
        if key == 114 and config.single_player: # letter R
            self.restart()
        if hasattr(self, 'input_manager'):
            self.input_manager.update_key(key, 1)
        if hasattr(self, 'input_manager2'):
            self.input_manager2.update_key(key, 1)

    def on_key_release(self, key, modifiers):
        if hasattr(self, 'input_manager'):
            self.input_manager.update_key(key, 0)
        if hasattr(self, 'input_manager2'):
            self.input_manager2.update_key(key, 0)

    def on_close(self):
        print 'Close button pressed, shutting down'
        self.shutdown(do_quit=1)

    def stop_updater(self):
        if hasattr(self, 'updater_delayed') and self.updater_delayed.active():
            self.updater_delayed.cancel()

    def shutdown(self, do_quit=0, no_pop=0):
        if self.shutting_down:
            return
        self.shutting_down = 1
        self.stop_updater()
        if not config.single_player:
			self.net.send_msg({'type': 'leaving'})
        if not config.single_player and self.seq:
            total_states = self.seq + self.total_soft_skip_count + self.total_hard_skip_count
            print 'Last seq %d, last server seq %d' % (self.seq, self.server_seq)
            soft_percent = self.total_soft_skip_count * 100.0 / total_states
            print 'Total soft skips: %d - %.1f%%' % (self.total_soft_skip_count, soft_percent)
            hard_percent = self.total_hard_skip_count * 100.0 / total_states
            print 'Total hard skips: %d - %.1f%%' % (self.total_hard_skip_count, hard_percent)
        self.background_player.pause()
        for s in self.playing_sounds:
            s.pause()
        cocos.director.director.pop()

    def restart(self):
        self.stop_updater()
        self.unschedule(self.entity_manager.render)
        self.start_game(config.single_player, is_restart=1)
