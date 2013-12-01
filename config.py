import sys
# from pyglet.window import key

# the server should not import cocos or pyglet
bindings = {
    65361: 'left', # key.LEFT
    65363: 'right', # key.RIGHT
    65362: 'up', # key.UP
    65364: 'down', # key.DOWN

    97: 'left2', # key.A
    100: 'right2', # key.D
    119: 'up2', # key.W
    115: 'down2', # key.S
}

tick = 0.02

#entities physical properties
max_vel = 500.0
acc = 1000.0
decel = 10.0
radius = 16.0
elasticity = 1.0 #1 is perfectly elastic collisions, 0 is perfectly inelastic
mass = 1.0
difficulty=1

screen_height = 800
screen_width = 800

field_height = 800
field_width = 600

#players "own walls" distance from goal
goal_wall_distance = 100

goal_width = 200
goal_depth = 50

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