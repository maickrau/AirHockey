import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cocos2d-0.5.5'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pyglet-1.1.4'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Twisted-13.1.0'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'autobahn-0.6.4'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'zope.interface-3.8.0', 'src'))

import cocos
import config

import pyglet
from pyglet import clock

import game_layer

execfile('menu.py')

#Entry point
if __name__ == "__main__":
    #clock.set_fps_limit(120)
    cocos.director.director.init(vsync=True, height=config.height, width=config.width)
    cocos.director.director.show_FPS = True
    game = game_layer.GameLayer()
    scene = cocos.scene.Scene(game)
    cocos.director.director.run(scene)
