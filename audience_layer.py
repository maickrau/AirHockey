import config
import cocos
import pyglet

from random import choice

class AudienceLayer(cocos.layer.Layer):
	def __init__(self):
		super(AudienceLayer, self).__init__()
		rows = config.screen_width-config.field_width
		rows /= 40
		per_row = config.screen_height/32
		sprite = pyglet.image.load_animation('res/audience.gif')
		left = cocos.sprite.Sprite(sprite)
		left.position = (config.screen_width-config.field_width)/2-sprite.get_max_width()/2, config.screen_height/2
		left.rotation = 180
		self.add(left)
		right = cocos.sprite.Sprite(sprite)
		right.position = config.screen_width-(config.screen_width-config.field_width)/2+sprite.get_max_width()/2, config.screen_height/2
		self.add(right)
