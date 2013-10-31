import math
from util import *
import config

class EntityManager():

    def __init__(self, server=0):
        self.entities = self._generate_entities(server)
        self.state_history = History()

    def _generate_entities(self, server=0):

        import entity
        ball1_1 = entity.Ball(eu.Point2(100, 100), 'letters1')
        ball1_2 = entity.Ball(eu.Point2(300, 100), 'arrows1')
        ball2_1 = entity.Ball(eu.Point2(100, 700), 'letters2')
        ball2_2 = entity.Ball(eu.Point2(300, 700), 'arrows2')
        puck = entity.Ball(eu.Point2(200, 400), 'puck')

        return [ball1_1, ball1_2, ball2_1, ball2_2, puck]

    def update(self, dt):
        #Update power ups
        for e in self.entities:
            if isinstanceof(e, PowerUp):
                e.update(dt, entities)

    def _should_render(self, old, new):
        new = map(round, world_to_view(new))
        return old[0] != new[0] or old[1] != new[1]

    def render(self, dt):
        for ball in self.entities:
            if self._should_render(ball.old_int_pos, ball.pos):
                ball.position = world_to_view(ball.pos)
                ball.old_int_pos = to_int_pos(ball.pos)

    def add_to_history(self, input_state):
        self.state_history.add(StateItem(self.entities, input_state).full_state())

    def compare_server_state(self, state):
        local_state = self.state_history.get(state['seq'])
        print 'compare result',  StateItem.compare(local_state, state)



class History:
    def __init__(self):
        self.hist = []
        self.min = 1

    def add(self, item):
        if len(self.hist) >= config.state_history_size:
            self.min += 1
            del self.hist[0]
        self.hist.append(item)

    def get(self, seq):
        idx = seq - self.min
        if idx >= len(self.hist): return None
        item = self.hist[idx]
        assert item['seq'] == seq, 'Item seq: %d, requested seq: %d' % (item['seq'], seq)
        return item

    def get_after(self, seq):
        idx = seq - self.min + 1
        return self.hist[idx:]

    def replace(self, seq, item):
        idx = seq - self.min
        self.hist[idx] = item

    def delete(self, seq):
        self.min += 1
        del self.hist[0]

class StateItem:
    # physics parameters to be included in history
    params = ['ident', 'pos', 'vel', 'acc', 'max_vel', 'accValue', 'decel', 'elasticity', 'mass']
    def __init__(self, ents, input_state):

        self.entities = []
        self.input_state = input_state
        self.seq = input_state['seq']

        for i, ent in enumerate(ents):
            self.entities.append({})
            for p in self.params:
                if not hasattr(ent, p):
                    continue
                self.entities[i][p] = self.serialize_property(ent.__getattribute__(p))

    def serialize_property(self, prop):
        if isinstance(prop, eu.Vector2):
            return [prop.x, prop.y]
        else:
            return prop

    @staticmethod
    def unserialize_property(prop):
        if type(prop) == list:
            return eu.Point2(prop[0], prop[1])
        else:
            return prop

    @staticmethod
    def restore_entities(ents, state_data):
        for i, ent in enumerate(ents):
            for p in StateItem.params:
                new_prop = StateItem.unserialize_property(state_data[i][p])
                #print 'setting prop', p, 'in', ent.ident, 'to', new_prop
                ent.__setattr__(p, new_prop)

    def state(self):
        return {'entities': self.entities, 'seq': self.seq}

    def input(self):
        return self.input_state

    def full_state(self):
        return {'entities': self.entities, 'seq': self.seq, 'input': self.input_state}

    def __repr__(self):
        return self.full_state()

    @staticmethod
    def compare(self, other):
        """Compare a state with another state to determine divergence of local computations
        from server's
        """
        for i, ent in enumerate(self['entities']):
            for p in StateItem.params:
                other_prop = other['entities'][i][p]
                if ent[p] == other_prop:
                    continue
                if type(ent[p]) != list:
                    print 'Difference:', ent['ident'], p, 'seq:', self['seq']
                    print 'local', ent[p], 'server', other_prop
                    return False
                for j, val in enumerate(ent[p]):
                    if val != other_prop[j]:
                        print 'Difference:', ent['ident'], p, 'seq:', self['seq']
                        print 'local', ent[p], 'server', other_prop
                        return False
        return True

    @staticmethod
    def init_entity(self, init_pos, ident):
        """Physics properties that are not used in rendering directly
        are initialized here so that the same function could be used on server-side
        without having graphics (X window) available
        """
        self.pos = init_pos
        self.vel = eu.Vector2(0, 0)
        self.acc = eu.Vector2(0, 0)
        # identifier of the ball, used to associate it with input
        self.ident = ident

        # default physics attributes
        self.max_vel = config.max_vel
        self.accValue = config.acc  #maximum acceleration from player control, different from current acceleration
        self.decel = config.decel
        self.elasticity = config.elasticity
        self.mass = config.mass

        self.collidable = False


class PhysicsBall(object):
    def __init__(self, init_pos, ident):
        self.radius = config.radius
        StateItem.init_entity(self, init_pos, ident)