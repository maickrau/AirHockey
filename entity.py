import config
import physics
import util
import euclid as eu

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

class Wall(entityclass.SpritelessEntity):
    def __init__(self, start, end, ident):
        super(Wall, self).__init__(start, ident, "")
        self.start = start
        self.end = end
        self.collidable = True
        self.direction = (end-start).normalized()
        self.tangent = eu.Vector2(self.direction.y, -self.direction.x)
        self.length = (end-start).magnitude()

class WallCorner(entityclass.SpritelessEntity):
    def __init__(self, wall, which_end):
        ident = wall.ident + "_corner_" + str(which_end)
        if which_end == 1:
            init_pos = wall.end
        else:
            init_pos = wall.start
        super(WallCorner, self).__init__(init_pos, ident, "")
        self.radius = 0
        self.collidable = wall.collidable

class PlayerControlledBall(Ball):

    #Constructor for player controlled ball.
    #Parameter "number" is 1 for left and 2 for right(used to assign controls)
    def __init__(self, init_pos, ident):
        super(PlayerControlledBall, self).__init__(init_pos, ident)

class PowerUp(entityclass.Entity):

    def __init__(self, init_pos, ident, sprite_sheet):
        super(PowerUp, self).__init__(init_pos, ident, sprite_sheet)
        self.remove = False
        self.visible = True

    def update(self, dt, entities):
        #Method should be implemented in specific instance of powerup
        raise NotImplementedError("This method should be implemented in child!")


#Immobilizes the ball for limited time
class StopPowerUp(PowerUp):

    def __init__(self, init_pos, ident):
        super(StopPowerUp, self).__init__(init_pos, ident, "res/stop.png")
        self.used = False
        #temp radius, used only in physics atm because no other shapes
        self.radius = config.radius

    def update(self, dt, entities):
        if self.remove:
            return
        if not self.used:
            for e in entities:
                #!!! Temporary!!#
                if False:
                #if isinstance(e, PlayerControlledBall):
                    if physics.isColliding(self, e):
                        print("This StopPowerUp is colliding with a PlayerControlledBall")
                        self.ball = e
                        self.trigger()
        elif self.used:
            self.timer.addTime(dt)
            if self.timer.isDone():
                self.remove = True
                self.ball.maxVel = config.maxVel
            else:
                self.ball.maxVel = 0

    def _trigger(self):
        self.timer = util.Timer(5000)
        self.visible = False
        self.used = True