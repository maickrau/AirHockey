import os, time
import euclid as eu

unit_vec_x = eu.Vector2(1, 0)
unit_vec_y = eu.Vector2(0, 1)

def vec_project(a, b):
    """Project Vector2 a onto b"""
    b_norm = b.normalized()
    return a.dot(b_norm) * b_norm

def to_int_pos(pos):
    return map(round, world_to_view(pos))

def world_to_view(v):
    """world coords to view coords; v an eu.Vector2, returns (float, float)"""
    scale_x = scale_y = 1
    return v.x * scale_x, v.y * scale_y

def mstime(start=0.0):
    if os.name == 'nt':
        return time.clock() * 1000 - start
    else:
        return time.time() * 1000 - start


class Timer():

    def __init__(self, timems):
        self.totalms = 0
        self.milliseconds = timems

    def addTime(self, dt):
        self.totalms += dt

    def isDone(self):
        if self.milliseconds <= self.totalms:
            return True
        return False
