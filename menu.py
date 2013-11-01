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

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *

import config
import game_layer

class MainMenu(Menu):

#    arial=font.load('Arial',26,bold=True, italic=False)

    def __init__( self ):
        super( MainMenu, self ).__init__("AirHockey  v1.0")


#        self.menu_valign = BOTTOM
#        self.menu_halign = RIGHT

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

        item1 = EntryMenuItem('', self.on_entry_callback, 'Your name',
                              max_length=24)
        resolutions = ['320x200','640x480','800x600', '1024x768', '1200x1024']
        item2= MultipleMenuItem('Resolution: ',
                        self.on_multiple_callback,
                        resolutions)
        item3 = MenuItem('Server Game', self.start_game, 0)
        item4 = MenuItem('Single Player', self.start_game, 1)
        item5 = MenuItem('High Score', self.on_callback)
		
        resolutions = ['ON', 'OFF']
        item6= MultipleMenuItem('Powerup: ',
                        self.on_multiple_callback,
                        resolutions)

		
#        item4 = EntryMenuItem('EntryMenuItem:', self.on_entry_callback, 'value', max_length=8)

        colors = [(255, 255, 255), (129, 255, 100), (50, 50, 100), (255, 200, 150)]
        item7 = ColorMenuItem('Select your color:', self.on_color_callback, colors)
#        item8 = ImageMenuItem('Credits', self.on_image_callback)
        item8 = MenuItem('Credits', self.play_our_names)

#        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8], layout_strategy=fixedPositionMenuLayout([(510, 500), (130, 300), (200, 300), (300, 350), (400,300), (500,300), (600,300),(700,300)]) )
        self.create_menu( [item1,item2,item3,item4,item5,item6, item7, item8])


    def start_game(self, single):
        config.single_player = single
        config.server = False
        game = game_layer.GameLayer()
        scene = Scene(game)
        director.run(scene)
		
    def on_quit( self ):
        pyglet.app.exit()

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

def main():

    pyglet.font.add_directory('.')

    director.init( resizable=True)
    director.run( Scene( MainMenu() ) )

if __name__ == '__main__':
    main()