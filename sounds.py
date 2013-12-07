import pyglet

# use pyglet effects instead of cocos effects because cocos effects can't be stopped

# uncomment these when sounds exist, also search game_layer.py for sounds.whatever and uncomment their lines
#win = pyglet.media.load("res/win.wav", streaming=False)
#goal = pyglet.media.load("res/goal.wav", streaming=False)
#lose = pyglet.media.load("res/lose.wav", streaming=False)

go = pyglet.media.load("res/go.wav", streaming=False)
goal = pyglet.media.load("res/go.wav", streaming=False)

# don't use cocos's scene music because it doesn't work
#background = pyglet.media.load("res/background.wav", streaming=False)
