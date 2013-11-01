import config
import euclid as eu

import entity
import time
from math import copysign

from util import *

class PhysicsManager():

    def __init__(self, entities):
        self.balls = []
        self.walls = []
        self.wall_corners = []
        self.prev_time = time.time()
        for e in entities:
            if isinstance(e, entity.Ball):
                self.balls.append(e)
            if isinstance(e, entity.Wall):
                self.walls.append(e)
                self.wall_corners.append(entity.WallCorner(e, 0))
                self.wall_corners.append(entity.WallCorner(e, 1))

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
            b1 = self.balls[i]
            if b1.collidable:
                for j in range(i):
                    b2 = self.balls[j]
                    if b2.collidable:
                        if PhysicsManager.isColliding(b1, b2):
                            self._collide_two_balls(b1, b2)
                for j in range(len(self.walls)):
                    w2 = self.walls[j]
                    if w2.collidable:
                        if PhysicsManager.isColliding(b1, w2):
                            self._collide_ball_with_wall(b1, w2)
                for j in range(len(self.wall_corners)):
                    c2 = self.wall_corners[j]
                    if c2.collidable:
                        if PhysicsManager.isColliding(b1, c2):
                            self._collide_ball_with_corner(b1, c2)

    def _collide_ball_with_corner(self, ball, corner):
        #collide a moving ball with a static wallcorner (aka static ball)
        coefficient_of_restitution = ball.elasticity*corner.elasticity
        relative_position = ball.pos-corner.pos
        relative_direction = relative_position.normalized()
        #push ball away from corner
        overlap = (ball.radius+corner.radius)-relative_position.magnitude()
        ball.pos += relative_direction * overlap
        #bounce ball off corner
        tangent_vel = vec_project(ball.vel, relative_direction)
        ball.vel -= tangent_vel*(1.0+coefficient_of_restitution)

    def _collide_ball_with_wall(self, ball, wall):
        #collide a moving ball with a static wall (only flat part)
        coefficient_of_restitution = ball.elasticity*wall.elasticity
        distance = wall.tangent.dot(ball.pos-wall.start)
        if (distance > 0):
            side = 1
        else:
            side = -1
        #push ball away from wall
        overlap = abs(ball.radius)-abs(distance)
        ball.pos += wall.tangent*overlap*side
        #bounce ball backwards
        tangent_vel = vec_project(ball.vel, wall.tangent)
        ball.vel -= tangent_vel*(1.0+coefficient_of_restitution)


    def _collide_two_balls(self, ball1, ball2):
        #collide two moving balls
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

    @staticmethod
    def _does_ball_collide_with_wall( wall, ball):
        if abs(wall.tangent.dot(ball.pos-wall.start)) <= ball.radius:
            inside = wall.direction.dot(ball.pos-wall.start)
            if inside >= 0 and inside <= wall.length:
                return True
        return False

    @staticmethod
    def isColliding(entity1, entity2):
        if isinstance(entity1, entity.Ball) and isinstance(entity2, entity.Ball):
            return (entity1.pos-entity2.pos).magnitude() < entity1.radius+entity2.radius
        if isinstance(entity1, entity.Ball) and isinstance(entity2, entity.WallCorner):
            return (entity1.pos-entity2.pos).magnitude() < entity1.radius+entity2.radius
        if isinstance(entity1, entity.WallCorner) and isinstance(entity2, entity.Ball):
            return (entity1.pos-entity2.pos).magnitude() < entity1.radius+entity2.radius
        if isinstance(entity1, entity.Ball) and isinstance(entity2, entity.PowerUp):
            return (entity1.pos-entity2.pos).magnitude() < entity1.radius+entity2.radius
        if isinstance(entity1, entity.PowerUp) and isinstance(entity2, entity.Ball):
            return (entity1.pos-entity2.pos).magnitude() < entity1.radius+entity2.radius
        if isinstance(entity1, entity.Wall) and isinstance(entity2, entity.Ball):
            return PhysicsManager._does_ball_collide_with_wall(entity1, entity2)
        if isinstance(entity1, entity.Ball) and isinstance(entity2, entity.Wall):
            return PhysicsManager._does_ball_collide_with_wall(entity2, entity1)
        #TODO: other shapes
        return False
