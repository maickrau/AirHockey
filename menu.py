# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "menu, menu_valign, menu_halign"

from pyglet import image
from pyglet.gl import *
from pyglet import font
import cocos

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *

import __init__
import config
import game_layer
import bg_layer
import audience_layer

#from cocos.menu import Menu, MenuItem, RIGHT
from cocos.director import director
#from cocos.layer import AnimationLayer

from threading import Thread

class MainMenu(Menu):

#    arial=font.load('Arial',26,bold=True, italic=False)

    def __init__( self ):
        super( MainMenu, self ).__init__("AirHockey")
        self.restart_game = False

#        self.menu_valign = BOTTOM
        self.menu_halign = LEFT

        # then add the items
#        items = [
#            ( MenuItem('Item 1', self.on_quit ) ),
#            ( MenuItem('Item 2', self.on_quit ) ),
#            ( MenuItem('Item 3', self.on_quit ) ),
#            ( MenuItem('Item 4', self.on_quit ) ),


#        ]

#        self.create_menu( items, selected_effect=zoom_in(),
#                          unselected_effect=zoom_out())
        
        
        # then add the items
#        item1= ToggleMenuItem('ToggleMenuItem: ', self.on_toggle_callback,# True )

#        item1 = EntryMenuItem('Your name:', self.on_entry_callback, '',
#                              max_length=24)
#        item2 = EntryMenuItem('IP:Port :', self.change_IP, 'localhost:54321',                              max_length=24)

#        resolutions = ['320x200','640x480','800x600', '1024x768', '1200x1024']
#        item2= MultipleMenuItem('Resolution: ',
#                        self.on_multiple_callback,
#                        resolutions)
#        item2 = MenuItem('Settings', self.settings_callback)

        item3 = MenuItem('Network Game', self.network_game_settings)
        item5 = MenuItem('Local Multiplayer', self.start_game, 2)
        item4 = MenuItem('Single Player', self.start_game, 1)
#        item5 = MenuItem('High Score', self.on_callback)
        
#        resolutions = ['ON', 'OFF']
#        item6= MultipleMenuItem('Powerup: ',
#                        self.on_multiple_callback,
#                        resolutions)

        
#        item4 = EntryMenuItem('EntryMenuItem:', self.on_entry_callback, 'value', max_length=8)

        colors = [(255, 255, 255), (129, 255, 100), (50, 50, 100), (255, 200, 150)]
#        item7 = ColorMenuItem('Select your color:', self.on_color_callback, colors)
        item7 = MenuItem('Tutorial', self.tutorial_callback)

#        item7 = ImageMenuItem('Tutorial_image.jpg', self.on_image_callback)
        item8 = MenuItem('Credits', self.play_our_names)
        item9 = MenuItem('Exit', self.on_quit)
        item10 = MenuItem('', self.on_quit)

        
        item2 = ImageMenuItem('res/field_with_audience.png', self.on_image_callback)
        item2.scale=10
#        bg = cocos.scene.Scene("res/field.png", 100,100)
#        director.run(bg)
        #        item2 = MenuItem('', self.on_callback)        
        self.create_menu( [item3,item5,item4,item2, item7, item8, item9], layout_strategy=fixedPositionMenuLayout(
                            [(10, 500), (10, 450),(10, 400),(400, 350),(10, 300),(10, 250), (10, 150)]))        
        
#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8], layout_strategy=fixedPositionMenuLayout([(510, 500), (130, 300), (200, 300), (300, 350), (400,300), (500,300), (600,300),(700,300)]) )
#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8])
#        self.create_menu( [item3,item5,item4,item2, item7, item8, item10, item9])




    def start_game(self, single):
        if single == 2:
            config.local_multiplayer = True
        else:
            config.local_multiplayer = False
        config.single_player = single
        config.server = False
        bg = bg_layer.BgLayer()
        game = game_layer.GameLayer(self.start_game)
        audience = audience_layer.AudienceLayer()
        self.restart_game = True
        scene = Scene(bg, game, audience)
        game.position = (config.screen_width-config.field_width)/2, 0
        bg.position = game.position

        director.push(scene)
        
    def on_quit( self ):
        pyglet.app.exit()
    def change_IP(self, value):
    
        server_url = 'ws://' + value                        
        
    def on_multiple_callback(self, idx ):
        print 'multiple item callback', idx

    def on_toggle_callback(self, b ):
        print 'toggle item callback', b

    def on_callback(self ):
        print 'item callback'

    def on_entry_callback (self, value):
        print 'entry item callback', value

    def on_image_callback (self):
        print 'image item callback'

    def on_color_callback(self, value):
        print 'color item callback:', value
        
    def play_our_names(self):
        print 'Our names gif image running'
        cocos.director.director.push( cocos.scene.Scene( Credits() ) )
    def tutorial_callback(self):

        cocos.director.director.push( cocos.scene.Scene( Tutorial() ) )
    def settings_callback(self):

        cocos.director.director.push( cocos.scene.Scene( Settings() ) )
    def network_game_settings(self):
        print 'Our names gif image running'
        cocos.director.director.push( cocos.scene.Scene( NetworkSettings() ) )
		
        
