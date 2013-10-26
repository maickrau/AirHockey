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
        print self.balls[0].vel
        for ball in self.balls:
            movement = eu.Vector2(self.input_state.get(ball.ident, 'x'), self.input_state.get(ball.ident, 'y'))
            movement.normalize()
            self._update_acc(ball, movement)
            self._update_vel(ball, dt)
        self.collide()
        self.collide_walls()
        for ball in self.balls:
            self.update_pos(ball, dt)
            # print ball.pos, dt, self.seq
        self.prev_time = time.time()

    def _update_acc(self, ball, movement):
        """Update acceleration"""
        ball.acc = eu.Vector2(0, 0)
        if movement.magnitude() > 0:
            #acceleration from player's controls
            ball.acc += movement * ball.accValue
            #deceleration to make sure player can't accelerate past max_vel
            ball.acc -= ball.vel * (ball.accValue/ball.max_vel)
        else:
            #constant deceleration from floor
            ball.acc -= ball.vel.normalized()*ball.decel

    def _update_vel(self, ball, dt):
        """Update velocity"""
        ball.vel += ball.acc * dt

    def update_pos(self, ball, dt):
        pos = ball.pos
        pos.x += ball.acc.x * dt * dt / 2.0 + ball.vel.x * dt
        pos.y += ball.acc.y * dt * dt / 2.0 + ball.vel.y * dt

    def collide(self):
        for i in range(len(self.balls)):
            for j in range(i):
                b1 = self.balls[i]
                b2 = self.balls[j]
                if b1.pos.distance(b2.pos) >= b1.radius + b2.radius:
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
