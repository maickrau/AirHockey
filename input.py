import config

class InputManager():

    def __init__(self, num):
        # to be used for serialized representation of input state
        self.serial = {
            'letters' + num: {'x': 0, 'y': 0}, 
            'arrows' + num: {'x': 0, 'y': 0}, 'seq': 0, 'type': 'input'
        }
        self.buttons = {}
        self.num = num
        for v in config.bindings.values():
            self.buttons[v] = 0

    def update_key(self, k, pressed):
        binds = config.bindings
        if k in binds:
            self.buttons[binds[k]] = pressed

        two = ''
        self.serial['arrows' + self.num]['x'] = self.buttons['right' + two] - self.buttons['left' + two]
        self.serial['arrows' + self.num]['y'] = self.buttons['up' + two] - self.buttons['down' + two]
        two = '2'
        self.serial['letters' + self.num]['x'] = self.buttons['right' + two] - self.buttons['left' + two]
        self.serial['letters' + self.num]['y'] = self.buttons['up' + two] - self.buttons['down' + two]

    def get(self, ident, axis):
        input_data = self.serial.get(ident)
        if input_data is None:
            return 0
        return input_data[axis]