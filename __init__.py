import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cocos2d-0.5.5'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pyglet-1.1.4'))

import cocos
import config

import pyglet
from pyglet import clock

import game_layer

#Entry point
if __name__ == "__main__":
    #clock.set_fps_limit(120)
    cocos.director.director.init(vsync=True, height=config.height, width=config.width)
    cocos.director.director.show_FPS = True
    game = game_layer.GameLayer()
    scene = cocos.scene.Scene(game)
    cocos.director.director.run(scene)
