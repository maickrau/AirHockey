import cocos
from util import *
import config

class BgLayer(cocos.layer.Layer):

    def __init__(self):
        super(BgLayer, self).__init__()
        height = config.height / 2
        width = config.width / 2
        bg = cocos.sprite.Sprite("res/field.png", position=(width,height))
        self.add(bg)
		
class BgLayer_Tutorial(cocos.layer.Layer):

    def __init__(self):
        super(BgLayer, self).__init__()
        height = config.height / 2
        width = config.width / 2
        bg = cocos.sprite.Sprite("res/Tutorial_image.png", position=(width,height))
        self.add(bg)