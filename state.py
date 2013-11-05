import math
from util import *
import config
import entity

class EntityManager():

    def __init__(self, server=0):
        self.entities = self._generate_entities(server)
        self.state_history = History()

    #return player number or 0 if no goal
    def isGoal(self):
	puck = self.getByIdent('puck')
	if (puck.pos.y < config.goal_depth):
		return 2
	elif (puck.pos.y > (config.height - config.goal_depth)):
		return 1
	return 0

    def getByIdent(self, ident):
	for e in self.entities:
		if e.ident == ident:
			return e

    def reset(self):
        #TODO implement
        print "Resetting"

    def _generate_entities(self, server=0):

        #walls for everyone
        #left
        wall_points = []
        wall_points.append(eu.Point2(config.width/2-config.goal_width/2, config.height-config.goal_depth))
        wall_points.append(eu.Point2(0, config.height-config.goal_depth))
        wall_points.append(eu.Point2(0, config.goal_depth))
        wall_points.append(eu.Point2(config.width/2-config.goal_width/2, config.goal_depth))
        walls_left = entity.WallStrip("walls_left")
        walls_left.points = wall_points

        #right
        wall_points = []
        wall_points.append(eu.Point2(config.width/2+config.goal_width/2, config.height-config.goal_depth))
        wall_points.append(eu.Point2(config.width, config.height-config.goal_depth))
        wall_points.append(eu.Point2(config.width, config.goal_depth))
        wall_points.append(eu.Point2(config.width/2+config.goal_width/2, config.goal_depth))
        walls_right = entity.WallStrip("walls_right")
        walls_right.points = wall_points

        ball1_1 = entity.PlayerControlledBall(eu.Point2(config.width/4, 100), 'letters1')
        ball1_2 = entity.PlayerControlledBall(eu.Point2(3*config.width/4, 100), 'arrows1')
        ball2_1 = entity.PlayerControlledBall(eu.Point2(config.width/4, 700), 'letters2')
        ball2_2 = entity.PlayerControlledBall(eu.Point2(3*config.width/4, 700), 'arrows2')
        puck = entity.Ball(eu.Point2(config.width/2, 400), 'puck')
        stopPower = entity.StopPowerUp(eu.Point2(200, 200), 'stopPower')

        #walls close to goal
        wall_player1_goal = entity.Wall(eu.Point2(0, config.goal_depth+config.goal_wall_distance), eu.Point2(config.width, config.goal_depth+config.goal_wall_distance), "wall_player1_goal")
        wall_player2_goal = entity.Wall(eu.Point2(0, config.height-config.goal_depth-config.goal_wall_distance), eu.Point2(config.width, config.height-config.goal_depth-config.goal_wall_distance), "wall_player2_goal")

        #goal lines
        goal_player1 = entity.Wall(eu.Point2(config.width/2-config.goal_width/2, config.goal_depth), eu.Point2(config.width/2+config.goal_width/2, config.goal_depth), "player1_goal")
        goal_player2 = entity.Wall(eu.Point2(config.width/2-config.goal_width/2, config.height-config.goal_depth), eu.Point2(config.width/2+config.goal_width/2, config.height-config.goal_depth), "player2_goal")

        ball1_1.dont_collide = [wall_player1_goal]
        ball1_2.dont_collide = [wall_player1_goal]
        ball2_1.dont_collide = [wall_player2_goal]
        ball2_2.dont_collide = [wall_player2_goal]

        puck.dont_collide = [wall_player1_goal, wall_player2_goal, goal_player1, goal_player2]

        return [ball1_1, ball1_2, ball2_1, ball2_2, puck, walls_left, walls_right, stopPower, wall_player1_goal, wall_player2_goal, goal_player1, goal_player2]

    def update(self, dt):
        #Update power ups
        for e in self.entities:
            if isinstance(e, entity.PowerUp):
                e.update(dt, self.entities)

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

    #TODO ident generator/manager


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
        assert item['seq'] == seq, 'Item seq: %d, requested seq: %d, idx: %d' % (item['seq'], seq, idx)
        return item

    def get_after(self, seq):
        idx = seq - self.min + 1
        return self.hist[idx:]

    def get_last(self):
        return len(self.hist) and self.hist[-1] or None

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

    @staticmethod
    def copy_entity_data(fr, to):
        for i, ent in enumerate(fr):
            for p in StateItem.params:
                to[i].__setattr__(p, ent.__getattribute__(p))

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
                    #print 'Difference:', ent['ident'], p, 'seq:', self['seq']
                    #print 'local', ent[p], 'server', other_prop
                    return False
                for j, val in enumerate(ent[p]):
                    if val != other_prop[j]:
                        #print 'Difference:', ent['ident'], p, 'seq:', self['seq']
                        #print 'local', ent[p], 'server', other_prop
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
