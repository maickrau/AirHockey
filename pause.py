from cocos.director import director
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene

import pyglet

from pyglet.gl import *

import game_layer

__pause_scene_generator__ = None
game_layer = None

def get_pause_scene():
    return __pause_scene_generator__()
    
def set_pause_scene_generator(generator):
    global __pause_scene_generator__
    __pause_scene_generator__ = generator
    
def default_pause_scene():
    w, h = director.window.width, director.window.height
    texture = pyglet.image.Texture.create_for_size(
                    GL_TEXTURE_2D, w, h, GL_RGBA)
    texture.blit_into(pyglet.image.get_buffer_manager().get_color_buffer(), 0,0,0)
    return PauseScene(
        texture.get_region(0, 0, w, h), ColorLayer(25,25,25,205), PauseLayer()
        )
set_pause_scene_generator( default_pause_scene )

class PauseScene(Scene):
    '''Pause Scene'''
    def __init__(self, background, *layers):
        super(PauseScene, self).__init__(*layers)
        self.bg = background
        self.width, self.height = director.get_window_size()
        
    def draw(self):
        self.bg.blit(0, 0, width=self.width, height=self.height)
        super(PauseScene, self).draw()
        
        
class PauseLayer(Layer):
    '''Layer that shows the text 'PAUSED'
    '''
    is_event_handler = True     #: enable pyglet's events

    def __init__(self):
        super(PauseLayer, self).__init__()
        
        x,y = director.get_window_size()
        
        ft = pyglet.font.load('Arial', 36)
        self.text = pyglet.font.Text(ft, 
            'PAUSED', halign=pyglet.font.Text.CENTER)
        self.text.x = x/2
        self.text.y = y/2
        
    def draw(self):
        self.text.draw()
        
    def on_key_press(self, k, m):
        if k == pyglet.window.key.PAUSE:
            director.pop()
            game_layer.req_resume()
            return True