class Credits(Menu):

#    arial=font.load('Arial',26,bold=True, italic=False)

    def __init__( self ):
        super( Credits, self ).__init__("Creators:")
		
        item3 = MenuItem('Mikko', self.on_callback)
        item4 = MenuItem('Niklas', self.on_callback)
        item5 = MenuItem('Slava', self.on_callback)
        item2 = MenuItem('Alexey', self.on_callback)
        #        item8 = ImageMenuItem('Credits', self.on_image_callback)

        
#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8], layout_strategy=fixedPositionMenuLayout([(510, 500), (130, 300), (200, 300), (300, 350), (400,300), (500,300), (600,300),(700,300)]) )
#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8])
        self.create_menu( [item2, item3,item4,item5])
    def on_callback(self):
        cocos.director.director.pop()

class Tutorial(Menu):

#    arial=font.load('Arial',26,bold=True, italic=False)

    def __init__( self ):
        super( Tutorial, self ).__init__("Tutorial")

        item1 = ImageMenuItem('res/keyboard_singleplayer.png', self.on_image_callback)
        item1.scale=5
#        bg = cocos.sprite.Sprite("res/field.png", position=(config.screen_width,config.screen_height))
#        item2 = MenuItem('', self.on_callback)
        item2 = ImageMenuItem('res/keyboard_2_players.png', self.on_image_callback)
        item1.scale=5
        item2.scale=5

        item3 = MenuItem('Back', self.on_callback)        
#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8], layout_strategy=fixedPositionMenuLayout([(510, 500), (130, 300), (200, 300), (300, 350), (400,300), (500,300), (600,300),(700,300)]) )
#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8])
        self.create_menu( [item1, item2, item3], layout_strategy=fixedPositionMenuLayout(
                            [(300, 500),(300, 300), (300, 150)]))
    def on_image_callback(self):
        cocos.director.director.pop()
    def on_callback(self):
        cocos.director.director.pop()
		
class Settings(Menu):

#    arial=font.load('Arial',26,bold=True, italic=False)

    def __init__( self ):
        super( Settings, self ).__init__("Settings")
        self.menu_halign = LEFT

        resolutions = ['ON', 'OFF']
#        item1= MultipleMenuItem('Powerup: ',
#                        self.on_multiple_callback,
#                        resolutions)

        item1 = EntryMenuItem('AI level :\n', self.change_AI, '1',
                              max_length=24)
		
        item2 = EntryMenuItem('IP:Port :\n', self.change_IP, 'localhost:54321',
                              max_length=24)
		

        item3 = MenuItem('Back', self.on_callback)
        #        item8 = ImageMenuItem('Credits', self.on_image_callback)
        item4 = MenuItem(' ', self.on_callback)

#        self.create_menu( [item1, item2, item4 ,item3])
        self.create_menu( [item1, item2, item4 ,item3])
    def on_callback(self):
        cocos.director.director.pop()
    def change_IP(self, value):    
        server_url = 'ws://' + value                        
    def on_multiple_callback(self, idx ):
        print 'multiple item callback', idx
    def change_AI(self, value):    
        difficulty = value                        


class NetworkSettings(Menu):
    def __init__(self):
    
        super( NetworkSettings, self ).__init__("Settings")
        self.menu_halign = LEFT
        item2 = EntryMenuItem('IP:Port :\n', self.change_IP, 'localhost:54321',
                              max_length=24)
		

        item3 = MenuItem('Start', self.start_game, 0)
        #        item8 = ImageMenuItem('Credits', self.on_image_callback)
        item4 = MenuItem('Back', self.on_callback)

#        self.create_menu( [item1, item2, item4 ,item3])
        self.create_menu( [item3,item2, item4 ])
    def on_callback(self):
        cocos.director.director.pop()
    def change_IP(self, value):    
        server_url = 'ws://' + value                        
    def start_game(self, single):
        if single == 2:
            config.local_multiplayer = True
        else:
            config.local_multiplayer = False
        config.single_player = single
        config.server = False
        bg = bg_layer.BgLayer()
        game = game_layer.GameLayer(self.start_game)
        audience = audience_layer.AudienceLayer()
        self.restart_game = True
        scene = Scene(bg, game, audience)
        game.position = (config.screen_width-config.field_width)/2, 0
        bg.position = game.position

        director.push(scene)        

		
def main():

    pyglet.font.add_directory('.')

    director.init( resizable=True)
    director.run( Scene( MainMenu() ) )

if __name__ == '__main__':
    main()
