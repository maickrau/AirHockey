import cocos
from util import *
import config
from state import StateItem

class Entity(cocos.sprite.Sprite):

    def __init__(self, init_pos, ident, sprite_sheet):
        super(Entity, self).__init__(sprite_sheet)
        StateItem.init_entity(self, init_pos, ident)
        self.old_int_pos = to_int_pos(init_pos)
        self.position = world_to_view(init_pos)

class Ball(Entity):

    #Constructor for Ball instance, defaults pos x and y to 0, 0 if not given

    def __init__(self, init_pos, ident):
        super(Ball, self).__init__(init_pos, ident, ident == 'puck' and 'res/puck.png' or 'res/ball.png')

        self.radius = config.radius



class PlayerControlledBall(Ball):

    #Constructor for player controlled ball.
    #Parameter "number" is 1 for left and 2 for right(used to assign controls)
    def __init__(self, number):
        super(PlayerControlledBall, self).__init__()