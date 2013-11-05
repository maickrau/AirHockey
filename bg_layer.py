import cocos
from util import *

class BgLayer(cocos.layer.Layer):

    def __init__(self):
        super(BgLayer, self).__init__()
        bg = cocos.sprite.Sprite("res/field.png", position=(200,400))
        self.add(bg)
