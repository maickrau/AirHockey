import config


class InputManager():

    def __init__(self):
        # to be used for serialized representation of input state
        self.serial = {'letters': {'x': 0, 'y': 0}, 'arrows': {'x': 0, 'y': 0}}
        self.buttons = {}
        for v in config.bindings.values():
            self.buttons[v] = 0

    def update_key(self, k, pressed):
        binds = config.bindings
        if k in binds:
            self.buttons[binds[k]] = pressed

        two = ''
        self.serial['arrows']['x'] = self.buttons['right' + two] - self.buttons['left' + two]
        self.serial['arrows']['y'] = self.buttons['up' + two] - self.buttons['down' + two]
        two = '2'
        self.serial['letters']['x'] = self.buttons['right' + two] - self.buttons['left' + two]
        self.serial['letters']['y'] = self.buttons['up' + two] - self.buttons['down' + two]

    def get(self, ident, axis):
        input_data = self.serial.get(ident)
        if input_data is None:
            return 0
        return input_data[axis]