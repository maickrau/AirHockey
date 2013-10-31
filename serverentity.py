from state import StateItem
from util import *

class Entity(object):

	def __init__(self, init_pos, ident, sprite_sheet):
		StateItem.init_entity(self, init_pos, ident)
		self.old_int_pos = to_int_pos(init_pos)
		self.position = world_to_view(init_pos)

	def update(self, dt):
		print "updating entity"

SpritelessEntity = Entity