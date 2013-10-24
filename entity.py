import cocos
import math
from threading import Timer
from util import *
import config

class EntityManager():

    def __init__(self):
        self.entities = self.__generateEntities__()

    def __generateEntities__(self):
        #TODO Remove placeholder code
        ball1 = Ball(eu.Point2(100, 100), 'letters')
        ball2 = Ball(eu.Point2(300, 100), 'arrows')
        puck = Ball(eu.Point2(200, 200), 'puck')
        return [ball1, ball2, puck]

    def updater(self, obj, func, interval):
        """Thread-based timer 
        """
        def iteration(noexit=0):
            #if not noexit and not obj.closing:
            # if not noexit:
            #     print 'exiting'
            #     return
            obj._timer = Timer(interval, iteration).start()
            func(interval)

        # obj._timer = Timer(interval, iteration).start()
        iteration(1)

    def should_render(self, old, new):
        new = map(round, world_to_view(new))
        return old[0] != new[0] or old[1] != new[1]

    def render(self, dt):
        for ball in self.entities:
            if self.should_render(ball.old_int_pos, ball.pos):
                ball.position = world_to_view(ball.pos)
                ball.old_int_pos = to_int_pos(ball.pos)


class Entity(cocos.sprite.Sprite):

    def __init__(self, sprite_sheet):
        super(Entity, self).__init__(sprite_sheet)


class Ball(Entity):

    #Constructor for Ball instance, defaults pos x and y to 0, 0 if not given

    def __init__(self, init_pos, ident):
        super(Ball, self).__init__(ident == 'puck' and 'res/puck.png' or 'res/ball.png')
        # init_pos as eu.Point2
        self.pos = init_pos
        self.old_int_pos = to_int_pos(init_pos)
        self.vel = eu.Vector2(0, 0)
        self.acc = eu.Vector2(0, 0)
        # identifier of the ball, used to associate it with input
        self.ident = ident

        self.position = world_to_view(init_pos)
        self.radius = config.radius



class PlayerControlledBall(Ball):

    #Constructor for player controlled ball.
    #Parameter "number" is 1 for left and 2 for right(used to assign controls)
    def __init__(self, number):
        super(PlayerControlledBall, self).__init__()