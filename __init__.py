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

from threading import Thread
from twisted.internet import reactor

import menu

#Entry point
if __name__ == "__main__":
    #clock.set_fps_limit(120)
    cocos.director.director.init(vsync=True, height=config.screen_height, width=config.screen_width)
    cocos.director.director.show_FPS = True

	
    pyglet.font.add_directory('.')

    Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    cocos.director.director.run( cocos.scene.Scene( menu.MainMenu() ) )
    #director.run returns only after all scenes have finished
    reactor.stop()
