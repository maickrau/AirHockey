# from pyglet.window import key

# bindings = {
#     key.LEFT: 'left',
#     key.RIGHT: 'right',
#     key.UP: 'up',
#     key.DOWN: 'down',

#     key.A: 'left2',
#     key.D: 'right2',
#     key.W: 'up2',
#     key.S: 'down2',
# }

# the server should not import cocos or pyglet
bindings = {
    65361: 'left',
    65363: 'right',
    65362: 'up',
    65364: 'down',

    97: 'left2',
    100: 'right2',
    119: 'up2',
    115: 'down2',
}

tick = 0.01

#entities physical properties
max_vel = 1000.0
acc = 1000.0
decel = 10.0
radius = 16.0
elasticity = 1.0 #1 is perfectly elastic collisions, 0 is perfectly inelastic
mass = 1.0

height = 800
width = 400

server_url = "ws://localhost:54321"
state_history_size = 100

# print key.LEFT, key.RIGHT, key.UP, key.DOWN
# print key.A, key.D, key.W, key.S