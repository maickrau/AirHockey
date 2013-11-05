import cocos
from util import *

class BgLayer(cocos.layer.Layer):

    def __init__(self):
        super(BgLayer, self).__init__()
        bg = cocos.sprite.Sprite("res/field.png", position=(0,0), rotation=0, scale=1, opacity=255, color=(255, 255, 255), anchor=None)
        self.add(bg)
