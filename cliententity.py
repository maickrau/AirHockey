import cocos
from state import StateItem
from util import *

class Entity(cocos.sprite.Sprite):

    def __init__(self, init_pos, ident, sprite_sheet):
        super(Entity, self).__init__(sprite_sheet)
        StateItem.init_entity(self, init_pos, ident)
        self.old_int_pos = to_int_pos(init_pos)
        self.position = world_to_view(init_pos)

    def update(self, dt):
        print "updating entity"

class SpritelessEntity(cocos.cocosnode.CocosNode):

    def __init__(self, init_pos, ident, sprite_sheet):
    	super(SpritelessEntity, self).__init__()
        StateItem.init_entity(self, init_pos, ident)
        self.old_int_pos = to_int_pos(init_pos)
        self.position = world_to_view(init_pos)

    def update(self, dt):
        print "updating entity"

