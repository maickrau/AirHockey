class InputManager():

    def getInputModel(self, keys_pressed):
        return InputModel()


class InputModel():

    def __init__(self):
        self.ball1up = False
        self.ball1down = False
        self.ball1left = False
        self.ball1right = False
        #etc.. for other controls