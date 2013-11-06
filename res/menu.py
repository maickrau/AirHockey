import os.path

from pyglet import font

from cocos.actions import ActionSprite, FadeIn, Goto
from cocos.scene import Scene
from cocos.menu import Menu, MenuItem, RIGHT
from cocos.director import director
from cocos.layer import AnimationLayer

import game, tutorial, scoreboard

try:
    import pygame.mixer
except:
    class pygame():
        class mixer():
            class music():
                @staticmethod
                def load(*k,**kw): pass
                @staticmethod
                def play(*k,**kw): pass
                @staticmethod
                def stop(*k,**kw): pass
                @staticmethod
                def get_busy(*k,**kw): pass

class MainMenu(Menu):
    def __init__ (self):
        super(MainMenu, self).__init__("X-25: Unplugged")
        self.font_title = 'Baveuse'
        self.font_items = 'Baveuse'
        
        self.menu_halign = RIGHT

        self.font_title_color = (0.6, 0.6, 0.6, 1.0 )
        self.font_items_color = (0.6, 0.6, 0.6, 1.0 )
        self.font_items_selected_color = (0.31, 0.0, 0.31, 1.0 ) 

        
        self.add_item ( MenuItem('Play', self.on_play))
        self.add_item ( MenuItem('Tutorial', self.on_tutorial))
        self.add_item ( MenuItem('High scores', self.on_hiscores))
        self.add_item ( MenuItem('Quit', self.on_quit))
        self.build_items()

    def on_play(self):
        director.push (game.GameScene())

    def on_quit(self):
        director.pop()

    def on_tutorial(self):
        director.push (tutorial.Tutorial())
    
    def on_hiscores(self):
        director.push (scoreboard.ScoreScene())

    def on_enter(self):
        super (MainMenu, self).on_enter()
        pygame.mixer.music.load(os.path.join('data', 'music', 'menu.ogg'))
        pygame.mixer.music.play(-1)
        
    def on_exit(self):
        super (MainMenu, self).on_exit()
        pygame.mixer.music.stop()
        

def MenuScene():
    bg = AnimationLayer()
    sp = ActionSprite (os.path.join ('data', 'menulogo.png'))
    bg.add (sp)
    sp.do(FadeIn(1))
    w, h = director.get_window_size()
    sp.do(Goto((w/2, h/2, 0), 0.01))
    return Scene(bg, MainMenu())
    
