import sys
# from pyglet.window import key

# the server should not import cocos or pyglet

#default bindings, used in network multiplayer and singleplayer vs AI but not in local multiplayer

bindings = {
    65361: 'left', # arrow left
    65363: 'right', # arrow right
    65362: 'up', # arrow up
    65364: 'down', # arrow down

    97: 'left2', # key.A
    100: 'right2', # key.D
    119: 'up2', # key.W
    115: 'down2', # key.S
}

#bindings for player 1 in local multiplayer
bindings_local_multiplayer1 = {
    65361: 'left2', # arrow left
    65363: 'right2', # arrow right
    65362: 'up2', # arrow up
    65364: 'down2', # arrow down

    65460: 'left', # numpad left
    65462: 'right', # numpad right
    65464: 'up', # numpad up
    65458: 'down', # numpad down
}

#bindings for player 2 in local multiplayer
bindings_local_multiplayer2 = {
    97: 'left2', # key.A
    100: 'right2', # key.D
    119: 'up2', # key.W
    115: 'down2', # key.S

    118: 'left', # key.V
    110: 'right', # key.N
    103: 'up', # key.G
    98: 'down', # key.B
}

tick = 0.02

#entities physical properties
max_vel = 500.0
acc = 1000.0
decel = 10.0
radius = 16.0
elasticity = 1.0 #1 is perfectly elastic collisions, 0 is perfectly inelastic
mass = 1.0

height = 800
width = 600

#players "own walls" distance from goal
goal_wall_distance = 100

goal_width = 200
goal_depth = 50

local_multiplayer = False
server = False
single_player = 0
server_url = "ws://localhost:54321"
if len(sys.argv) > 1:
    if sys.argv[1] == 'single':
        single_player = 1
    else:
        server_url = 'ws://' + sys.argv[1]

state_history_size = 100
soft_skip_thres = 10
hard_skip_thres = 20
soft_skip_period = 5

# print key.LEFT, key.RIGHT, key.UP, key.DOWN
# print key.A, key.D, key.W, key.S