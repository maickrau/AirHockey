import cocos

import pyglet
from pyglet import clock

import game_layer

#Entry point
if __name__ == "__main__":
    clock.set_fps_limit(120)
    cocos.director.director.init()
    game = game_layer.GameLayer()
    scene = cocos.scene.Scene(game)
    cocos.director.director.run(scene)
