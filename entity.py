import cocos
import math
from util import *
import config
from copy import deepcopy

class EntityManager():

    def __init__(self, server=0):
        self.entities = self._generate_entities(server)
        self.state_history = History()

    def _generate_entities(self, server=0):
        if server:
            ball1 = PhysicsBall(eu.Point2(100, 100), 'letters')
            ball2 = PhysicsBall(eu.Point2(300, 100), 'arrows')
            puck = PhysicsBall(eu.Point2(200, 200), 'puck')
        else:
            ball1 = Ball(eu.Point2(100, 100), 'letters')
            ball2 = Ball(eu.Point2(300, 100), 'arrows')
            puck = Ball(eu.Point2(200, 200), 'puck')

        return [ball1, ball2, puck]


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
        return self.hist[seq - self.min]

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

    def restore_entities(ents, state_data):
        for i, ent in enumerate(ents):
            for p in self.params:
                ent.__setattribute__(p, state_data[i][p])

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
                        print 'Difference:', ent['ident'], p
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


class Entity(cocos.sprite.Sprite):

    def __init__(self, init_pos, ident, sprite_sheet):
        super(Entity, self).__init__(sprite_sheet)
        StateItem.init_entity(self, init_pos, ident)
        self.old_int_pos = to_int_pos(init_pos)
        self.position = world_to_view(init_pos)


class PhysicsBall(object):
    def __init__(self, init_pos, ident):
        self.radius = config.radius
        StateItem.init_entity(self, init_pos, ident)

class Ball(Entity):

    #Constructor for Ball instance, defaults pos x and y to 0, 0 if not given

    def __init__(self, init_pos, ident):
        super(Ball, self).__init__(init_pos, ident, ident == 'puck' and 'res/puck.png' or 'res/ball.png')

        self.radius = config.radius



class PlayerControlledBall(Ball):

    #Constructor for player controlled ball.
    #Parameter "number" is 1 for left and 2 for right(used to assign controls)
    def __init__(self, number):
        super(PlayerControlledBall, self).__init__()