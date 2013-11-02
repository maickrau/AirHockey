import state
from util import *

class Entity(object):

	def __init__(self, init_pos, ident, sprite_sheet):
		state.StateItem.init_entity(self, init_pos, ident)
		self.old_int_pos = to_int_pos(init_pos)
		self.position = world_to_view(init_pos)
		self.dont_collide = []

	def update(self, dt):
		print "updating entity"

SpritelessEntity = Entity