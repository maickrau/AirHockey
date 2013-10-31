import config
import physics

if config.server:
    import serverentity as entityclass
else:
    import cliententity as entityclass

class Ball(entityclass.Entity):

    #Constructor for Ball instance, defaults pos x and y to 0, 0 if not given

    def __init__(self, init_pos, ident):
        super(Ball, self).__init__(init_pos, ident, ident == 'puck' and 'res/puck.png' or 'res/ball.png')
        self.radius = config.radius
        self.collidable = True


class PlayerControlledBall(Ball):

    #Constructor for player controlled ball.
    #Parameter "number" is 1 for left and 2 for right(used to assign controls)
    def __init__(self, number):
        super(PlayerControlledBall, self).__init__()

class PowerUp(entityclass.Entity):

    def __init__(self, init_pos, ident, sprite_sheet):
        super(PowerUp, self).__init__(init_pos, ident, sprite_sheet)
        self.remove = False
        self.visible = True

    def update(self, dt, entities):
        #Method should be implemented in specific instance of powerup
        raise NotImplementedError("This method should be implemented in child!")


#Speed up the player ball for limited time
class SpeedPowerUp(PowerUp):

    def __init__(self):
        super(SpeedPowerUp, self).__init__()

    def update(self, dt, entities):
        for e in entities:
            if physics.isColliding(self, e):
                if isinstanceof(e, PlayerControlledBall):
                    print("This SpeedPowerUp is colliding with a PlayerControlledBall")
                    trigger(e)

    def trigger(ball):
        #TODO implement
        print("")


#Grows the size of the player ball for limited time
class GrowPowerUp(PowerUp):

    def __init__(self):
        super(SpeedPowerUp, self).__init__()

    def update(self, dt, entities):
        for e in entities:
            if physics.isColliding(self, e):
                if isinstanceof(e, PlayerControlledBall):
                    print("This GrowPowerUp is colliding with a PlayerControlledBall")
                    trigger(e)

    def trigger(ball):
        #TODO implement
        print("")