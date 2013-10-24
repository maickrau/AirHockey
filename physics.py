import config
import cocos.euclid as eu

import time
from math import copysign

from util import *

class PhysicsManager():

    def __init__(self, balls, input_state):
        self.balls = balls
        self.input_state = input_state
        self.prev_time = time.time()
        self.seq = 0
        self.walls = {}

    def update(self, dt):
        # print time.time() - self.prev_time
        self.seq += 1
        for ball in self.balls:
            mx = self.input_state.get(ball.ident, 'x')
            my = self.input_state.get(ball.ident, 'y')
            self.update_acc(ball, mx, my)
            self.update_vel(ball, mx, my, dt)
        self.collide()
        self.collide_walls()
        for ball in self.balls:
            self.update_pos(ball, dt)
            # print ball.pos, dt, self.seq
        self.prev_time = time.time()

    def update_acc(self, ball, mx, my):
        """Update acceleration"""
        if mx:
            if abs(ball.vel.x) < config.max_vel or copysign(1, ball.vel.x) != mx:
                # ball is not at max speed or acc has opposite direction
                ball.acc.x = mx * config.acc
            else:
                ball.acc.x = 0 # max speed achieved, continue with it
        elif ball.vel.x:
            # if key not pressed, decelerate, i.e. accelerate with opposite sign from velocity
            ball.acc.x = -copysign(config.decel, ball.vel.x)

        if my:
            if abs(ball.vel.y) < config.max_vel or copysign(1, ball.vel.y) != my:
                ball.acc.y = my * config.acc
            else:
                ball.acc.y = 0
        elif ball.vel.y:
            ball.acc.y = -copysign(config.decel, ball.vel.y)

    def update_vel(self, ball, mx, my, dt):
        """Update velocity"""
        if ball.acc.x:
            dv = ball.acc.x * dt
            if copysign(1, ball.acc.x) == copysign(1, ball.vel.x):
                # increasing velocity
                ball.vel.x += dv
                if abs(ball.vel.x) > config.max_vel:
                    # set to max_vel, same direction
                    ball.vel.x = copysign(config.max_vel, ball.vel.x)
            else:
                # decelerating
                if abs(ball.vel.x) < abs(dv) and not mx:
                    # velocity change larger than velocity itself and we are not accelerating
                    ball.vel.x = 0
                else:
                    ball.vel.x += dv

        if ball.acc.y:
            dv = ball.acc.y * dt
            if copysign(1, ball.acc.y) == copysign(1, ball.vel.y):
                # increasing velocity
                ball.vel.y += ball.acc.y * dt
                if abs(ball.vel.y) > config.max_vel:
                    # set to max_vel, same direction
                    ball.vel.y = copysign(config.max_vel, ball.vel.y)
            else:
                # decelerating
                if abs(ball.vel.y) < abs(dv) and not my:
                    # velocity change larger than velocity itself and we are not accelerating
                    ball.vel.y = 0
                else:
                    ball.vel.y += dv

    def update_pos(self, ball, dt):
        pos = ball.pos
        pos.x += ball.acc.x * dt * dt / 2.0 + ball.vel.x * dt
        pos.y += ball.acc.y * dt * dt / 2.0 + ball.vel.y * dt

    def collide(self):
        for i in range(len(self.balls)):
            for j in range(i):
                b1 = self.balls[i]
                b2 = self.balls[j]
                if b1.pos.distance(b2.pos) >= 2 * config.radius:
                    continue
                print 'collision of', i, b1.ident, 'and', j, b2.ident
                print 'positions: %d: x: %f y: %f ; %d: x: %f y: %f' % (
                    i, b1.pos.x, b1.pos.y, j, b2.pos.x, b2.pos.y
                )
                print 'Distance: %f' % b1.pos.distance(b2.pos)
                # elastic collision, equal mass, details http://www.vobarian.com/collisions/2dcollisions2.pdf
                normal = eu.Vector2(b2.pos.x - b1.pos.x, b2.pos.y - b1.pos.y)
                tang = normal.cross()
                b1norm = vec_project(b2.vel, normal)
                b1tang = vec_project(b1.vel, tang)
                b2norm = vec_project(b1.vel, normal)
                b2tang = vec_project(b2.vel, tang)
                b1.vel.x = vec_project(b1norm, unit_vec_x).x + vec_project(b1tang, unit_vec_x).x
                b1.vel.y = vec_project(b1norm, unit_vec_y).y + vec_project(b1tang, unit_vec_y).y
                b2.vel.x = vec_project(b2norm, unit_vec_x).x + vec_project(b2tang, unit_vec_x).x
                b2.vel.y = vec_project(b2norm, unit_vec_y).y + vec_project(b2tang, unit_vec_y).y
    def collide_walls(self):
        for b in self.balls:
            if b.pos.x < b.radius:
                # left wall
                b.vel.x *= -1
                # prevent sticking to the wall
                b.pos.x += 1
            if config.width - b.pos.x < b.radius:
                # right wall
                b.vel.x *= -1
                b.pos.x -= 1
            if b.pos.y < b.radius:
                # bottom wall
                b.vel.y *= -1
                b.pos.y += 1
            if config.height - b.pos.y < b.radius:
                # top wall
                b.vel.y *= -1
                b.pos.y -= 1
