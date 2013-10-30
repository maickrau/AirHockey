import config
import euclid as eu

import time
from math import copysign

from util import *

class PhysicsManager():

    def __init__(self, balls):
        self.balls = balls
        self.prev_time = time.time()
        self.walls = {}

    def read_input(self, state, ident):
        input_data = state.get(ident)
        if input_data is None:
            return eu.Vector2(0, 0)
        return eu.Vector2(input_data['x'], input_data['y'])

    def update(self, dt, input_state):
#        self._debug_print_total_momentum()
#        self._debug_print_center_of_mass()
#        self._debug_print_center_of_momentum_frame()
        for ball in self.balls:
            movement = self.read_input(input_state, ball.ident)
            movement.normalize()
            self._update_acc(ball, movement)
            self._update_vel(ball, dt)
        self.collide()
        self.collide_walls()
        for ball in self.balls:
            self.update_pos(ball, dt)
        self.prev_time = time.time()

    def _debug_print_total_momentum(self):
        momentum = 0
        for ball in self.balls:
            momentum += ball.vel.magnitude()*ball.mass
        print momentum

    def _debug_print_center_of_momentum_frame(self):
        momentum = eu.Vector2(0, 0)
        mass = 0
        for ball in self.balls:
            momentum += ball.vel*ball.mass
            mass += ball.mass
        momentum /= mass
        print momentum

    def _debug_print_center_of_mass(self):
        center = eu.Vector2(0, 0)
        mass = 0
        for ball in self.balls:
            center += ball.pos*ball.mass
            mass += ball.mass
        center /= mass
        print center

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
                if b1.pos.distance(b2.pos) < b1.radius + b2.radius:
                    self._collide_two_balls(b1, b2)

    def _collide_two_balls(self, ball1, ball2):
        relative_position = ball2.pos-ball1.pos #ball2's position from ball1's frame of reference
        relative_direction = relative_position.normalized();
        coefficient_of_restitution = ball1.elasticity*ball2.elasticity
        #push balls apart so they can't get stuck inside eachothers
        #lighter ball is pushed more
        overlap = ((ball1.radius+ball2.radius)-relative_position.magnitude())
        if (overlap > 0):
            ball1.pos -= relative_direction * overlap * ball2.mass/(ball1.mass+ball2.mass)
            ball2.pos += relative_direction * overlap * ball1.mass/(ball1.mass+ball2.mass)
        #elastic/inelastic collision with varying mass
        #see: http://en.wikipedia.org/wiki/Inelastic_collision
        #and http://en.wikipedia.org/wiki/Center_of_momentum_frame
        momentum_sum = ball1.vel*ball1.mass+ball2.vel*ball2.mass
        center_of_momentum = momentum_sum/(ball1.mass+ball2.mass)
        #transform balls to the center of momentum frame
        ball1.vel -= center_of_momentum
        ball2.vel -= center_of_momentum
        #collide
        velocity_normal1 = vec_project(ball1.vel, relative_direction)
        velocity_normal2 = vec_project(ball2.vel, relative_direction)
        ball1.vel -= velocity_normal1*(1.0+coefficient_of_restitution)
        ball2.vel -= velocity_normal2*(1.0+coefficient_of_restitution)
        #transform back into world frame
        ball1.vel += center_of_momentum
        ball2.vel += center_of_momentum
        return


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

    def isColliding(entity1, entity2):
        #TODO implement
        return False
