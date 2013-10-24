from pyglet.window import key

bindings = {
    key.LEFT: 'left',
    key.RIGHT: 'right',
    key.UP: 'up',
    key.DOWN: 'down',

    key.A: 'left2',
    key.D: 'right2',
    key.W: 'up2',
    key.S: 'down2',
}

max_vel = 100.0
acc = 100.0
decel = 10.0
radius = 16.0
height = 800
width = 400